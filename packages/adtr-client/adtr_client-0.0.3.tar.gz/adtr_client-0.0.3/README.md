# Adtr Translation Client

A simple Python client for the [Adtr Translation API](https://adtr.webnova.one/docs).

## Installation

Install the client using pip:

```bash
pip install adtr_client
```

## Usage

Use the client to translate text via the Adtr Translation API.

Example:

```python
from adtr_client import translate

result = translate(
    user_id="your_user_id",
    api_key="your_api_key",
    text="text to translate",
    target_language="target_language"
)

print(result)
```

## Configuration

1. Obtain your `user_id` and `api_key` from the rkn.name service
2. Replace `"your_user_id"`, `"your_api_key"`, and other parameters in the example above with your credentials and desired values.

```

