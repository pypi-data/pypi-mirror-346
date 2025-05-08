"""Tests for the MixinClient class."""

import pytest
from mixin_client import MixinClient


def test_client_initialization():
    """Test that the client can be initialized."""
    client = MixinClient()
    assert client.api_key is None
    assert client.api_secret is None
    assert client.base_url == "https://api.mixin.one"


def test_client_with_credentials():
    """Test that the client can be initialized with credentials."""
    client = MixinClient(api_key="test_key", api_secret="test_secret")
    assert client.api_key == "test_key"
    assert client.api_secret == "test_secret" 