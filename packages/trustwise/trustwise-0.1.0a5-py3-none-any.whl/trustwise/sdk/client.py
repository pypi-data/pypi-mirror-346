"""
Client for the Trustwise API.

This client provides methods to interact with Trustwise's safety and
alignment metrics.
"""

import json
import logging
from typing import Any, Dict

import requests

from trustwise.sdk.config import TrustwiseConfig

# Configure logger to respect root logger's level
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # Prevent propagation to root logger if no handlers are configured


class TrustwiseClient:
    """Client for the Trustwise API."""

    def __init__(self, config: TrustwiseConfig) -> None:
        """
        Initialize the Trustwise client.

        Args:
            config: Trustwise configuration object.
        """
        self.config = config
        self.headers = {
            "API_KEY": config.api_key,  # Use the API key value directly
            "Content-Type": "application/json",
        }
        logger.debug("Initialized Trustwise client with base URL: %s", config.base_url)

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a POST request to the Trustwise API.

        Args:
            endpoint: The API endpoint URL.
            data: The request payload.

        Returns:
            The API response as a dictionary.

        Raises:
            requests.HTTPError: If the request fails with a non-422 status code.
            Exception: If the request fails for other reasons.
        """
        logger.debug("Making POST request to %s", endpoint)
        logger.debug("Request headers: %s", {k: "***" if k == "Authorization" else v for k, v in self.headers.items()})
        logger.debug("Request data: %s", json.dumps(data))

        try:
            response = requests.post(
                endpoint,
                json=data,
                headers=self._get_headers(),
                timeout=30  # Add timeout to prevent hanging
            )
            
            if response.status_code == 401:
                logger.error("Authentication failed. Please check your API key.")
                logger.debug("Response headers: %s", dict(response.headers))
            
            # For 422 errors, return the response body instead of raising an error
            if response.status_code == 422:
                return response.json()
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e!s}") from e

    def _get_headers(self) -> Dict[str, str]:
        return self.headers 