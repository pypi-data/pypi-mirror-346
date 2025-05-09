"""
Mixin Network Client
~~~~~~~~~~~~~~~~~~

This module provides the main client class for interacting with the Mixin Network.
"""

import json
import uuid
from typing import Any, Dict, Optional, Union

import requests
import websockets

from .auth import encrypt_pin, generate_token, generate_trace_id, generate_unique_id
from .config import MixinBotConfig
from .http import HttpRequest
from .models import UserResponse


class MixinClient:
    """Main client class for interacting with Mixin Network API."""

    def __init__(self, config: MixinBotConfig):
        """Initialize the Mixin client.

        Args:
            config (MixinBotConfig): Configuration object containing necessary credentials.
        """
        self.config = config
        self.http = HttpRequest(config)

    def get_me(self) -> UserResponse:
        """Get the current user's profile.

        Returns:
            UserResponse: User profile information.

        Example:
            >>> client = MixinClient(config)
            >>> profile = client.get_me()
            >>> print(profile.data.full_name)
        """
        response = self.http.get("/me")
        return UserResponse(**response)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get a user's profile by ID.

        Args:
            user_id (str): The ID of the user to fetch.

        Returns:
            Dict[str, Any]: User profile information.

        Example:
            >>> client = MixinClient(config)
            >>> user = client.get_user("user_id")
            >>> print(user)
        """
        return self.http.get(f"/users/{user_id}")

    def get_asset(self, asset_id: str) -> Dict[str, Any]:
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

    def get_assets(self) -> Dict[str, Any]:
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
    ) -> Dict[str, Any]:
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

    def get_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
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

    def get_pending_deposits(self, asset_id: str) -> Dict[str, Any]:
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

    def get_pending_withdrawals(self, asset_id: str) -> Dict[str, Any]:
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

    def get_network_info(self) -> Dict[str, Any]:
        """Get Mixin Network information.

        Returns:
            Dict[str, Any]: Network information.

        Example:
            >>> client = MixinClient(config)
            >>> network_info = client.get_network_info()
            >>> print(network_info)
        """
        return self.http.get("/network")

    def create_transfer(
        self,
        pin_code: str,
        asset_id: str,
        opponent_id: str,
        amount: float,
        memo: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
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

        return self.http.post("/transfers", json=data)

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
