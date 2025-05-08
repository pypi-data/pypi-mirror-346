"""
Tsetsen TTS API Request Models

This module defines the request models used by the Tsetsen TTS Python SDK.
These models provide type validation and enforce required parameters.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union


@dataclass
class BaseRequest:
    """Base class for all API request models."""
    
    api_key: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the request to a dictionary for API submission."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class ListVoicesRequest(BaseRequest):
    """Request model for listing available voices."""
    
    version: Optional[str] = "beta-v0.1"
    skip_cache: bool = False


@dataclass
class GenerateSpeechRequest(BaseRequest):
    """Request model for generating speech from text."""
    
    text: str
    voice_id: str
    speed: float = 1.0
    version: str = "beta-v0.1"
    
    def __post_init__(self) -> None:
        """Validate the request parameters."""
        if not self.text:
            raise ValueError("Text cannot be empty")
        if not self.voice_id:
            raise ValueError("Voice ID cannot be empty")
        if self.speed <= 0:
            raise ValueError("Speed must be positive")


@dataclass
class CheckStatusRequest(BaseRequest):
    """Request model for checking the status of a TTS request."""
    
    request_id: str
    
    def __post_init__(self) -> None:
        """Validate the request parameters."""
        if not self.request_id:
            raise ValueError("Request ID cannot be empty")


@dataclass
class GetUserBalanceRequest(BaseRequest):
    """Request model for getting user balance information."""
    pass  # No additional parameters needed beyond the API key