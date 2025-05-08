# tripletex/core/client.pyi
import os
from typing import Any

from crudclient.client import Client

from .config import TripletexConfig, TripletexTestConfig

class TripletexClient(Client):
    """
    Custom HTTP client for interacting with the Tripletex API.

    Handles configuration loading (production or test) and overrides
    the base request method to potentially skip response handling for DELETE requests.
    """

    def __init__(self, config: TripletexConfig | None = ...) -> None:
        """
        Initialize the Tripletex client.

        Args:
            config: An optional configuration object. If None, loads
                    TripletexTestConfig if DEBUG env var is "1", otherwise TripletexConfig.
        """
        ...

    def _request(self, method: str, endpoint: str | None = ..., url: str | None = ..., **kwargs: Any) -> Any:
        """
        Sends an HTTP request to the Tripletex API.

        Overrides the base method to conditionally skip response handling,
        specifically for DELETE requests where Tripletex might return an empty body.

        Args:
            method: The HTTP method (e.g., 'GET', 'POST', 'DELETE').
            endpoint: The API endpoint path (appended to base_url).
            url: An absolute URL to use instead of base_url + endpoint.
            **kwargs: Additional arguments passed to the underlying request library.

        Returns:
            The processed response data (usually a dict or list) or raw response object,
            depending on the base client's implementation and the handle_response flag.
        """
        ...
