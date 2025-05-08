"""
Tsetsen TTS API Response Models

This module defines the response models used by the Tsetsen TTS Python SDK.
These models provide a structured way to access API responses.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from enum import Enum, auto


class RequestStatus(Enum):
    """Enum for TTS request status."""
    
    UNSPECIFIED = 0
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4
    
    @classmethod
    def from_grpc(cls, status_code: int) -> 'RequestStatus':
        """Convert a gRPC status code to a RequestStatus enum."""
        return cls(status_code)
    
    @classmethod
    def from_string(cls, status_string: str) -> 'RequestStatus':
        """Convert a status string to a RequestStatus enum."""
        status_map = {
            "UNSPECIFIED": cls.UNSPECIFIED,
            "PENDING": cls.PENDING,
            "PROCESSING": cls.PROCESSING,
            "COMPLETED": cls.COMPLETED,
            "FAILED": cls.FAILED
        }
        return status_map.get(status_string.upper(), cls.UNSPECIFIED)


class Gender(Enum):
    """Enum for voice gender."""
    
    UNSPECIFIED = 0
    MALE = 1
    FEMALE = 2
    
    @classmethod
    def from_grpc(cls, gender_code: int) -> 'Gender':
        """Convert a gRPC gender code to a Gender enum."""
        return cls(gender_code)
    
    @classmethod
    def from_string(cls, gender_string: str) -> 'Gender':
        """Convert a gender string to a Gender enum."""
        gender_map = {
            "UNSPECIFIED": cls.UNSPECIFIED,
            "MALE": cls.MALE,
            "FEMALE": cls.FEMALE
        }
        return gender_map.get(gender_string.upper(), cls.UNSPECIFIED)


@dataclass
class Voice:
    """Model for a TTS voice."""
    
    id: str
    name: str
    gender: Gender
    language: str
    preview_url: Optional[str] = None
    
    @classmethod
    def from_grpc(cls, grpc_voice: Any) -> 'Voice':
        """Create a Voice object from a gRPC voice response."""
        return cls(
            id=grpc_voice.id,
            name=grpc_voice.name,
            gender=Gender.from_grpc(grpc_voice.gender),
            language=grpc_voice.language,
            preview_url=grpc_voice.preview_url if grpc_voice.preview_url else None
        )
    
    @classmethod
    def from_dict(cls, voice_dict: Dict[str, Any]) -> 'Voice':
        """Create a Voice object from a dictionary."""
        return cls(
            id=voice_dict["id"],
            name=voice_dict["name"],
            gender=Gender.from_string(voice_dict.get("gender", "UNSPECIFIED")),
            language=voice_dict["language"],
            preview_url=voice_dict.get("preview_url")
        )


@dataclass
class ListVoicesResponse:
    """Response model for listing available voices."""
    
    voices: List[Voice]
    
    @classmethod
    def from_grpc(cls, grpc_response: Any) -> 'ListVoicesResponse':
        """Create a ListVoicesResponse object from a gRPC response."""
        return cls(
            voices=[Voice.from_grpc(voice) for voice in grpc_response.voices]
        )
    
    @classmethod
    def from_dict(cls, response_dict: Dict[str, Any]) -> 'ListVoicesResponse':
        """Create a ListVoicesResponse object from a dictionary."""
        return cls(
            voices=[Voice.from_dict(voice) for voice in response_dict.get("voices", [])]
        )


@dataclass
class GenerateSpeechResponse:
    """Response model for generating speech from text."""
    
    request_id: str
    status: RequestStatus
    
    @classmethod
    def from_grpc(cls, grpc_response: Any) -> 'GenerateSpeechResponse':
        """Create a GenerateSpeechResponse object from a gRPC response."""
        return cls(
            request_id=grpc_response.request_id,
            status=RequestStatus.from_grpc(grpc_response.status)
        )
    
    @classmethod
    def from_dict(cls, response_dict: Dict[str, Any]) -> 'GenerateSpeechResponse':
        """Create a GenerateSpeechResponse object from a dictionary."""
        return cls(
            request_id=response_dict["request_id"],
            status=RequestStatus.from_string(response_dict.get("status", "UNSPECIFIED"))
        )


@dataclass
class RequestMetrics:
    """Model for TTS request performance metrics."""
    
    queue_time: Optional[int] = None
    processing_time: Optional[int] = None
    total_time: Optional[int] = None
    audio_length: Optional[float] = None
    credits_used: Optional[int] = None
    character_count: Optional[int] = None
    
    @classmethod
    def from_grpc(cls, grpc_metrics: Any) -> 'RequestMetrics':
        """Create a RequestMetrics object from a gRPC metrics response."""
        if not grpc_metrics:
            return cls()
            
        return cls(
            queue_time=grpc_metrics.queue_time if hasattr(grpc_metrics, 'queue_time') else None,
            processing_time=grpc_metrics.processing_time if hasattr(grpc_metrics, 'processing_time') else None,
            total_time=grpc_metrics.total_time if hasattr(grpc_metrics, 'total_time') else None,
            audio_length=grpc_metrics.audio_length if hasattr(grpc_metrics, 'audio_length') else None,
            credits_used=grpc_metrics.credits_used if hasattr(grpc_metrics, 'credits_used') else None,
            character_count=grpc_metrics.character_count if hasattr(grpc_metrics, 'character_count') else None
        )
    
    @classmethod
    def from_dict(cls, metrics_dict: Dict[str, Any]) -> 'RequestMetrics':
        """Create a RequestMetrics object from a dictionary."""
        if not metrics_dict:
            return cls()
            
        return cls(
            queue_time=metrics_dict.get("queue_time"),
            processing_time=metrics_dict.get("processing_time"),
            total_time=metrics_dict.get("total_time"),
            audio_length=metrics_dict.get("audio_length"),
            credits_used=metrics_dict.get("credits_used"),
            character_count=metrics_dict.get("character_count")
        )


@dataclass
class CheckStatusResponse:
    """Response model for checking the status of a TTS request."""
    
    request_id: str
    status: RequestStatus
    audio_url: Optional[str] = None
    error_message: Optional[str] = None
    metrics: Optional[RequestMetrics] = None
    
    @classmethod
    def from_grpc(cls, grpc_response: Any) -> 'CheckStatusResponse':
        """Create a CheckStatusResponse object from a gRPC response."""
        return cls(
            request_id=grpc_response.request_id,
            status=RequestStatus.from_grpc(grpc_response.status),
            audio_url=grpc_response.audio_url if grpc_response.audio_url else None,
            error_message=grpc_response.error_message if grpc_response.error_message else None,
            metrics=RequestMetrics.from_grpc(grpc_response.metrics) if hasattr(grpc_response, 'metrics') else None
        )
    
    @classmethod
    def from_dict(cls, response_dict: Dict[str, Any]) -> 'CheckStatusResponse':
        """Create a CheckStatusResponse object from a dictionary."""
        return cls(
            request_id=response_dict["request_id"],
            status=RequestStatus.from_string(response_dict.get("status", "UNSPECIFIED")),
            audio_url=response_dict.get("audio_url"),
            error_message=response_dict.get("error_message"),
            metrics=RequestMetrics.from_dict(response_dict.get("metrics", {}))
        )


@dataclass
class GetUserBalanceResponse:
    """Response model for getting user balance information."""
    
    credits: int
    
    @classmethod
    def from_grpc(cls, grpc_response: Any) -> 'GetUserBalanceResponse':
        """Create a GetUserBalanceResponse object from a gRPC response."""
        return cls(
            credits=grpc_response.credits
        )
    
    @classmethod
    def from_dict(cls, response_dict: Dict[str, Any]) -> 'GetUserBalanceResponse':
        """Create a GetUserBalanceResponse object from a dictionary."""
        return cls(
            credits=response_dict["credits"]
        )