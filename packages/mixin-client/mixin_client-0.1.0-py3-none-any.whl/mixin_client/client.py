"""
Mixin Network Client
~~~~~~~~~~~~~~~~~~

This module provides the main client class for interacting with the Mixin Network.
"""

import requests


class MixinClient:
    """A client for interacting with the Mixin Network API."""

    def __init__(self, api_key: str = None, api_secret: str = None):
        """Initialize the Mixin Network client.

        Args:
            api_key (str, optional): Your Mixin Network API key.
            api_secret (str, optional): Your Mixin Network API secret.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.mixin.one"

    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Make a request to the Mixin Network API.

        Args:
            method (str): The HTTP method to use.
            endpoint (str): The API endpoint to call.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            dict: The JSON response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() 