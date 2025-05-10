"""
Message API
~~~~~~~~~~

This module provides the Message API interface for the Mixin Network client.
"""

import base64
import json
import uuid
from typing import Any, Optional

from ..http import HttpRequest
from ..models import MessageResponse


class MessageApi:
    """API interface for message-related operations."""
    
    def __init__(self, http: HttpRequest):
        """Initialize the API with an HTTP client.

        Args:
            http (HttpRequest): The HTTP client to use for API requests.
        """
        self._http = http
    
    def _generate_message_id(self) -> str:
        """Generate a unique message ID.
        
        Returns:
            str: A UUID string for use as a message ID.
        """
        return str(uuid.uuid4())

    def send_message(
        self,
        conversation_id: str,
        category: str,
        message_id: Optional[str] = None,
        **extra_fields
    ) -> MessageResponse:
        """Generic message sender. Only assembles and sends the payload.
        Type-specific logic (encoding, field selection) should be handled by the caller.
        """
        if not message_id:
            message_id = self._generate_message_id()
        data = {
            "conversation_id": conversation_id,
            "category": category,
            "message_id": message_id,
        }
        data.update(extra_fields)
        response = self._http.post("/messages", body=data)
        return MessageResponse(**response)

    def get_message(self, message_id: str) -> MessageResponse:
        """Get a specific message by ID.

        Note: This functionality may not be supported by the API in all cases.

        Args:
            message_id (str): The ID of the message to fetch.

        Returns:
            MessageResponse: Message information.

        Example:
            >>> client = MixinClient(config)
            >>> message = client.api.message.get_message("message_id")
            >>> print(message.data.content)
        """
        response = self._http.get(f"/messages/{message_id}")
        return MessageResponse(**response)

    def acknowledge_message(self, message_id: str) -> dict[str, Any]:
        """Acknowledge receipt of a message.

        Args:
            message_id (str): The ID of the message to acknowledge.

        Returns:
            dict[str, Any]: Response from the API.

        Example:
            >>> client = MixinClient(config)
            >>> response = client.api.message.acknowledge_message("message_id")
            >>> print(response)
        """
        data = {"message_id": message_id, "status": "READ"}
        return self._http.post("/acknowledgements", body=data)
        
    def send_text_message(
        self,
        conversation_id: str,
        content: str,
        recipient_id: Optional[str] = None,
        message_id: Optional[str] = None,
        quote_message_id: Optional[str] = None
    ) -> MessageResponse:
        """Send a plain text message (with base64 encoding and correct field)."""
        encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        extra = {"data": encoded}
        if recipient_id:
            extra["recipient_id"] = recipient_id
        if quote_message_id:
            extra["quote_message_id"] = quote_message_id
        return self.send_message(
            conversation_id=conversation_id,
            category="PLAIN_TEXT",
            message_id=message_id,
            **extra
        )
        
    def send_image_message(
        self,
        conversation_id: str,
        attachment_id: str,
        mime_type: str,
        width: int,
        height: int,
        size: int,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None,
        recipient_id: Optional[str] = None,
        message_id: Optional[str] = None,
        quote_message_id: Optional[str] = None
    ) -> MessageResponse:
        """Send an image message.

        Args:
            conversation_id (str): The ID of the conversation to send the message to.
            attachment_id (str): The ID of the uploaded attachment.
            mime_type (str): The MIME type of the image, e.g., "image/jpeg", "image/png".
            width (int): The width of the image in pixels.
            height (int): The height of the image in pixels.
            size (int): The size of the image in bytes.
            thumbnail_width (Optional[int], optional): The width of the thumbnail. Defaults to None.
            thumbnail_height (Optional[int], optional): The height of the thumbnail. Defaults to None.
            recipient_id (Optional[str], optional): The recipient user ID. If provided, this creates
                                                  a direct message. Defaults to None.
            message_id (Optional[str], optional): The message ID. If not provided, a UUID will be generated.
            quote_message_id (Optional[str], optional): The ID of the message to quote. Defaults to None.

        Returns:
            MessageResponse: The created message.

        Example:
            >>> client = MixinClient(config)
            >>> message = client.api.message.send_image_message(
            ...     conversation_id="conversation_id",
            ...     attachment_id="attachment_id",
            ...     mime_type="image/jpeg",
            ...     width=1024,
            ...     height=768,
            ...     size=1024000,
            ... )
            >>> print(message.data.message_id)
        """
        image_data = {
            "attachment_id": attachment_id,
            "mime_type": mime_type,
            "width": width,
            "height": height,
            "size": size,
        }
        
        if thumbnail_width and thumbnail_height:
            image_data["thumbnail"] = {
                "width": thumbnail_width,
                "height": thumbnail_height
            }
            
        content = json.dumps(image_data)
        # Base64 encode the JSON content
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        return self.send_message(
            conversation_id=conversation_id,
            category="PLAIN_IMAGE",
            content=encoded_content,
            recipient_id=recipient_id,
            message_id=message_id,
            quote_message_id=quote_message_id
        )
        
    def send_contact_message(
        self,
        conversation_id: str,
        user_id: str,
        recipient_id: Optional[str] = None,
        message_id: Optional[str] = None,
        quote_message_id: Optional[str] = None
    ) -> MessageResponse:
        """Send a contact card message.

        Args:
            conversation_id (str): The ID of the conversation to send the message to.
            user_id (str): The user ID of the contact to share.
            recipient_id (Optional[str], optional): The recipient user ID. If provided, this creates
                                                   a direct message. Defaults to None.
            message_id (Optional[str], optional): The message ID. If not provided, a UUID will be generated.
            quote_message_id (Optional[str], optional): The ID of the message to quote. Defaults to None.

        Returns:
            MessageResponse: The created message.

        Example:
            >>> client = MixinClient(config)
            >>> message = client.api.message.send_contact_message(
            ...     conversation_id="conversation_id",
            ...     user_id="contact_user_id",
            ... )
            >>> print(message.data.message_id)
        """
        contact_data = {"user_id": user_id}
        content = json.dumps(contact_data)
        # Base64 encode the JSON content
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        return self.send_message(
            conversation_id=conversation_id,
            category="PLAIN_CONTACT",
            content=encoded_content,
            recipient_id=recipient_id,
            message_id=message_id,
            quote_message_id=quote_message_id
        )
        
    def send_sticker_message(
        self,
        conversation_id: str,
        sticker_id: str,
        album_id: str,
        name: str,
        recipient_id: Optional[str] = None,
        message_id: Optional[str] = None,
        quote_message_id: Optional[str] = None
    ) -> MessageResponse:
        """Send a sticker message.

        Args:
            conversation_id (str): The ID of the conversation to send the message to.
            sticker_id (str): The ID of the sticker.
            album_id (str): The ID of the sticker album.
            name (str): The name of the sticker.
            recipient_id (Optional[str], optional): The recipient user ID. If provided, this creates
                                                  a direct message. Defaults to None.
            message_id (Optional[str], optional): The message ID. If not provided, a UUID will be generated.
            quote_message_id (Optional[str], optional): The ID of the message to quote. Defaults to None.

        Returns:
            MessageResponse: The created message.

        Example:
            >>> client = MixinClient(config)
            >>> message = client.api.message.send_sticker_message(
            ...     conversation_id="conversation_id",
            ...     sticker_id="sticker_id",
            ...     album_id="album_id",
            ...     name="Sticker Name",
            ... )
            >>> print(message.data.message_id)
        """
        sticker_data = {
            "sticker_id": sticker_id,
            "album_id": album_id,
            "name": name
        }
        content = json.dumps(sticker_data)
        # Base64 encode the JSON content
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        return self.send_message(
            conversation_id=conversation_id,
            category="PLAIN_STICKER",
            content=encoded_content,
            recipient_id=recipient_id,
            message_id=message_id,
            quote_message_id=quote_message_id
        )
        
    def send_app_card_message(
        self,
        conversation_id: str,
        app_id: str,
        icon_url: str,
        title: str,
        description: str,
        action: str,
        recipient_id: Optional[str] = None,
        message_id: Optional[str] = None,
        quote_message_id: Optional[str] = None
    ) -> MessageResponse:
        """Send an app card message.

        Args:
            conversation_id (str): The ID of the conversation to send the message to.
            app_id (str): The ID of the app.
            icon_url (str): The URL of the app icon.
            title (str): The title of the app card.
            description (str): The description of the app card.
            action (str): The action URL or deep link for the app card.
            recipient_id (Optional[str], optional): The recipient user ID. If provided, this creates
                                                  a direct message. Defaults to None.
            message_id (Optional[str], optional): The message ID. If not provided, a UUID will be generated.
            quote_message_id (Optional[str], optional): The ID of the message to quote. Defaults to None.

        Returns:
            MessageResponse: The created message.

        Example:
            >>> client = MixinClient(config)
            >>> message = client.api.message.send_app_card_message(
            ...     conversation_id="conversation_id",
            ...     app_id="app_id",
            ...     icon_url="https://example.com/icon.png",
            ...     title="App Title",
            ...     description="App Description",
            ...     action="https://example.com/action",
            ... )
            >>> print(message.data.message_id)
        """
        app_data = {
            "app_id": app_id,
            "icon_url": icon_url,
            "title": title,
            "description": description,
            "action": action
        }
        content = json.dumps(app_data)
        # Base64 encode the JSON content
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        return self.send_message(
            conversation_id=conversation_id,
            category="APP_CARD",
            content=encoded_content,
            recipient_id=recipient_id,
            message_id=message_id,
            quote_message_id=quote_message_id
        ) 