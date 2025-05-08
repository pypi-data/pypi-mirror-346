# Tsetsen Python SDK API Reference

This document provides a complete reference for all public classes and methods in the Tsetsen TTS Python SDK.

## Client

The main client class for interacting with the Tsetsen TTS API.

```python
from tsetsen import Client
```

### Initialization

```python
client = Client(
    api_key: Optional[str] = None, 
    endpoint: Optional[str] = None,
    timeout: float = 30.0,
    secure: bool = True,
    max_retries: int = 3
)
```

- **api_key**: Your Tsetsen TTS API key. If not provided, will look for the `TSETSEN_API_KEY` environment variable.
- **endpoint**: The API endpoint to connect to. Defaults to `api.tsetsen.ai:50051`.
- **timeout**: Timeout in seconds for API requests. Defaults to 30 seconds.
- **secure**: Whether to use a secure gRPC channel. Defaults to True.
- **max_retries**: Maximum number of retries for failed requests. Defaults to 3.

### Methods

#### `list_voices`

List available voices for TTS.

```python
client.list_voices(
    version: Optional[str] = None,
    skip_cache: bool = False
) -> ListVoicesResponse
```

- **version**: Voice model version (e.g., "beta-v0.1", "beta-v0.2"). Defaults to "beta-v0.1" if not specified.
- **skip_cache**: Whether to skip cache and fetch fresh data. Defaults to False.

Returns a `ListVoicesResponse` object containing a list of available voices.

#### `generate_speech`

Generate speech from text.

```python
client.generate_speech(
    text: str,
    voice_id: str,
    speed: float = 1.0,
    version: str = "beta-v0.1"
) -> GenerateSpeechResponse
```

- **text**: The text to convert to speech.
- **voice_id**: The ID of the voice to use.
- **speed**: Speech speed multiplier. Defaults to 1.0.
- **version**: Voice model version. Defaults to "beta-v0.1".

Returns a `GenerateSpeechResponse` object containing the request ID and status.

#### `check_status`

Check the status of a speech generation request.

```python
client.check_status(
    request_id: str
) -> CheckStatusResponse
```

- **request_id**: The ID of the request to check.

Returns a `CheckStatusResponse` object containing the status and details.

#### `get_user_balance`

Get the user's credit balance.

```python
client.get_user_balance() -> GetUserBalanceResponse
```

Returns a `GetUserBalanceResponse` object containing the credit balance.

#### `wait_for_completion`

Wait for a speech generation request to complete.

```python
client.wait_for_completion(
    request_id: str,
    timeout: Optional[float] = None,
    poll_interval: float = 1.0
) -> CheckStatusResponse
```

- **request_id**: The ID of the request to wait for.
- **timeout**: Maximum time to wait in seconds. If None, wait indefinitely.
- **poll_interval**: Time between status checks in seconds. Defaults to 1 second.

Returns a `CheckStatusResponse` object containing the final status and details.

#### `close`

Close the client and release resources.

```python
client.close() -> None
```

This should be called when the client is no longer needed to free up resources.

## Models

### Request Models

#### `ListVoicesRequest`

Request model for listing available voices.

```python
ListVoicesRequest(
    api_key: str,
    version: Optional[str] = "beta-v0.1",
    skip_cache: bool = False
)
```

#### `GenerateSpeechRequest`

Request model for generating speech from text.

```python
GenerateSpeechRequest(
    api_key: str,
    text: str,
    voice_id: str,
    speed: float = 1.0,
    version: str = "beta-v0.1"
)
```

#### `CheckStatusRequest`

Request model for checking the status of a TTS request.

```python
CheckStatusRequest(
    api_key: str,
    request_id: str
)
```

#### `GetUserBalanceRequest`

Request model for getting user balance information.

```python
GetUserBalanceRequest(
    api_key: str
)
```

### Response Models

#### `Voice`

Model for a TTS voice.

```python
Voice(
    id: str,
    name: str,
    gender: Gender,
    language: str,
    preview_url: Optional[str] = None
)
```

#### `ListVoicesResponse`

Response model for listing available voices.

```python
ListVoicesResponse(
    voices: List[Voice]
)
```

#### `GenerateSpeechResponse`

Response model for generating speech from text.

```python
GenerateSpeechResponse(
    request_id: str,
    status: RequestStatus
)
```

#### `RequestMetrics`

Model for TTS request performance metrics.

```python
RequestMetrics(
    queue_time: Optional[int] = None,
    processing_time: Optional[int] = None,
    total_time: Optional[int] = None,
    audio_length: Optional[float] = None,
    credits_used: Optional[int] = None,
    character_count: Optional[int] = None
)
```

#### `CheckStatusResponse`

Response model for checking the status of a TTS request.

```python
CheckStatusResponse(
    request_id: str,
    status: RequestStatus,
    audio_url: Optional[str] = None,
    error_message: Optional[str] = None,
    metrics: Optional[RequestMetrics] = None
)
```

#### `GetUserBalanceResponse`

Response model for getting user balance information.

```python
GetUserBalanceResponse(
    credits: int
)
```

### Enums

#### `RequestStatus`

Enum for TTS request status.

```python
class RequestStatus(Enum):
    UNSPECIFIED = 0
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4
```

#### `Gender`

Enum for voice gender.

```python
class Gender(Enum):
    UNSPECIFIED = 0
    MALE = 1
    FEMALE = 2
```

## Exceptions

### `TsetsenError`

Base exception class for all Tsetsen TTS SDK exceptions.

```python
TsetsenError(
    message: str, 
    code: Optional[str] = None, 
    status_code: Optional[int] = None, 
    request_id: Optional[str] = None, 
    details: Optional[Dict[str, Any]] = None
)
```

### Specific Exception Types

- `AuthenticationError`: Raised when authentication fails due to invalid API key or credentials.
- `PermissionDeniedError`: Raised when the authenticated user doesn't have permission for the requested action.
- `InvalidRequestError`: Raised when the request contains invalid parameters or is malformed.
- `RateLimitExceededError`: Raised when the client has exceeded the rate limit for API requests.
- `InsufficientCreditsError`: Raised when the user doesn't have enough credits for the requested operation.
- `ResourceNotFoundError`: Raised when the requested resource (voice, request, etc.) does not exist.
- `ServiceUnavailableError`: Raised when the TTS service is temporarily unavailable.
- `ConnectionError`: Raised when there's a network error connecting to the API.
- `TimeoutError`: Raised when a request times out.
- `ServerError`: Raised when the server encounters an internal error.

## Utilities

### `retry`

Decorator that retries a function call if it raises specified exceptions.

```python
@retry(
    max_retries: int = 3,
    retry_exceptions: Optional[List[Type[Exception]]] = None,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    backoff_factor: float = 2.0,
    jitter: bool = True
)
```

- **max_retries**: Maximum number of retries before giving up.
- **retry_exceptions**: List of exception types that should trigger a retry.
- **base_delay**: Initial delay between retries in seconds.
- **max_delay**: Maximum delay between retries in seconds.
- **backoff_factor**: Factor by which the delay increases after each retry.
- **jitter**: Whether to add random jitter to the delay to prevent thundering herd.