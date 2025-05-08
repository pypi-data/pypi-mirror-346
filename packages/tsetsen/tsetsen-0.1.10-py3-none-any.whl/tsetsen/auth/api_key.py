"""
API Key authentication for the Tsetsen TTS Python SDK.

This module handles API key validation and management for authenticating
with the Tsetsen TTS API.
"""
import os
import re
from typing import Optional, Dict, Any, Tuple, List

from tsetsen.exceptions import AuthenticationError


class ApiKeyManager:
    """Manages API keys for the Tsetsen TTS API."""
    
    # API key regex pattern (based on the API key format from the server code)
    API_KEY_PATTERN = r'^tsetsen-(prod|development)-[A-Za-z0-9_-]+$'
    
    # Environment variable name for the API key
    ENV_VAR_NAME = "TSETSEN_API_KEY"
    
    def __init__(
        self, 
        api_key: Optional[str] = None
    ) -> None:
        """
        Initialize the API key manager.
        
        Args:
            api_key: API key to use. If not provided, will look for the
                     TSETSEN_API_KEY environment variable.
        
        Raises:
            AuthenticationError: If no API key is found or the API key is invalid.
        """
        self.api_key = api_key or os.environ.get(self.ENV_VAR_NAME)
        if not self.api_key:
            raise AuthenticationError(
                "No API key provided. Please provide an API key or set the "
                f"{self.ENV_VAR_NAME} environment variable."
            )
        
        self.validate_api_key(self.api_key)
        # Store environment (prod or beta) from the API key
        self.environment = self._extract_environment(self.api_key)
    
    @classmethod
    def validate_api_key(cls, api_key: str) -> None:
        """
        Validate the format of an API key.
        
        Args:
            api_key: API key to validate.
            
        Raises:
            AuthenticationError: If the API key is not valid.
        """
        if not re.match(cls.API_KEY_PATTERN, api_key):
            raise AuthenticationError(
                "Invalid API key format. API keys should start with 'tsetsen-prod-' or 'tsetsen-beta-'."
            )
    
    @staticmethod
    def _extract_environment(api_key: str) -> str:
        """
        Extract the environment (prod or beta) from an API key.
        
        Args:
            api_key: API key to extract environment from.
            
        Returns:
            The environment string ('prod' or 'beta').
        """
        match = re.match(r'^tsetsen-(prod|beta)-', api_key)
        if match:
            return match.group(1)
        return "prod"  # Default to prod if we can't determine
    
    def get_auth_metadata(self) -> Dict[str, str]:
        """
        Get metadata for authenticating gRPC requests.
        
        Returns:
            Dictionary of metadata headers.
        """
        return {"x-api-key": self.api_key}
    
    def get_request_params(self) -> Dict[str, str]:
        """
        Get parameters for authenticating HTTP requests.
        
        Returns:
            Dictionary of request parameters.
        """
        return {"api_key": self.api_key}