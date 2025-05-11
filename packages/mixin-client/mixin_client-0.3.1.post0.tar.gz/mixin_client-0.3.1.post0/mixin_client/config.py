"""
Mixin Network Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides the configuration class for the Mixin Network client.
"""

import json
from typing import Any


class MixinBotConfig:
    """Configuration for Mixin Network bot client."""

    def __init__(
        self,
        app_id: str,
        session_id: str,
        server_public_key: str,
        session_private_key: str,
        api_host: str = "https://api.mixin.one",
    ):
        """Initialize the Mixin bot configuration.

        Args:
            app_id (str): Your Mixin Network app ID.
            session_id (str): Your Mixin Network session ID.
            server_public_key (str): Mixin Network server public key.
            session_private_key (str): Your session private key in hex format.
            api_host (str, optional): Mixin Network API host. Defaults to "https://api.mixin.one".
        """
        self.app_id = app_id
        self.session_id = session_id
        self.server_public_key = server_public_key
        self.session_private_key = session_private_key
        self.api_host = api_host
        self.private_key = bytes.fromhex(session_private_key)

    @staticmethod
    def from_payload(payload: dict[str, Any]) -> "MixinBotConfig":
        """Create a MixinBotConfig instance from a payload dictionary.

        Args:
            payload (Dict[str, Any]): A dictionary containing the configuration values.

        Returns:
            MixinBotConfig: A new MixinBotConfig instance.

        Example:
            >>> payload = {
            ...     "app_id": "your_app_id",
            ...     "session_id": "your_session_id",
            ...     "server_public_key": "your_server_public_key",
            ...     "session_private_key": "your_session_private_key"
            ... }
            >>> config = MixinBotConfig.from_payload(payload)
        """
        return MixinBotConfig(
            app_id=payload["app_id"],
            session_id=payload["session_id"],
            server_public_key=payload["server_public_key"],
            session_private_key=payload["session_private_key"],
            api_host=payload.get("api_host", "https://api.mixin.one"),
        )

    @staticmethod
    def from_file(file_path: str) -> "MixinBotConfig":
        """Create a MixinBotConfig instance from a JSON file.

        Args:
            file_path (str): Path to the JSON configuration file.

        Returns:
            MixinBotConfig: A new MixinBotConfig instance.

        Example:
            >>> config = MixinBotConfig.from_file("config.json")
        """
        with open(file_path) as f:
            payload = json.load(f)
        return MixinBotConfig.from_payload(payload)
