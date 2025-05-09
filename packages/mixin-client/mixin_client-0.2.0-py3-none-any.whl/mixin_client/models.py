"""
Data Models
~~~~~~~~~~

This module provides data models for the Mixin Network client.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


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
    capabilities: List[str]
    resource_patterns: List[str]
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
    capabilites: List[str]


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
    features: Optional[Dict[str, Any]]
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
