"""
Tsetsen TTS - Python SDK for Text-to-Speech API

A client library for the Tsetsen Text-to-Speech API, providing a simple
interface for generating high-quality speech from text.

Basic usage:
    from tsetsen import Client
    
    client = Client(api_key="your-api-key")
    
    # List available voices
    voices = client.list_voices()
    
    # Generate speech
    response = client.generate_speech(text="Hello, world!", voice_id="voice-id")
    
    # Check status until complete
    status = client.check_status(request_id=response.request_id)
    
    # Get the audio URL when complete
    if status.status == RequestStatus.COMPLETED:
        print(f"Audio URL: {status.audio_url}")
"""
from tsetsen.client import Client
from tsetsen.exceptions import (
    TsetsenError,
    AuthenticationError,
    PermissionDeniedError,
    InvalidRequestError,
    RateLimitExceededError,
    InsufficientCreditsError,
    ResourceNotFoundError,
    ServiceUnavailableError,
    ConnectionError,
    TimeoutError,
    ServerError
)
from tsetsen.models.responses import (
    RequestStatus,
    Gender,
    Voice,
    ListVoicesResponse,
    GenerateSpeechResponse,
    RequestMetrics,
    CheckStatusResponse,
    GetUserBalanceResponse
)

__version__ = "0.1.1"
__all__ = [
    "Client",
    "TsetsenError",
    "AuthenticationError",
    "PermissionDeniedError",
    "InvalidRequestError",
    "RateLimitExceededError",
    "InsufficientCreditsError",
    "ResourceNotFoundError",
    "ServiceUnavailableError",
    "ConnectionError",
    "TimeoutError",
    "ServerError",
    "RequestStatus",
    "Gender",
    "Voice",
    "ListVoicesResponse",
    "GenerateSpeechResponse",
    "RequestMetrics",
    "CheckStatusResponse",
    "GetUserBalanceResponse"
]