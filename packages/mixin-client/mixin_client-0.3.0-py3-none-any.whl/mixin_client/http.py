"""
HTTP Request Handler
~~~~~~~~~~~~~~~~~~

This module provides the HTTP request handler for the Mixin Network client.
"""

import hashlib
import json
import time
import uuid
from typing import Any, Optional, Union

import httpx
import jwt
from cryptography.hazmat.primitives.asymmetric import ed25519

from .config import MixinBotConfig

# from .utils import generate_token


class RequestError(Exception):
    """Base exception for request errors."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Request failed with code {code}: {message}")


class RequestTimeoutError(RequestError):
    """Exception raised when a request times out."""

    def __init__(self, code: Optional[int], message: str):
        super().__init__(code or 408, message)


def sign_authentication_token(
    user_id: str,
    session_id: str,
    private_key: bytes,
    key_algorithm: str,
    method: str,
    uri: str,
    bodystring: Optional[str] = None,
    iat: Optional[int] = None,
    exp: Optional[int] = None,
    jti: Optional[str] = None,
) -> str:
    """Sign an authentication token for Mixin Network API.

    Args:
        user_id (str): The user ID.
        session_id (str): The session ID.
        private_key (bytes): The private key.
        key_algorithm (str): The key algorithm (rs512 or eddsa).
        method (str): The HTTP method.
        uri (str): The request URI.
        bodystring (str, optional): The request body string.
        iat (int, optional): Token issued at timestamp.
        exp (int, optional): Token expiration timestamp.
        jti (str, optional): Token ID.

    Returns:
        str: The signed JWT token.

    Raises:
        ValueError: If the key algorithm is not supported.
    """
    if key_algorithm.lower() in ["rs512", "rsa"]:
        alg = "RS512"
        key = private_key
    elif key_algorithm.lower() in ["eddsa", "ed25519"]:
        alg = "EdDSA"
        key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key[:32])
    else:
        raise ValueError(f"Unsupported key's algorithm: {key_algorithm}")

    jwt_headers = {
        "alg": alg,
        "typ": "JWT",
    }

    bodystring = bodystring if bodystring else ""
    hashresult = hashlib.sha256((method + uri + bodystring).encode("utf-8")).hexdigest()
    iat = int(time.time()) if iat is None else iat
    exp = iat + 600 if exp is None else exp
    jti = str(uuid.uuid4()) if jti is None else jti
    payload = {
        "uid": user_id,
        "sid": session_id,
        "iat": iat,
        "exp": exp,
        "jti": jti,
        "sig": hashresult,
        "scp": "FULL",
    }

    return jwt.encode(payload, key, algorithm=alg, headers=jwt_headers)


class HttpRequest:
    """HTTP request handler for Mixin Network API."""

    def __init__(self, config: MixinBotConfig):
        """Initialize the HTTP request handler.

        Args:
            config (MixinBotConfig): Configuration object containing necessary credentials.
        """
        self.config = config
        self.session = httpx.Client()

    def get(
        self,
        path: str,
        query_params: Optional[dict[str, Any]] = None,
        request_id: Optional[str] = None,
        timeout: int = 60,
    ) -> dict[str, Any]:
        """Make a GET request to the API.

        Args:
            path (str): The API endpoint to call.
            query_params (Dict[str, Any], optional): Query parameters for the request.
            request_id (str, optional): Request ID for tracking. If not provided, a UUID will be generated.
            timeout (int, optional): Request timeout in seconds. Defaults to 60.

        Returns:
            Dict[str, Any]: The JSON response from the API.

        Raises:
            RequestTimeout: If the request times out.
            RequestError: If the request fails or returns an error.
        """
        if query_params:
            params_string = "&".join(f"{k}={v}" for k, v in query_params.items())
            path = f"{path}?{params_string}"

        url = self.config.api_host + path
        headers = {"Content-Type": "application/json"}

        auth_token = sign_authentication_token(
            user_id=self.config.app_id,
            session_id=self.config.session_id,
            private_key=self.config.private_key,
            key_algorithm="eddsa",
            method="GET",
            uri=path,
        )
        if auth_token:
            headers["Authorization"] = "Bearer " + auth_token

        request_id = request_id if request_id else str(uuid.uuid4())
        headers["X-Request-Id"] = request_id

        try:
            r = self.session.get(url, headers=headers, timeout=timeout)
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.WriteTimeout) as e:
            raise RequestTimeoutError(None, str(e)) from None
        except Exception as e:
            raise RequestError(1, str(e)) from e

        try:
            body_json = r.json()
        except Exception:
            body_json = {}

        if r.status_code != 200:
            error = body_json.get("error", {})
            status_code = error.get("code", r.status_code)
            message = error.get("description", r.reason_phrase)
            raise RequestError(status_code, message)

        if "error" in body_json:
            error = body_json.get("error", {})
            status_code = error.get("code", r.status_code)
            message = error.get("description", r.reason_phrase)
            raise RequestError(status_code, message)

        return body_json

    def post(
        self,
        path: str,
        body: Union[dict[str, Any], list],
        query_params: Optional[dict[str, Any]] = None,
        request_id: Optional[str] = None,
        timeout: int = 60,
    ) -> dict[str, Any]:
        """Make a POST request to the API.

        Args:
            path (str): The API endpoint to call.
            body (Union[Dict[str, Any], list]): The request body.
            query_params (Dict[str, Any], optional): Query parameters for the request.
            request_id (str, optional): Request ID for tracking. If not provided, a UUID will be generated.
            timeout (int, optional): Request timeout in seconds. Defaults to 60.

        Returns:
            Dict[str, Any]: The JSON response from the API.

        Raises:
            RequestTimeout: If the request times out.
            RequestError: If the request fails or returns an error.
        """
        if query_params:
            params_string = "&".join(f"{k}={v}" for k, v in query_params.items())
            path = f"{path}?{params_string}"

        url = self.config.api_host + path
        headers = {"Content-Type": "application/json"}
        bodystring = json.dumps(body)

        auth_token = sign_authentication_token(
            user_id=self.config.app_id,
            session_id=self.config.session_id,
            private_key=self.config.private_key,
            key_algorithm="eddsa",
            method="POST",
            uri=path,
            bodystring=bodystring,
        )
        if auth_token:
            headers["Authorization"] = "Bearer " + auth_token

        request_id = request_id if request_id else str(uuid.uuid4())
        headers["X-Request-Id"] = request_id

        try:
            r = self.session.post(
                url, headers=headers, data=bodystring, timeout=timeout
            )
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.WriteTimeout) as e:
            raise RequestTimeoutError(None, str(e)) from None
        except Exception as e:
            raise RequestError(1, str(e)) from e

        try:
            body_json = r.json()
        except Exception:
            body_json = {}

        if r.status_code != 200:
            error = body_json.get("error", {})
            status_code = error.get("code", r.status_code)
            message = error.get("description", r.reason_phrase)
            raise RequestError(status_code, message)

        if "error" in body_json:
            error = body_json.get("error", {})
            status_code = error.get("code", r.status_code)
            message = error.get("description", r.reason_phrase)
            raise RequestError(status_code, message)

        return body_json
