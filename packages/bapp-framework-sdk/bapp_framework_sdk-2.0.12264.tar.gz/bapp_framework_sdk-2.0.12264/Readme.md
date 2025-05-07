# Bapp Framework Python SDK

This is the Python SDK for the Bapp Framework. It provides a simple way to interact with the Bapp Framework API.

## Installation
To install the SDK, run the following command:
```bash
pip install bapp-framework-sdk
```

# Example
```python
from bapp_framework_sdk import BappFrameworkApiClient

client = BappFrameworkApiClient(token='your_token_here')
client.get_available_tasks()
```
