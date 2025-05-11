"""
Data Models
~~~~~~~~~~

This module provides data models for the Mixin Network client.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, root_validator


class Membership(BaseModel):
    """Membership information for a user."""

    plan: str
    expired_at: datetime


class App(BaseModel):
    """App information associated with a user."""

    type: str
    app_id: str
    app_number: str
    redirect_uri: str
    home_uri: str
    name: str
    icon_url: str
    description: str
    capabilities: list[str]
    resource_patterns: list[str]
    category: str
    creator_id: str
    updated_at: datetime
    is_verified: bool
    tip_key_base64: str
    tip_counter: int
    has_safe: bool
    spend_public_key: str
    safe_created_at: datetime
    app_secret: str
    session_public_key: str
    session_secret: str
    capabilites: list[str]


class User(BaseModel):
    """User information from Mixin Network."""

    type: str
    user_id: str
    identity_number: str
    phone: str
    full_name: str
    biography: str
    avatar_url: str
    relationship: str
    mute_until: datetime
    created_at: datetime
    is_verified: bool
    is_scam: bool
    is_deactivated: bool
    code_id: str
    code_url: str
    features: Optional[dict[str, Any]]
    has_safe: bool
    membership: Membership
    email: str
    app_id: str
    app: App
    session_id: str
    device_status: str
    has_pin: bool
    salt_exported_at: datetime
    receive_message_source: str
    accept_conversation_source: str
    accept_search_source: str
    fiat_currency: str
    transfer_notification_threshold: float
    transfer_confirmation_threshold: float
    pin_token_base64: str
    pin_token: str
    salt_base64: str
    tip_key_base64: str
    tip_counter: int
    spend_public_key: str
    has_emergency_contact: bool


class UserResponse(BaseModel):
    """API response wrapper for user data."""

    data: User


class MessageData(BaseModel):
    """Message data from Mixin Network."""

    type: Optional[str] = Field(default="message")
    representative_id: Optional[str] = None
    quote_message_id: Optional[str] = None
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    message_id: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    category: Optional[str] = None
    data: Optional[str] = None 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Compatibility fields with old model
    id: Optional[str] = None
    content: Optional[str] = None
    
    class Config:
        populate_by_name = True
        extra = "allow"
        arbitrary_types_allowed = True
        
    @root_validator(pre=True)
    def handle_fields(cls, values):
        # Handle API response format variations
        # Debug logging of received data
        # print(f"Received message data: {values}")
        
        # These are convenience aliases for working with different field names
        if 'id' in values and not values.get('message_id'):
            values['message_id'] = values['id']
        elif 'message_id' in values and not values.get('id'):
            values['id'] = values['message_id']
            
        if 'content' in values and not values.get('data'):
            values['data'] = values['content']
        elif 'data' in values and not values.get('content'):
            values['content'] = values['data']
            
        return values


class Message(MessageData):
    """Backward compatible Message model"""
    
    media_url: Optional[str] = None
    media_name: Optional[str] = None
    media_size: Optional[int] = None
    media_duration: Optional[int] = None
    media_width: Optional[int] = None
    media_height: Optional[int] = None
    media_hash: Optional[str] = None
    thumb_url: Optional[str] = None
    

class MessageResponse(BaseModel):
    """API response wrapper for message data."""

    data: MessageData


class MessageListResponse(BaseModel):
    """API response wrapper for a list of messages."""

    data: list[MessageData]
