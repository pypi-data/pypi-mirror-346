"""
Test cases for data models.
"""

from datetime import datetime

from mixin_client.models import App, Membership, User, UserResponse


def test_membership_model():
    """Test Membership model creation and validation."""
    membership = Membership(
        plan="none", expired_at=datetime.fromisoformat("0001-01-01T00:00:00Z")
    )
    assert membership.plan == "none"
    assert isinstance(membership.expired_at, datetime)


def test_app_model():
    """Test App model creation and validation."""
    app = App(
        type="app",
        app_id="test-app-id",
        app_number="7000103105",
        redirect_uri="https://example.com/auth",
        home_uri="https://example.com",
        name="Test App",
        icon_url="",
        description="Test Description",
        capabilities=["IMMERSIVE", "ENCRYPTED"],
        resource_patterns=["https://example.com"],
        category="OTHER",
        creator_id="test-creator-id",
        updated_at=datetime.fromisoformat("2025-01-03T08:43:16.360914164Z"),
        is_verified=False,
        tip_key_base64="",
        tip_counter=0,
        has_safe=False,
        spend_public_key="",
        safe_created_at=datetime.fromisoformat("0001-01-01T00:00:00Z"),
        app_secret="",
        session_public_key="",
        session_secret="",
        capabilites=["IMMERSIVE", "ENCRYPTED"],
    )
    assert app.type == "app"
    assert app.app_id == "test-app-id"
    assert isinstance(app.updated_at, datetime)


def test_user_model():
    """Test User model creation and validation."""
    user = User(
        type="user",
        user_id="test-user-id",
        identity_number="7000103105",
        phone="test-phone",
        full_name="Test User",
        biography="Test Bio",
        avatar_url="",
        relationship="ME",
        mute_until=datetime.fromisoformat("0001-01-01T00:00:00Z"),
        created_at=datetime.fromisoformat("2020-01-06T14:52:03.497887444Z"),
        is_verified=False,
        is_scam=False,
        is_deactivated=False,
        code_id="test-code-id",
        code_url="https://mixin.one/codes/test",
        features=None,
        has_safe=True,
        membership=Membership(
            plan="none", expired_at=datetime.fromisoformat("0001-01-01T00:00:00Z")
        ),
        email="test@mixin.id",
        app_id="test-app-id",
        app=App(
            type="app",
            app_id="test-app-id",
            app_number="7000103105",
            redirect_uri="https://example.com/auth",
            home_uri="https://example.com",
            name="Test App",
            icon_url="",
            description="Test Description",
            capabilities=["IMMERSIVE", "ENCRYPTED"],
            resource_patterns=["https://example.com"],
            category="OTHER",
            creator_id="test-creator-id",
            updated_at=datetime.fromisoformat("2025-01-03T08:43:16.360914164Z"),
            is_verified=False,
            tip_key_base64="",
            tip_counter=0,
            has_safe=False,
            spend_public_key="",
            safe_created_at=datetime.fromisoformat("0001-01-01T00:00:00Z"),
            app_secret="",
            session_public_key="",
            session_secret="",
            capabilites=["IMMERSIVE", "ENCRYPTED"],
        ),
        session_id="test-session-id",
        device_status="",
        has_pin=True,
        salt_exported_at=datetime.fromisoformat("0001-01-01T00:00:00Z"),
        receive_message_source="EVERYBODY",
        accept_conversation_source="EVERYBODY",
        accept_search_source="EVERYBODY",
        fiat_currency="USD",
        transfer_notification_threshold=0,
        transfer_confirmation_threshold=100,
        pin_token_base64="",
        pin_token="",
        salt_base64="",
        tip_key_base64="test-tip-key",
        tip_counter=1,
        spend_public_key="test-spend-key",
        has_emergency_contact=False,
    )
    assert user.type == "user"
    assert user.user_id == "test-user-id"
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.membership, Membership)
    assert isinstance(user.app, App)


def test_user_response_model():
    """Test UserResponse model creation and validation."""
    user = User(
        type="user",
        user_id="test-user-id",
        identity_number="7000103105",
        phone="test-phone",
        full_name="Test User",
        biography="Test Bio",
        avatar_url="",
        relationship="ME",
        mute_until=datetime.fromisoformat("0001-01-01T00:00:00Z"),
        created_at=datetime.fromisoformat("2020-01-06T14:52:03.497887444Z"),
        is_verified=False,
        is_scam=False,
        is_deactivated=False,
        code_id="test-code-id",
        code_url="https://mixin.one/codes/test",
        features=None,
        has_safe=True,
        membership=Membership(
            plan="none", expired_at=datetime.fromisoformat("0001-01-01T00:00:00Z")
        ),
        email="test@mixin.id",
        app_id="test-app-id",
        app=App(
            type="app",
            app_id="test-app-id",
            app_number="7000103105",
            redirect_uri="https://example.com/auth",
            home_uri="https://example.com",
            name="Test App",
            icon_url="",
            description="Test Description",
            capabilities=["IMMERSIVE", "ENCRYPTED"],
            resource_patterns=["https://example.com"],
            category="OTHER",
            creator_id="test-creator-id",
            updated_at=datetime.fromisoformat("2025-01-03T08:43:16.360914164Z"),
            is_verified=False,
            tip_key_base64="",
            tip_counter=0,
            has_safe=False,
            spend_public_key="",
            safe_created_at=datetime.fromisoformat("0001-01-01T00:00:00Z"),
            app_secret="",
            session_public_key="",
            session_secret="",
            capabilites=["IMMERSIVE", "ENCRYPTED"],
        ),
        session_id="test-session-id",
        device_status="",
        has_pin=True,
        salt_exported_at=datetime.fromisoformat("0001-01-01T00:00:00Z"),
        receive_message_source="EVERYBODY",
        accept_conversation_source="EVERYBODY",
        accept_search_source="EVERYBODY",
        fiat_currency="USD",
        transfer_notification_threshold=0,
        transfer_confirmation_threshold=100,
        pin_token_base64="",
        pin_token="",
        salt_base64="",
        tip_key_base64="test-tip-key",
        tip_counter=1,
        spend_public_key="test-spend-key",
        has_emergency_contact=False,
    )
    response = UserResponse(data=user)
    assert isinstance(response.data, User)
    assert response.data.user_id == "test-user-id"
