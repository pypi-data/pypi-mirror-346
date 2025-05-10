"""
Authentication and encryption utilities for Mixin Network.
"""

import base64
import hashlib
import json
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_token(
    app_id: str,
    client_secret: str,
    session_id: str,
    server_public_key: str,
    session_private_key: str,
) -> str:
    """Generate an authentication token for API requests.

    Args:
        app_id (str): The Mixin Network app ID.
        client_secret (str): The Mixin Network client secret.
        session_id (str): The Mixin Network session ID.
        server_public_key (str): The Mixin Network server public key.
        session_private_key (str): The session private key.

    Returns:
        str: The generated authentication token.
    """
    # Create the authentication payload
    payload = {
        "uid": app_id,
        "sid": session_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,  # Token expires in 1 hour
        "jti": str(int(time.time() * 1000)),
    }

    # Convert the payload to a JSON string
    payload_str = json.dumps(payload)

    # Load the server's public key
    server_key = serialization.load_pem_public_key(
        f"-----BEGIN PUBLIC KEY-----\n{server_public_key}\n-----END PUBLIC KEY-----".encode()
    )

    # Encrypt the payload with the server's public key
    encrypted = server_key.encrypt(
        payload_str.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Create the authentication token
    return base64.b64encode(encrypted).decode()


def encrypt_pin(pin: str, private_key: str) -> str:
    """Encrypt a PIN code using the private key.

    Args:
        pin (str): The PIN code to encrypt.
        private_key (str): The private key to use for encryption.

    Returns:
        str: The encrypted PIN code.
    """
    # Load the private key
    key = serialization.load_pem_private_key(
        f"-----BEGIN PRIVATE KEY-----\n{private_key}\n-----END PRIVATE KEY-----".encode(),
        password=None,
    )

    # Create a random initialization vector
    iv = b"\x00" * 16

    # Create a cipher
    cipher = Cipher(
        algorithms.AES(
            key.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
        ),
        modes.CBC(iv),
    )

    # Encrypt the PIN
    encryptor = cipher.encryptor()
    padded_pin = pin.encode() + b"\x00" * (16 - len(pin.encode()) % 16)
    encrypted = encryptor.update(padded_pin) + encryptor.finalize()

    return base64.b64encode(encrypted).decode()


def generate_trace_id(tx_hash: str) -> str:
    """Generate a trace ID from a transaction hash.

    Args:
        tx_hash (str): The transaction hash.

    Returns:
        str: The generated trace ID.
    """
    # Create a hash of the transaction hash
    hash_obj = hashlib.sha256(tx_hash.encode())
    return hash_obj.hexdigest()


def generate_unique_id(*uuids: str) -> str:
    """Generate a unique ID from multiple UUIDs.

    Args:
        *uuids: The UUIDs to combine.

    Returns:
        str: The generated unique ID.
    """
    # Sort the UUIDs to ensure consistent ordering
    sorted_uuids = sorted(uuids)

    # Create a hash of the combined UUIDs
    hash_obj = hashlib.sha256("".join(sorted_uuids).encode())
    return hash_obj.hexdigest()
