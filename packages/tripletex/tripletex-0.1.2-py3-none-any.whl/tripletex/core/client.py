from __future__ import annotations

import logging
import os
import threading
import time
from typing import TYPE_CHECKING, Any, Optional, Union

import requests  # Need this for type hints and accessing response
from crudclient.client import Client
from crudclient.exceptions import RateLimitError  # Need this exception

from tripletex.core.config import TripletexConfig, TripletexTestConfig

log = logging.getLogger(__name__)


# --- Type Hinting for Multiprocessing Objects ---
# This block is only evaluated by type checkers (like Pylance, Mypy), not at runtime.
if TYPE_CHECKING:
    # Import the module or specific types needed for hints.
    import multiprocessing


class TripletexClient(Client):
    def __init__(
        self,
        config: TripletexConfig | None = None,
        # Use the types imported within TYPE_CHECKING block for hints
        mp_lock: Optional[multiprocessing.Lock] = None,
        mp_remaining: Optional[Any] = None,  # mp.Value returns a proxy object, Any is safest
        mp_reset_timestamp: Optional[Any] = None,  # mp.Value returns a proxy object, Any is safest
    ) -> None:
        if config is None:
            config = TripletexTestConfig() if os.getenv("DEBUG", "") == "1" else TripletexConfig()

        super().__init__(config=config)

        # --- Rate Limiting State (Inter-Process or Thread-Based) ---
        self._is_multiprocessing = mp_lock is not None and mp_remaining is not None and mp_reset_timestamp is not None

        if self._is_multiprocessing:
            # Use provided multiprocessing objects
            # The Union can now also use the directly imported type
            self._rate_limit_lock: Union[multiprocessing.Lock, threading.Lock] = mp_lock  # type: ignore
            self._mp_rate_limit_remaining = mp_remaining  # Stores int, use .value
            self._mp_rate_limit_reset_timestamp = mp_reset_timestamp  # Stores float (double), use .value
            log.info("TripletexClient initialized with multiprocessing rate limiting.")
        else:
            # Fallback to thread-based (for single process use)
            self._rate_limit_lock = threading.Lock()
            self._thread_rate_limit_remaining: Optional[int] = None
            self._thread_rate_limit_reset_timestamp: float = 0.0
            log.info("TripletexClient initialized with thread-based rate limiting.")
        # --------------------------

    def _update_rate_limit_state(self, response: Optional[requests.Response]) -> None:
        """Helper to update rate limit state from a response object."""
        if response is None:
            return

        try:
            remaining_str = response.headers.get("X-Rate-Limit-Remaining")
            reset_str = response.headers.get("X-Rate-Limit-Reset")  # Seconds until reset

            if remaining_str is not None and reset_str is not None:
                # Acquire the appropriate lock (multiprocessing or threading)
                with self._rate_limit_lock:
                    try:
                        remaining = int(remaining_str)
                        reset_seconds = int(reset_str)
                        now = time.monotonic()
                        new_reset_timestamp = now + reset_seconds

                        # Get current values (depending on mode)
                        if self._is_multiprocessing:
                            current_reset_ts = self._mp_rate_limit_reset_timestamp.value  # type: ignore
                            current_remaining = self._mp_rate_limit_remaining.value  # type: ignore
                            # Use a large number if remaining is unknown (-1 is our convention for unknown in mp.Value)
                            current_remaining_comp = float("inf") if current_remaining == -1 else current_remaining
                        else:
                            current_reset_ts = self._thread_rate_limit_reset_timestamp
                            current_remaining = self._thread_rate_limit_remaining
                            current_remaining_comp = float("inf") if current_remaining is None else current_remaining

                        # Update only if the new info is relevant (more recent reset or same reset time with lower count)
                        if new_reset_timestamp > current_reset_ts or (new_reset_timestamp == current_reset_ts and remaining < current_remaining_comp):

                            # Set new values (depending on mode)
                            if self._is_multiprocessing:
                                self._mp_rate_limit_remaining.value = remaining  # type: ignore
                                self._mp_rate_limit_reset_timestamp.value = new_reset_timestamp  # type: ignore
                            else:
                                self._thread_rate_limit_remaining = remaining
                                self._thread_rate_limit_reset_timestamp = new_reset_timestamp

                            log.debug(
                                f"Updated rate limit state from headers: Remaining={remaining}, ResetIn={reset_seconds}s (Timestamp={new_reset_timestamp:.2f})"
                            )
                        # else: log.debug("Skipping rate limit state update as it's older or not more restrictive.")

                    except (ValueError, TypeError) as parse_err:
                        log.warning(f"Could not parse rate limit headers: {parse_err}")
        except Exception as header_err:
            log.warning(f"Error processing rate limit headers: {header_err}")

    def _wait_for_rate_limit(self) -> None:
        """
        Checks rate limit (using shared state if configured) and waits if necessary,
        ensuring atomicity for concurrent processes/threads.
        """
        RATE_LIMIT_THRESHOLD = 30  # Threshold to start waiting

        # Use the appropriate lock (multiprocessing or threading)
        with self._rate_limit_lock:
            while True:  # Loop until allowed to proceed
                now = time.monotonic()

                # --- Get current state (depending on mode) ---
                if self._is_multiprocessing:
                    reset_ts = self._mp_rate_limit_reset_timestamp.value  # type: ignore
                    remaining = self._mp_rate_limit_remaining.value  # type: ignore
                    is_unknown = remaining == -1  # Use -1 convention for unknown in mp.Value
                else:
                    reset_ts = self._thread_rate_limit_reset_timestamp
                    remaining = self._thread_rate_limit_remaining
                    is_unknown = remaining is None
                # --- State retrieved ---

                # Reset remaining count if reset time has passed
                if now >= reset_ts:
                    if not is_unknown:  # Only log/reset if it wasn't already unknown
                        log.debug("Rate limit reset time passed. Resetting count to unknown.")
                        if self._is_multiprocessing:
                            self._mp_rate_limit_remaining.value = -1  # type: ignore
                        else:
                            self._thread_rate_limit_remaining = None
                    is_unknown = True  # Now considered unknown
                    remaining = -1 if self._is_multiprocessing else None  # Update local vars for checks below

                # --- Check if we need to wait ---
                # Wait if limit is known AND at or below threshold
                if not is_unknown and remaining <= RATE_LIMIT_THRESHOLD:
                    wait_time = reset_ts - now
                    if wait_time <= 0:
                        # Reset time passed while checking, reset state and restart loop
                        log.debug("Rate limit reset time passed during check. Re-evaluating.")
                        if self._is_multiprocessing:
                            self._mp_rate_limit_remaining.value = -1  # type: ignore
                        else:
                            self._thread_rate_limit_remaining = None
                        continue  # Restart the while loop

                    wait_time += 0.1  # Add buffer
                    log.warning(
                        f"Rate limit threshold hit (remaining={remaining}, threshold={RATE_LIMIT_THRESHOLD}). "
                        f"Waiting for {wait_time:.2f} seconds."
                    )

                    # --- Release lock ONLY for sleeping ---
                    self._rate_limit_lock.release()
                    try:
                        time.sleep(wait_time)
                    finally:
                        # --- Re-acquire lock immediately ---
                        self._rate_limit_lock.acquire()
                    # --- Lock re-acquired ---

                    # After waiting, restart the loop to re-check the condition
                    continue

                # --- If allowed to proceed ---
                # Decrement if limit is known and above threshold
                elif not is_unknown:
                    # Decrement *before* releasing the lock for the actual request
                    new_remaining = remaining - 1
                    if self._is_multiprocessing:
                        self._mp_rate_limit_remaining.value = new_remaining  # type: ignore
                    else:
                        self._thread_rate_limit_remaining = new_remaining
                    log.debug(f"Proceeding with request. Decremented rate limit remaining count to {new_remaining}")
                    break  # Exit the while loop, permission granted

                # Proceed if limit is unknown
                else:  # is_unknown is True
                    log.debug("Rate limit remaining is unknown. Proceeding optimistically.")
                    break  # Exit the while loop, permission granted

    def _request(self, method: str, endpoint: str | None = None, url: str | None = None, **kwargs) -> Any:
        # Original handle_response logic (specific to TripletexClient)
        original_handle_response = method != "DELETE"
        # Get handle_response from kwargs if provided, otherwise use default
        handle_response_arg = kwargs.pop("handle_response", original_handle_response)

        # --- Rate Limiting Wait ---
        self._wait_for_rate_limit()
        # --- End Rate Limiting Wait ---

        raw_response: Optional[requests.Response] = None
        result: Any = None
        try:
            # Always call super()._request with handle_response=False to get the raw response
            # We need the raw response to access headers for rate limiting state update.
            # Ensure the request uses the potentially modified kwargs
            raw_response = super()._request(method, endpoint=endpoint, url=url, handle_response=False, **kwargs)

            # Now, handle the response processing based on the original handle_response_arg
            if handle_response_arg:
                # Manually trigger response handling using the http_client's handler
                # This mimics what crudclient.Client._request -> http_client._request -> _handle_request_response does
                try:
                    # Ensure response is valid before handling
                    if not isinstance(raw_response, requests.Response):
                        raise TypeError(f"Expected requests.Response, got {type(raw_response).__name__}")
                    # Raise HTTP errors (like 4xx, 5xx) to be caught below or handled by caller
                    raw_response.raise_for_status()
                    # Process the successful response using the handler from the http_client
                    result = self.http_client.response_handler.handle_response(raw_response)
                except requests.HTTPError as http_err:
                    # Let crudclient's error handling take over if raise_for_status fails
                    # We still update rate limit state in finally block
                    self.http_client._handle_http_error(http_err)  # This will raise the appropriate CrudClientError
                    # This line technically shouldn't be reached if _handle_http_error raises
                    raise http_err from http_err
            else:
                # If original request didn't want handling, return the raw response
                result = raw_response

        except RateLimitError as rle:
            # If super()._request raises RateLimitError, try to update state from its response
            self._update_rate_limit_state(rle.response)
            raise rle  # Re-raise the exception
        except Exception as e:
            # Catch other exceptions, potentially update state if response is available
            response_for_update = None
            if isinstance(raw_response, requests.Response):
                response_for_update = raw_response
            elif hasattr(e, "response") and isinstance(e.response, requests.Response):
                response_for_update = e.response  # type: ignore

            if response_for_update:
                self._update_rate_limit_state(response_for_update)

            # Re-raise the original exception if one occurred
            if isinstance(e, Exception) and not isinstance(e, RateLimitError):  # RateLimitError already handled
                raise e

        finally:
            # Final attempt to update state if we have a raw response
            # (covers cases where handling failed but we got a response)
            if raw_response is not None and isinstance(raw_response, requests.Response):
                self._update_rate_limit_state(raw_response)

        return result
