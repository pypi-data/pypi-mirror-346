# Mixin Network Python Client

A Python client for interacting with the Mixin Network API.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

The client requires a configuration file in JSON format. You can use the example configuration file as a template:

```bash
cp examples/keystore.json.example keystore.json
```

Then edit `keystore.json` with your Mixin Network credentials:

```json
{
  "app_id": "your-app-id",
  "session_id": "your-session-id",
  "server_public_key": "your-server-public-key",
  "session_private_key": "your-session-private-key"
}
```

### Configuration Fields

- `app_id`: Your Mixin Network application ID (UUID format)
- `session_id`: Your Mixin Network session ID (UUID format)
- `server_public_key`: Mixin Network server public key (64 characters hex string)
- `session_private_key`: Your session private key (64 characters hex string)

## Usage

```python
from mixin_client import MixinClient, MixinBotConfig

# Load configuration from file
config = MixinBotConfig.from_file("keystore.json")

# Create client instance
client = MixinClient(config)

# Get user profile
user_info = client.me()
print(f"User ID: {user_info.get('user_id')}")
print(f"Full Name: {user_info.get('full_name')}")

# Get user assets
assets = client.assets()
for asset in assets.get("data", []):
    print(f"Asset: {asset.get('symbol')} - Balance: {asset.get('balance')}")
```

## Features

- User profile management
- Asset management
- Transfer functionality
- Real-time message handling via WebSocket
- JWT authentication
- Request/response error handling

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Linting

```bash
flake8
```

## License

MIT License 