"""
Tsetsen TTS API Exceptions

This module defines the exception hierarchy used by the Tsetsen TTS Python SDK.
All exceptions inherit from TsetsenError, allowing users to catch all SDK-related
exceptions with a single except clause.
"""
from typing import Dict, Any, Optional, Union


class TsetsenError(Exception):
    """Base exception class for all Tsetsen TTS SDK exceptions."""
    
    def __init__(
        self, 
        message: str, 
        code: Optional[str] = None, 
        status_code: Optional[int] = None, 
        request_id: Optional[str] = None, 
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a new TsetsenError.
        
        Args:
            message: Human-readable error message
            code: Error code (e.g. 'authentication_failed')
            status_code: HTTP or gRPC status code
            request_id: Unique identifier for the request that failed
            details: Additional error details
        """
        self.message = message
        self.code = code
        self.status_code = status_code
        self.request_id = request_id
        self.details = details or {}
        
        # Create a detailed error message
        detailed_message = message
        if code:
            detailed_message = f"{code}: {detailed_message}"
        if request_id:
            detailed_message = f"{detailed_message} (Request ID: {request_id})"
            
        super().__init__(detailed_message)


class AuthenticationError(TsetsenError):
    """Raised when authentication fails due to invalid API key or credentials."""
    
    def __init__(
        self, 
        message: str = "Authentication failed. Please check your API key.",
        **kwargs
    ) -> None:
        super().__init__(message, code="authentication_failed", **kwargs)


class PermissionDeniedError(TsetsenError):
    """Raised when the authenticated user doesn't have permission for the requested action."""
    
    def __init__(
        self, 
        message: str = "Permission denied for the requested operation.",
        **kwargs
    ) -> None:
        super().__init__(message, code="permission_denied", **kwargs)


class InvalidRequestError(TsetsenError):
    """Raised when the request contains invalid parameters or is malformed."""
    
    def __init__(
        self, 
        message: str = "Invalid request parameters.",
        **kwargs
    ) -> None:
        super().__init__(message, code="invalid_request", **kwargs)


class RateLimitExceededError(TsetsenError):
    """Raised when the client has exceeded the rate limit for API requests."""
    
    def __init__(
        self, 
        message: str = "Rate limit exceeded. Please retry after some time.",
        **kwargs
    ) -> None:
        super().__init__(message, code="rate_limit_exceeded", **kwargs)


class InsufficientCreditsError(TsetsenError):
    """Raised when the user doesn't have enough credits for the requested operation."""
    
    def __init__(
        self, 
        message: str = "Insufficient credits to complete this operation.",
        **kwargs
    ) -> None:
        super().__init__(message, code="insufficient_credits", **kwargs)


class ResourceNotFoundError(TsetsenError):
    """Raised when the requested resource (voice, request, etc.) does not exist."""
    
    def __init__(
        self, 
        message: str = "The requested resource was not found.",
        **kwargs
    ) -> None:
        super().__init__(message, code="resource_not_found", **kwargs)


class ServiceUnavailableError(TsetsenError):
    """Raised when the TTS service is temporarily unavailable."""
    
    def __init__(
        self, 
        message: str = "Service is temporarily unavailable. Please try again later.",
        **kwargs
    ) -> None:
        super().__init__(message, code="service_unavailable", **kwargs)


class ConnectionError(TsetsenError):
    """Raised when there's a network error connecting to the API."""
    
    def __init__(
        self,
        message: str = "Failed to connect to the Tsetsen API. Please check your internet connection.",
        **kwargs
    ) -> None:
        super().__init__(message, code="connection_error", **kwargs)


class TimeoutError(TsetsenError):
    """Raised when a request times out."""
    
    def __init__(
        self,
        message: str = "Request timed out. Please try again later.",
        **kwargs
    ) -> None:
        super().__init__(message, code="timeout", **kwargs)


class ServerError(TsetsenError):
    """Raised when the server encounters an internal error."""
    
    def __init__(
        self,
        message: str = "Internal server error. Please contact support if this persists.",
        **kwargs
    ) -> None:
        super().__init__(message, code="server_error", **kwargs)


# Map gRPC status codes to exception classes
GRPC_STATUS_TO_EXCEPTION = {
    # Standard gRPC status codes: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    2: InvalidRequestError,    # UNKNOWN
    3: InvalidRequestError,    # INVALID_ARGUMENT
    4: TimeoutError,           # DEADLINE_EXCEEDED
    5: ResourceNotFoundError,  # NOT_FOUND
    6: ResourceNotFoundError,  # ALREADY_EXISTS
    7: PermissionDeniedError,  # PERMISSION_DENIED
    8: RateLimitExceededError, # RESOURCE_EXHAUSTED (rate limiting)
    16: AuthenticationError,   # UNAUTHENTICATED
    14: ServiceUnavailableError, # UNAVAILABLE
}