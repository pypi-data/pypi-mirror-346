"""
Test cases for the Mixin client.
"""

from mixin_client import MixinBotConfig, MixinClient


def test_client_initialization():
    """Test that the client can be initialized."""
    config = MixinBotConfig(
        app_id="test-app-id",
        session_id="test-session-id",
        server_public_key="test-server-key",
        session_private_key="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    )
    client = MixinClient(config)
    assert isinstance(client, MixinClient)
    assert client.config == config


def test_client_with_config():
    """Test that the client can be initialized with a config object."""
    config = MixinBotConfig(
        app_id="test-app-id",
        session_id="test-session-id",
        server_public_key="test-server-key",
        session_private_key="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    )
    client = MixinClient(config)
    assert isinstance(client, MixinClient)
    assert client.config.app_id == "test-app-id"
    assert client.config.session_id == "test-session-id"
