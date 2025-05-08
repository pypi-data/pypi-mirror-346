"""
Retry utilities for the Tsetsen TTS Python SDK.

This module provides utilities for retrying failed API requests with
exponential backoff and jitter to handle transient failures gracefully.
"""
import time
import random
import logging
from functools import wraps
from typing import TypeVar, Callable, List, Type, Optional, Union, Any, Dict, cast

from tsetsen.exceptions import (
    ServiceUnavailableError,
    ConnectionError,
    TimeoutError,
    RateLimitExceededError,
    TsetsenError
)

# Set up logger
logger = logging.getLogger("tsetsen")

# Type variable for function return type
T = TypeVar('T')

# Default exceptions that should trigger a retry
DEFAULT_RETRY_EXCEPTIONS = (
    ServiceUnavailableError,
    ConnectionError,
    TimeoutError,
    RateLimitExceededError
)


def retry(
    max_retries: int = 3,
    retry_exceptions: Optional[List[Type[Exception]]] = None,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    backoff_factor: float = 2.0,
    jitter: bool = True
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that retries a function call if it raises specified exceptions.
    
    Args:
        max_retries: Maximum number of retries before giving up.
        retry_exceptions: List of exception types that should trigger a retry.
        base_delay: Initial delay between retries in seconds.
        max_delay: Maximum delay between retries in seconds.
        backoff_factor: Factor by which the delay increases after each retry.
        jitter: Whether to add random jitter to the delay to prevent thundering herd.
    
    Returns:
        A decorator function that will retry the decorated function according to the parameters.
    """
    if retry_exceptions is None:
        retry_exceptions = list(DEFAULT_RETRY_EXCEPTIONS)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            delay = base_delay
            
            for retry_count in range(max_retries + 1):
                try:
                    if retry_count > 0:
                        logger.debug(
                            f"Retrying {func.__name__} (attempt {retry_count} of {max_retries})"
                        )
                    
                    return func(*args, **kwargs)
                
                except Exception as e:
                    # Only retry if the exception is in the retry_exceptions list
                    if not any(isinstance(e, exc) for exc in retry_exceptions):
                        raise
                    
                    last_exception = e
                    
                    if retry_count == max_retries:
                        # We've exhausted our retries, re-raise the last exception
                        logger.warning(
                            f"Exceeded maximum retries ({max_retries}) for {func.__name__}"
                        )
                        raise
                    
                    # Calculate delay with exponential backoff
                    current_delay = min(delay * (backoff_factor ** retry_count), max_delay)
                    
                    # Add jitter if enabled (±20% of delay)
                    if jitter:
                        jitter_amount = current_delay * 0.2
                        current_delay = current_delay + random.uniform(-jitter_amount, jitter_amount)
                    
                    if isinstance(e, RateLimitExceededError):
                        logger.warning(
                            f"Rate limit exceeded, retrying after {current_delay:.2f} seconds"
                        )
                    else:
                        logger.debug(
                            f"Request failed with {type(e).__name__}, "
                            f"retrying after {current_delay:.2f} seconds"
                        )
                    
                    time.sleep(current_delay)
            
            # This line should never be reached due to the raising of last_exception above
            # but we need it for mypy
            assert last_exception is not None
            raise last_exception
        
        return wrapper
    
    return decorator