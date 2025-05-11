"""
Mixin Network Client
~~~~~~~~~~~~~~~~~~

This module provides the main client class for interacting with the Mixin Network.
"""

import uuid
from typing import Any, Optional

from .api.conversation import ConversationApi
from .api.message import MessageApi
from .api.user import UserApi
from .auth import encrypt_pin, generate_trace_id, generate_unique_id
from .config import MixinBotConfig
from .http import HttpRequest


class MixinClient:
    """Main client class for interacting with Mixin Network API."""

    class _ApiInterface:
        """Internal class for unified API access."""
        
        def __init__(self, client):
            """Initialize the API interface with references to all API instances.
            
            Args:
                client (MixinClient): The parent client instance.
            """
            self.user = client._user
            self.message = client._message
            self.conversation = client._conversation
            
            # High-frequency use methods
            self.send_message = self.message.send_message
            self.send_text_message = self.message.send_text_message
            self.get_me = self.user.get_me
            self.create_conversation = self.conversation.create_conversation

    def __init__(self, config: MixinBotConfig):
        """Initialize the Mixin client.

        Args:
            config (MixinBotConfig): Configuration object containing necessary credentials.
        """
        self.config = config
        self.http = HttpRequest(config)
        
        # Initialize API interfaces
        self._user = UserApi(self.http)
        self._message = MessageApi(self.http)
        self._conversation = ConversationApi(self.http)
        
        # Create the unified API interface
        self._api = self._ApiInterface(self)
        
    @property
    def api(self):
        """Access to all API interfaces.
        
        Returns:
            _ApiInterface: Unified API interface with access to all API methods.
        """
        return self._api
        
    def create_transfer(
        self,
        pin_code: str,
        asset_id: str,
        opponent_id: str,
        amount: float,
        memo: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a transfer to another user.

        Args:
            pin_code (str): The PIN code for the transfer.
            asset_id (str): The UUID of the asset to transfer.
            opponent_id (str): The UUID of the recipient.
            amount (float): The amount to transfer.
            memo (str, optional): A memo for the transfer. Max 140 characters.
            trace_id (str, optional): A UUID to trace the transfer.

        Returns:
            dict: The transfer response from the API.
        """
        if not trace_id:
            trace_id = str(uuid.uuid4())

        data = {
            "asset_id": asset_id,
            "opponent_id": opponent_id,
            "amount": str(amount),
            "trace_id": trace_id,
            "pin": encrypt_pin(pin_code, self.config.session_private_key),
        }
        if memo:
            data["memo"] = memo

        return self.http.post("/transfers", body=data)

    def get_asset(self, asset_id: str) -> dict[str, Any]:
        """Get asset information by ID.

        Args:
            asset_id (str): The ID of the asset to fetch.

        Returns:
            Dict[str, Any]: Asset information.

        Example:
            >>> client = MixinClient(config)
            >>> asset = client.get_asset("asset_id")
            >>> print(asset)
        """
        return self.http.get(f"/assets/{asset_id}")

    def get_assets(self) -> dict[str, Any]:
        """Get all assets for the current user.

        Returns:
            Dict[str, Any]: List of assets.

        Example:
            >>> client = MixinClient(config)
            >>> assets = client.get_assets()
            >>> print(assets)
        """
        return self.http.get("/assets")

    def get_snapshots(
        self, limit: int = 20, offset: Optional[str] = None
    ) -> dict[str, Any]:
        """Get transaction snapshots.

        Args:
            limit (int, optional): Number of snapshots to return. Defaults to 20.
            offset (Optional[str], optional): Offset for pagination. Defaults to None.

        Returns:
            Dict[str, Any]: List of snapshots.

        Example:
            >>> client = MixinClient(config)
            >>> snapshots = client.get_snapshots(limit=10)
            >>> print(snapshots)
        """
        params = {"limit": limit}
        if offset:
            params["offset"] = offset
        return self.http.get("/snapshots", params=params)

    def get_snapshot(self, snapshot_id: str) -> dict[str, Any]:
        """Get a specific transaction snapshot.

        Args:
            snapshot_id (str): The ID of the snapshot to fetch.

        Returns:
            Dict[str, Any]: Snapshot information.

        Example:
            >>> client = MixinClient(config)
            >>> snapshot = client.get_snapshot("snapshot_id")
            >>> print(snapshot)
        """
        return self.http.get(f"/snapshots/{snapshot_id}")

    def get_pending_deposits(self, asset_id: str) -> dict[str, Any]:
        """Get pending deposits for an asset.

        Args:
            asset_id (str): The ID of the asset.

        Returns:
            Dict[str, Any]: List of pending deposits.

        Example:
            >>> client = MixinClient(config)
            >>> deposits = client.get_pending_deposits("asset_id")
            >>> print(deposits)
        """
        return self.http.get(f"/assets/{asset_id}/deposits")

    def get_pending_withdrawals(self, asset_id: str) -> dict[str, Any]:
        """Get pending withdrawals for an asset.

        Args:
            asset_id (str): The ID of the asset.

        Returns:
            Dict[str, Any]: List of pending withdrawals.

        Example:
            >>> client = MixinClient(config)
            >>> withdrawals = client.get_pending_withdrawals("asset_id")
            >>> print(withdrawals)
        """
        return self.http.get(f"/assets/{asset_id}/withdrawals")

    def get_network_info(self) -> dict[str, Any]:
        """Get Mixin Network information.

        Returns:
            Dict[str, Any]: Network information.

        Example:
            >>> client = MixinClient(config)
            >>> network_info = client.get_network_info()
            >>> print(network_info)
        """
        return self.http.get("/network")

    def generate_trace_id(self, tx_hash: str) -> str:
        """Generate a trace ID from a transaction hash.

        Args:
            tx_hash (str): The transaction hash.

        Returns:
            str: The generated trace ID.
        """
        return generate_trace_id(tx_hash)

    def generate_unique_id(self, *uuids: str) -> str:
        """Generate a unique ID from multiple UUIDs.

        Args:
            *uuids: The UUIDs to combine.

        Returns:
            str: The generated unique ID.
        """
        return generate_unique_id(*uuids)
