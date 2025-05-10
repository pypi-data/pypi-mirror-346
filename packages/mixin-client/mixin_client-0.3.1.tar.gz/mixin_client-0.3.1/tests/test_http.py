import httpx
import pytest

from mixin_client.config import MixinBotConfig
from mixin_client.http import (
    HttpRequest,
    RequestError,
    RequestTimeout,
    sign_authentication_token,
)


@pytest.fixture
def config():
    return MixinBotConfig(
        app_id="test-app-id",
        session_id="test-session-id",
        server_public_key="test-server-public-key",
        session_private_key="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        api_host="https://api.mixin.one",
    )


@pytest.fixture
def http_request(config):
    return HttpRequest(config)


def test_http_request_initialization(config):
    """测试 HttpRequest 初始化"""
    http_request = HttpRequest(config)
    assert http_request.config == config
    assert isinstance(http_request.session, httpx.Client)


def test_sign_authentication_token():
    """测试签名认证令牌生成"""
    user_id = "test-user-id"
    session_id = "test-session-id"
    private_key = bytes.fromhex(
        "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    )
    method = "GET"
    uri = "/users/me"

    token = sign_authentication_token(
        user_id=user_id,
        session_id=session_id,
        private_key=private_key,
        key_algorithm="eddsa",
        method=method,
        uri=uri,
    )

    assert isinstance(token, str)
    assert len(token) > 0


def test_get_request(http_request, mocker):
    """测试 GET 请求"""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}

    mocker.patch.object(http_request.session, "get", return_value=mock_response)

    response = http_request.get("/test")
    assert response == {"data": "test"}


def test_get_request_with_params(http_request, mocker):
    """测试带参数的 GET 请求"""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}

    mocker.patch.object(http_request.session, "get", return_value=mock_response)

    params = {"key": "value"}
    response = http_request.get("/test", query_params=params)
    assert response == {"data": "test"}


def test_post_request(http_request, mocker):
    """测试 POST 请求"""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}

    mocker.patch.object(http_request.session, "post", return_value=mock_response)

    body = {"test": "data"}
    response = http_request.post("/test", body=body)
    assert response == {"data": "test"}


def test_request_error(http_request, mocker):
    """测试请求错误处理"""
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "error": {"code": 400, "description": "Bad Request"}
    }
    mock_response.reason_phrase = "Bad Request"

    mocker.patch.object(http_request.session, "get", return_value=mock_response)

    with pytest.raises(RequestError) as exc_info:
        http_request.get("/test")

    assert exc_info.value.code == 400
    assert "Bad Request" in str(exc_info.value)


def test_request_timeout(http_request, mocker):
    """测试请求超时处理"""
    mocker.patch.object(
        http_request.session,
        "get",
        side_effect=httpx.ReadTimeout("Connection timed out"),
    )

    with pytest.raises(RequestTimeout) as exc_info:
        http_request.get("/test")

    assert exc_info.value.code == 408
    assert "Connection timed out" in str(exc_info.value)


def test_invalid_json_response(http_request, mocker):
    """测试无效 JSON 响应处理"""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")

    mocker.patch.object(http_request.session, "get", return_value=mock_response)

    response = http_request.get("/test")
    assert response == {}


def test_generate_headers(http_request):
    """测试请求头生成"""
    method = "GET"
    uri = "/users/me"
    body = ""

    headers = http_request._generate_headers(method, uri, body)

    assert "Authorization" in headers
    assert "X-Request-Id" in headers
    assert headers["Content-Type"] == "application/json"

    # 验证 Authorization 格式
    auth = headers["Authorization"]
    assert auth.startswith("Bearer ")


def test_request_signature(http_request):
    """测试请求签名生成"""
    method = "GET"
    uri = "/users/me"
    body = ""

    signature = http_request._generate_signature(method, uri, body)
    assert isinstance(signature, str)
    assert len(signature) > 0


def test_request_with_invalid_config():
    """测试使用无效配置初始化"""
    with pytest.raises(ValueError):
        HttpRequest(None)


def test_request_with_invalid_method(http_request):
    """测试使用无效的 HTTP 方法"""
    with pytest.raises(ValueError):
        http_request.request("INVALID", "/users/me")


def test_request_with_invalid_url(http_request):
    """测试使用无效的 URL"""
    with pytest.raises(ValueError):
        http_request.request("GET", "invalid-url")


def test_request_with_invalid_body(http_request):
    """测试使用无效的请求体"""
    with pytest.raises(ValueError):
        http_request.request("POST", "/users/me", body=123)  # 非字符串或字典类型
