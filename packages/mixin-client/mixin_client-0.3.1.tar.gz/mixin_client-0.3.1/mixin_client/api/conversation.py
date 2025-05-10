"""
Conversation API
~~~~~~~~~~~~~~

This module provides the Conversation API interface for the Mixin Network client.
"""

from typing import Any, List, Optional, Union

from ..http import HttpRequest


class ConversationApi:
    """API interface for conversation-related operations."""
    
    def __init__(self, http: HttpRequest):
        """Initialize the API with an HTTP client.

        Args:
            http (HttpRequest): The HTTP client to use for API requests.
        """
        self._http = http

    def create_conversation(
        self, user_id: Union[str, List[str]], name: Optional[str] = None
    ) -> dict[str, Any]:
        """Create a new conversation with a user or group of users.

        Args:
            user_id (Union[str, List[str]]): The user ID or list of user IDs to create a conversation with.
            name (Optional[str], optional): The name of the conversation (for group chats). Defaults to None.

        Returns:
            dict[str, Any]: Conversation information.

        Example:
            >>> client = MixinClient(config)
            >>> # Create a direct conversation
            >>> conversation = client.api.conversation.create_conversation("user_id")
            >>> # Create a group conversation
            >>> group = client.api.conversation.create_conversation(
            ...     ["user_id1", "user_id2"], 
            ...     name="Group Chat"
            ... )
            >>> print(group)
        """
        data = {}
        
        if isinstance(user_id, list):
            data["category"] = "GROUP"
            data["participants"] = [{"user_id": uid} for uid in user_id]
            if name:
                data["name"] = name
        else:
            data["category"] = "CONTACT"
            data["participants"] = [{"user_id": user_id}]

        return self._http.post("/conversations", body=data)
        
    def get_conversation(self, conversation_id: str) -> dict[str, Any]:
        """Get information about a conversation.

        Args:
            conversation_id (str): The ID of the conversation to fetch.

        Returns:
            dict[str, Any]: Conversation information.

        Example:
            >>> client = MixinClient(config)
            >>> conversation = client.api.conversation.get_conversation("conversation_id")
            >>> print(conversation)
        """
        return self._http.get(f"/conversations/{conversation_id}")
        
    def update_conversation(
        self, conversation_id: str, name: str, announcement: Optional[str] = None
    ) -> dict[str, Any]:
        """Update a conversation's information (for group chats).

        Args:
            conversation_id (str): The ID of the conversation to update.
            name (str): The new name for the conversation.
            announcement (Optional[str], optional): The new announcement for the conversation. Defaults to None.

        Returns:
            dict[str, Any]: Updated conversation information.

        Example:
            >>> client = MixinClient(config)
            >>> conversation = client.api.conversation.update_conversation(
            ...     "conversation_id",
            ...     name="New Group Name",
            ...     announcement="Welcome to the group!"
            ... )
            >>> print(conversation)
        """
        data = {"name": name}
        if announcement is not None:
            data["announcement"] = announcement
            
        return self._http.post(f"/conversations/{conversation_id}", body=data)
        
    def add_participants(
        self, conversation_id: str, user_ids: List[str]
    ) -> dict[str, Any]:
        """Add participants to a group conversation.

        Args:
            conversation_id (str): The ID of the conversation to update.
            user_ids (List[str]): The list of user IDs to add to the conversation.

        Returns:
            dict[str, Any]: Updated conversation information.

        Example:
            >>> client = MixinClient(config)
            >>> conversation = client.api.conversation.add_participants(
            ...     "conversation_id",
            ...     ["user_id1", "user_id2"]
            ... )
            >>> print(conversation)
        """
        data = {
            "action": "ADD",
            "participants": [{"user_id": uid} for uid in user_ids]
        }
        
        return self._http.post(f"/conversations/{conversation_id}/participants", body=data)
        
    def remove_participants(
        self, conversation_id: str, user_ids: List[str]
    ) -> dict[str, Any]:
        """Remove participants from a group conversation.

        Args:
            conversation_id (str): The ID of the conversation to update.
            user_ids (List[str]): The list of user IDs to remove from the conversation.

        Returns:
            dict[str, Any]: Updated conversation information.

        Example:
            >>> client = MixinClient(config)
            >>> conversation = client.api.conversation.remove_participants(
            ...     "conversation_id",
            ...     ["user_id1", "user_id2"]
            ... )
            >>> print(conversation)
        """
        data = {
            "action": "REMOVE",
            "participants": [{"user_id": uid} for uid in user_ids]
        }
        
        return self._http.post(f"/conversations/{conversation_id}/participants", body=data)
        
    def exit_conversation(self, conversation_id: str) -> dict[str, Any]:
        """Exit a group conversation.

        Args:
            conversation_id (str): The ID of the conversation to exit.

        Returns:
            dict[str, Any]: Response from the API.

        Example:
            >>> client = MixinClient(config)
            >>> response = client.api.conversation.exit_conversation("conversation_id")
            >>> print(response)
        """
        return self._http.post(f"/conversations/{conversation_id}/exit", body={}) 