# Mixin Network Client

A Python client for interacting with the Mixin Network API.

## Installation

You can install the package using pip:

```bash
pip install mixin-client
```

## Usage

```python
from mixin_client import MixinClient

# Initialize the client
client = MixinClient(api_key="your_api_key", api_secret="your_api_secret")

# Make API requests
response = client._make_request("GET", "/endpoint")
```

## Features

- Simple and intuitive API
- Full support for Mixin Network API endpoints
- Type hints for better IDE support
- Comprehensive error handling

## Requirements

- Python 3.9 or higher
- requests >= 2.25.1

## License

This project is licensed under the MIT License - see the LICENSE file for details. 