import base64
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests
from crudclient import ClientConfig  # type: ignore[attr-defined]

logger: logging.Logger

class TripletexConfig(ClientConfig):
    """
    Configuration class for the Tripletex API client.

    Handles authentication tokens, session management, and API endpoint details.
    """

    hostname: str
    version: str
    consumer_token: str
    employee_token: str
    company_id: str
    session_token: Optional[str]
    session_expires_at: Optional[datetime]
    auth_type: str

    def get_auth_token(self) -> Optional[str]:
        """
        Returns Base64-encoded `company_id:session_token` string.
        Called automatically by `auth()` from base class.
        """
        ...

    def is_token_expired(self) -> bool:
        """Checks if the current session token is expired."""
        ...

    def create_date(self) -> str:
        """Generates the expiration date string for token creation (tomorrow)."""
        ...

    def refresh_token(self, force: bool = ...) -> None:
        """
        Refreshes the Tripletex session token.

        Args:
            force: If True, forces a refresh even if the token is not expired.

        Raises:
            ValueError: If consumer or employee tokens are missing.
            requests.RequestException: If the API request fails.
        """
        ...

    def auth_with_company(self, company_id: str) -> Dict[str, Any]:
        """
        Returns the Basic auth header using the given company_id.

        Refreshes the token if it's expired.

        Args:
            company_id: The company ID to use for authentication.

        Returns:
            A dictionary containing the Authorization header.
        """
        ...

    def auth(self) -> Dict[str, Any]:
        """
        Returns the Basic auth header using the default company_id.
        """
        ...

    def should_retry_on_403(self) -> bool:
        """Determines if a retry should occur on a 403 Forbidden response."""
        ...

    def handle_403_retry(self, client: Any) -> None:  # Replace Any with actual client type if known
        """Handles the retry logic for a 403 response, forcing a token refresh."""
        ...

class TripletexTestConfig(TripletexConfig):
    """
    Configuration class specifically for the Tripletex test environment.
    Uses different hostname and environment variables for test tokens.
    """

    hostname: str
    consumer_token: str
    employee_token: str
    log_request_body: bool
