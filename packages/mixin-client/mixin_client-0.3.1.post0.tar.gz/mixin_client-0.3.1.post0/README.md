# Mixin Network Python Client

A Python client for interacting with the Mixin Network API.

## Installation

```bash
pip install mixin-client
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
user_info = client.get_me()
print(f"User ID: {user_info.data.user_id}")
print(f"Full Name: {user_info.data.full_name}")

# Get user assets
assets = client.get_assets()
for asset in assets.get("data", []):
    print(f"Asset: {asset.get('symbol')} - Balance: {asset.get('balance')}")
```

### API Structure

The client provides multiple ways to access the API:

1. **Direct client methods**:

```python
user_info = client.get_me()
client.send_text_message(conversation_id="conversation_id", content="Hello!")
```

2. **Using domain-specific API interfaces**:

```python
user_info = client.user.get_me()
client.message.send_text_message(conversation_id="conversation_id", content="Hello!")
client.conversation.create_conversation("user_id")
```

3. **Using the unified API interface**:

```python
user_info = client.api.user.get_me()
client.api.message.send_text_message(conversation_id="conversation_id", content="Hello!")
client.api.conversation.create_conversation("user_id")
```

### Messaging

The client supports message operations including sending messages, retrieving messages, and creating conversations.

```python
# Create a conversation
conversation = client.conversation.create_conversation("user-id")
conversation_id = conversation.get("data", {}).get("conversation_id")

# Send a text message
message = client.message.send_text_message(
    conversation_id=conversation_id,
    content="Hello from Mixin Python Client!"
)

# Send an image message
message = client.message.send_image_message(
    conversation_id=conversation_id,
    attachment_id="attachment_id",
    mime_type="image/jpeg",
    width=1024,
    height=768,
    size=1024000
)

# Get messages from a conversation
messages = client.message.get_messages(conversation_id, limit=10)
for msg in messages.data:
    print(f"[{msg.created_at}] {msg.user_id}: {msg.content}")

# Acknowledge a message
client.message.acknowledge_message(message.data.id)
```

For a complete example, see `examples/message_example.py`.

## Features

- User profile management
- Asset management
- Transfer functionality
- Messaging and conversation management
- Real-time message handling via WebSocket
- JWT authentication
- Request/response error handling
- Lazy loading of API components

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
