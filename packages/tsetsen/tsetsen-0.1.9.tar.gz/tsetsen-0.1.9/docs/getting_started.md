# Getting Started with Tsetsen Python SDK

This guide will walk you through the basics of using the Tsetsen Text-to-Speech Python SDK.

## Installation

Install the SDK using pip:

```bash
pip install tsetsen
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/tsetsen-ai/tsetsen-python-sdk.git
```

## Prerequisites

- Python 3.7 or later
- A Tsetsen API key (sign up at [tsetsen.ai](https://tsetsen.ai))

## API Key Setup

You have two options for providing your API key:

### Option 1: Pass the API key directly

```python
from tsetsen import Client

client = Client(api_key="your-api-key")
```

### Option 2: Set an environment variable

```bash
# Set the environment variable (replace with your actual API key)
export TSETSEN_API_KEY="your-api-key"
```

Then initialize the client without explicitly providing the API key:

```python
from tsetsen import Client

client = Client()  # Will use the TSETSEN_API_KEY environment variable
```

## Basic Usage

### Step 1: Initialize the Client

```python
from tsetsen import Client

client = Client(api_key="your-api-key")
```

### Step 2: List Available Voices

```python
# Get all available voices
voices_response = client.list_voices()

# Print voice details
for voice in voices_response.voices:
    print(f"ID: {voice.id}, Name: {voice.name}, Gender: {voice.gender.name}")
```

### Step 3: Generate Speech

```python
# Request speech generation
response = client.generate_speech(
    text="Hello, this is a text-to-speech test.",
    voice_id="voice-id"  # Use an ID from list_voices
)

# Store the request ID for status checking
request_id = response.request_id
print(f"Request ID: {request_id}")
```

### Step 4: Check Status and Get Audio URL

```python
# Wait for the request to complete
final_status = client.wait_for_completion(
    request_id=request_id,
    timeout=60  # Optional timeout in seconds
)

if final_status.status.name == "COMPLETED":
    print(f"Audio URL: {final_status.audio_url}")
    
    # Check metrics
    if final_status.metrics:
        print(f"Audio length: {final_status.metrics.audio_length} seconds")
        print(f"Credits used: {final_status.metrics.credits_used}")
else:
    print(f"Error: {final_status.error_message}")
```

### Step 5: Check User Balance

```python
# Get user credit balance
balance = client.get_user_balance()
print(f"Available credits: {balance.credits}")
```

### Step 6: Proper Resource Cleanup

Always close the client when you're done to free up resources:

```python
# Option 1: Using a context manager
with Client(api_key="your-api-key") as client:
    # Use client...
    pass  # Resources automatically released when the block exits

# Option 2: Manual close
client = Client(api_key="your-api-key")
try:
    # Use client...
    pass
finally:
    client.close()
```

## Error Handling

The SDK uses a rich exception hierarchy for proper error handling:

```python
from tsetsen import Client
from tsetsen.exceptions import ResourceNotFoundError, AuthenticationError

client = Client(api_key="your-api-key")

try:
    status = client.check_status(request_id="non-existent-id")
except ResourceNotFoundError as e:
    print(f"Request not found: {e}")
except AuthenticationError as e:
    print(f"Authentication error: {e}")
except Exception as e:
    print(f"Other error: {e}")
```

## Advanced Configuration

### Custom Endpoint

```python
client = Client(
    api_key="your-api-key",
    endpoint="api.custom-endpoint.example:50051"
)
```

### Custom Timeout

```python
client = Client(
    api_key="your-api-key",
    timeout=60.0  # 60 seconds
)
```

### Insecure Channel (Not Recommended for Production)

```python
client = Client(
    api_key="your-api-key",
    secure=False  # Disable TLS (use only for development)
)
```

### Custom Retry Configuration

```python
client = Client(
    api_key="your-api-key",
    max_retries=5  # Increase retry attempts
)
```

## Complete Example

Here's a complete example that ties everything together:

```python
import os
import time
from tsetsen import Client, RequestStatus
from tsetsen.exceptions import TsetsenError

# Get API key from environment
api_key = os.environ.get("TSETSEN_API_KEY")

try:
    # Initialize the client with context manager for automatic cleanup
    with Client(api_key=api_key) as client:
        # List available voices
        voices_response = client.list_voices(version="beta-v0.1")
        if not voices_response.voices:
            print("No voices available. Exiting.")
            exit(1)
            
        # Select the first voice
        selected_voice = voices_response.voices[0]
        print(f"Selected voice: {selected_voice.name} ({selected_voice.id})")
        
        # Check user balance
        balance = client.get_user_balance()
        print(f"Available credits: {balance.credits}")
        
        # Generate speech
        text = "Hello, this is a test of the Tsetsen Text-to-Speech API."
        response = client.generate_speech(
            text=text,
            voice_id=selected_voice.id,
            speed=1.0
        )
        request_id = response.request_id
        print(f"Generation request submitted. Request ID: {request_id}")
        
        # Wait for the request to complete
        final_status = client.wait_for_completion(
            request_id=request_id,
            timeout=60
        )
        
        # Handle the result
        if final_status.status == RequestStatus.COMPLETED:
            print(f"Audio URL: {final_status.audio_url}")
            
            if final_status.metrics:
                print(f"Audio length: {final_status.metrics.audio_length} seconds")
                print(f"Credits used: {final_status.metrics.credits_used}")
        else:
            print(f"Error: {final_status.error_message}")

except TsetsenError as e:
    print(f"Error: {e}")
```

## Next Steps

- Check the [API Reference](api_reference.md) for comprehensive documentation of all SDK features
- See the [examples](../examples) directory for more usage examples