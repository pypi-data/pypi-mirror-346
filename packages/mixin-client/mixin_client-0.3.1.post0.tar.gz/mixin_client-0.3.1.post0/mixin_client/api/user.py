"""
User API
~~~~~~~

This module provides the User API interface for the Mixin Network client.
"""

from typing import Any, Optional

from ..http import HttpRequest
from ..models import UserResponse


class UserApi:
    """API interface for user-related operations."""
    
    def __init__(self, http: HttpRequest):
        """Initialize the API with an HTTP client.

        Args:
            http (HttpRequest): The HTTP client to use for API requests.
        """
        self._http = http

    def get_me(self) -> UserResponse:
        """Get the current user's profile.

        Returns:
            UserResponse: User profile information.

        Example:
            >>> client = MixinClient(config)
            >>> profile = client.api.user.get_me()
            >>> print(profile.data.full_name)
        """
        response = self._http.get("/me")
        return UserResponse(**response)

    def get_user(self, user_id: str) -> dict[str, Any]:
        """Get a user's profile by ID.

        Args:
            user_id (str): The ID of the user to fetch.

        Returns:
            Dict[str, Any]: User profile information.

        Example:
            >>> client = MixinClient(config)
            >>> user = client.api.user.get_user("user_id")
            >>> print(user)
        """
        return self._http.get(f"/users/{user_id}")
        
    def search_user(self, identity_number: str) -> dict[str, Any]:
        """Search for a user by identity number.

        Args:
            identity_number (str): The identity number of the user to search for.

        Returns:
            Dict[str, Any]: User profile information.

        Example:
            >>> client = MixinClient(config)
            >>> user = client.api.user.search_user("123456")
            >>> print(user)
        """
        return self._http.get(f"/search/{identity_number}")
        
    def get_friends(self) -> dict[str, Any]:
        """Get the current user's friends list.

        Returns:
            Dict[str, Any]: List of friends.

        Example:
            >>> client = MixinClient(config)
            >>> friends = client.api.user.get_friends()
            >>> print(friends)
        """
        return self._http.get("/friends")
        
    def update_preferences(
        self, 
        receive_message_source: Optional[str] = None,
        accept_conversation_source: Optional[str] = None,
        fiat_currency: Optional[str] = None,
    ) -> dict[str, Any]:
        """Update user preferences.

        Args:
            receive_message_source (Optional[str], optional): Message source preference. Defaults to None.
            accept_conversation_source (Optional[str], optional): Conversation source preference. Defaults to None.
            fiat_currency (Optional[str], optional): Fiat currency preference. Defaults to None.

        Returns:
            Dict[str, Any]: Updated user preferences.

        Example:
            >>> client = MixinClient(config)
            >>> preferences = client.api.user.update_preferences(fiat_currency="USD")
            >>> print(preferences)
        """
        data = {}
        if receive_message_source is not None:
            data["receive_message_source"] = receive_message_source
        if accept_conversation_source is not None:
            data["accept_conversation_source"] = accept_conversation_source
        if fiat_currency is not None:
            data["fiat_currency"] = fiat_currency
            
        return self._http.post("/me/preferences", body=data)
        
    def rotate_qr_code(self) -> dict[str, Any]:
        """Rotate the current user's QR code.

        Returns:
            Dict[str, Any]: Updated user information with new QR code.

        Example:
            >>> client = MixinClient(config)
            >>> user = client.api.user.rotate_qr_code()
            >>> print(user)
        """
        return self._http.get("/me/code") 