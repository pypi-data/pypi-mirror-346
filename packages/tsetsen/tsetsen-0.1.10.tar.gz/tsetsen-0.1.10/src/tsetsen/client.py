"""
Tsetsen TTS Python SDK Client

This module provides the main client class for interacting with the Tsetsen TTS API.
"""

import os
import time
import logging
import grpc
from typing import Optional, List, Dict, Any, Union, Tuple, cast, Iterator, Callable
from concurrent.futures import ThreadPoolExecutor

from tsetsen.auth.api_key import ApiKeyManager
from tsetsen.models.requests import (
    ListVoicesRequest,
    GenerateSpeechRequest,
    CheckStatusRequest,
    GetUserBalanceRequest,
)
from tsetsen.models.responses import (
    Voice,
    ListVoicesResponse,
    GenerateSpeechResponse,
    CheckStatusResponse,
    GetUserBalanceResponse,
    RequestStatus,
)
from tsetsen.exceptions import (
    TsetsenError,
    AuthenticationError,
    ServiceUnavailableError,
    ConnectionError,
    ResourceNotFoundError,
    GRPC_STATUS_TO_EXCEPTION,
)
from tsetsen.utils.retry import retry

# Import the generated gRPC code
try:
    # Try direct imports for newer protobuf
    from . import tsetsen_tts_pb2 as pb2
    from . import tsetsen_tts_pb2_grpc as pb2_grpc
except ImportError as e:
    if "runtime_version" in str(e):
        # Fix for newer protobuf versions that generate code with runtime_version
        # Manually modify the generated code to remove the runtime version check
        import os
        import re

        pb2_path = os.path.join(os.path.dirname(__file__), "tsetsen_tts_pb2.py")
        if os.path.exists(pb2_path):
            with open(pb2_path, "r") as f:
                content = f.read()

            # Remove the runtime version imports and checks
            content = re.sub(
                r"from google\.protobuf import runtime_version.*?\n", "", content
            )
            content = re.sub(
                r"_runtime_version\.ValidateProtobufRuntimeVersion.*?\n", "", content
            )

            with open(pb2_path, "w") as f:
                f.write(content)

            # Try importing again after fixes
            from . import tsetsen_tts_pb2 as pb2
            from . import tsetsen_tts_pb2_grpc as pb2_grpc
        else:
            raise ImportError(
                "Generated protobuf files not found. Run script/generate_grpc.py first."
            )
    else:
        raise ImportError(
            "The gRPC code for the Tsetsen TTS API has not been generated. "
            "Please run `python -m grpc_tools.protoc -I./protos --python_out=./src/tsetsen "
            "--grpc_python_out=./src/tsetsen ./protos/tsetsen_tts.proto` to generate the required files."
        )

# Set up logger
logger = logging.getLogger("tsetsen")


class Client:
    """
    Client for the Tsetsen TTS API.

    This client provides methods for interacting with the Tsetsen Text-to-Speech API,
    including voice listing, speech generation, and status checking.
    """

    # Default API endpoint
    DEFAULT_ENDPOINT = "tsetsen-grpc-server-103705352206.us-central1.run.app"

    # Maximum number of workers for async operations
    MAX_WORKERS = 5

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        timeout: float = 30.0,
        secure: bool = True,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the Tsetsen TTS client.

        Args:
            api_key: Your Tsetsen TTS API key. If not provided, will look for the
                     TSETSEN_API_KEY environment variable.
            endpoint: The API endpoint to connect to. Defaults to api.tsetsen.ai:50051.
            timeout: Timeout in seconds for API requests. Defaults to 30 seconds.
            secure: Whether to use a secure gRPC channel. Defaults to True.
            max_retries: Maximum number of retries for failed requests. Defaults to 3.

        Raises:
            AuthenticationError: If no API key is found or the API key is invalid.
        """
        # Set up API key manager
        self.auth = ApiKeyManager(api_key)

        # Set up endpoint and timeout
        self.endpoint = endpoint or os.environ.get(
            "TSETSEN_API_ENDPOINT", self.DEFAULT_ENDPOINT
        )
        self.timeout = timeout
        self.max_retries = max_retries

        # Set up gRPC channel and stub
        if secure:
            creds = grpc.ssl_channel_credentials()
            self.channel = grpc.secure_channel(self.endpoint, creds)
        else:
            self.channel = grpc.insecure_channel(self.endpoint)

        self.stub = pb2_grpc.TsetsenTTSStub(self.channel)

        # Set up thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

        logger.debug(f"Initialized Tsetsen client with endpoint {self.endpoint}")

    def close(self) -> None:
        """
        Close the client and release resources.

        This should be called when the client is no longer needed to free up resources.
        """
        self.channel.close()
        self.executor.shutdown()
        logger.debug("Closed Tsetsen client")

    def __enter__(self) -> "Client":
        """Context manager entry point."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit point."""
        self.close()

    @retry(max_retries=3)
    def list_voices(
        self, version: Optional[str] = None, skip_cache: bool = False
    ) -> ListVoicesResponse:
        """
        List available voices for TTS.

        Args:
            version: Voice model version (e.g., "beta-v0.1", "beta-v0.2").
                    Defaults to "beta-v0.1" if not specified.
            skip_cache: Whether to skip cache and fetch fresh data.
                        Defaults to False.

        Returns:
            A ListVoicesResponse object containing a list of available voices.

        Raises:
            AuthenticationError: If authentication fails.
            ServiceUnavailableError: If the service is unavailable.
            TsetsenError: For other API errors.
        """
        logger.debug("Listing voices...")

        # Create request
        request = ListVoicesRequest(
            api_key=self.auth.api_key, version=version, skip_cache=skip_cache
        )

        try:
            # Convert to gRPC request
            grpc_request = pb2.ListVoicesRequest(
                api_key=request.api_key,
                version=request.version if request.version else "",
                skip_cache=request.skip_cache,
            )

            # Make gRPC call
            metadata = [
                ("x-api-key", self.auth.api_key),
                ("x-goog-api-key", self.auth.api_key),
            ]
            grpc_response = self.stub.ListVoices(
                grpc_request, metadata=metadata, timeout=self.timeout
            )

            # Convert to response model
            response = ListVoicesResponse.from_grpc(grpc_response)
            logger.debug(f"Listed {len(response.voices)} voices")
            return response

        except grpc.RpcError as e:
            self._handle_grpc_error(e, "Error listing voices")

    @retry(max_retries=3)
    def generate_speech(
        self, text: str, voice_id: str, speed: float = 1.0, version: str = "beta-v0.1"
    ) -> GenerateSpeechResponse:
        """
        Generate speech from text.

        Args:
            text: The text to convert to speech.
            voice_id: The ID of the voice to use.
            speed: Speech speed multiplier. Defaults to 1.0.
            version: Voice model version. Defaults to "beta-v0.1".

        Returns:
            A GenerateSpeechResponse object containing the request ID and status.

        Raises:
            InvalidRequestError: If the request parameters are invalid.
            AuthenticationError: If authentication fails.
            ServiceUnavailableError: If the service is unavailable.
            TsetsenError: For other API errors.
        """
        logger.debug(
            f"Generating speech for text ({len(text)} chars) with voice {voice_id}..."
        )

        # Create request
        request = GenerateSpeechRequest(
            api_key=self.auth.api_key,
            text=text,
            voice_id=voice_id,
            speed=speed,
            version=version,
        )

        try:
            # Convert to gRPC request
            grpc_request = pb2.GenerateSpeechRequest(
                api_key=request.api_key,
                text=request.text,
                voice_id=request.voice_id,
                speed=request.speed,
                version=request.version,
            )

            # Make gRPC call
            metadata = [
                ("x-api-key", self.auth.api_key),
                ("x-goog-api-key", self.auth.api_key),
            ]
            grpc_response = self.stub.GenerateSpeech(
                grpc_request, metadata=metadata, timeout=self.timeout
            )

            # Convert to response model
            response = GenerateSpeechResponse.from_grpc(grpc_response)
            logger.debug(f"Generated speech request ID: {response.request_id}")
            return response

        except grpc.RpcError as e:
            self._handle_grpc_error(e, "Error generating speech")

    @retry(max_retries=3)
    def check_status(self, request_id: str) -> CheckStatusResponse:
        """
        Check the status of a speech generation request.

        Args:
            request_id: The ID of the request to check.

        Returns:
            A CheckStatusResponse object containing the status and details.

        Raises:
            ResourceNotFoundError: If the request ID is not found.
            AuthenticationError: If authentication fails.
            ServiceUnavailableError: If the service is unavailable.
            TsetsenError: For other API errors.
        """
        logger.debug(f"Checking status for request {request_id}...")

        # Create request
        request = CheckStatusRequest(api_key=self.auth.api_key, request_id=request_id)

        try:
            # Convert to gRPC request
            grpc_request = pb2.CheckStatusRequest(
                api_key=request.api_key, request_id=request.request_id
            )

            # Make gRPC call
            metadata = [
                ("x-api-key", self.auth.api_key),
                ("x-goog-api-key", self.auth.api_key),
            ]
            grpc_response = self.stub.CheckStatus(
                grpc_request, metadata=metadata, timeout=self.timeout
            )

            # Convert to response model
            response = CheckStatusResponse.from_grpc(grpc_response)
            logger.debug(f"Status for request {request_id}: {response.status.name}")
            return response

        except grpc.RpcError as e:
            self._handle_grpc_error(
                e, f"Error checking status for request {request_id}"
            )

    @retry(max_retries=3)
    def get_user_balance(self) -> GetUserBalanceResponse:
        """
        Get the user's credit balance.

        Returns:
            A GetUserBalanceResponse object containing the credit balance.

        Raises:
            AuthenticationError: If authentication fails.
            ServiceUnavailableError: If the service is unavailable.
            TsetsenError: For other API errors.
        """
        logger.debug("Getting user balance...")

        # Create request
        request = GetUserBalanceRequest(api_key=self.auth.api_key)

        try:
            # Convert to gRPC request
            grpc_request = pb2.GetUserBalanceRequest(api_key=request.api_key)

            # Make gRPC call
            metadata = [
                ("x-api-key", self.auth.api_key),
                ("x-goog-api-key", self.auth.api_key),
            ]
            grpc_response = self.stub.GetUserBalance(
                grpc_request, metadata=metadata, timeout=self.timeout
            )

            # Convert to response model
            response = GetUserBalanceResponse.from_grpc(grpc_response)
            logger.debug(f"User has {response.credits} credits")
            return response

        except grpc.RpcError as e:
            self._handle_grpc_error(e, "Error getting user balance")

    def wait_for_completion(
        self,
        request_id: str,
        timeout: Optional[float] = None,
        poll_interval: float = 1.0,
    ) -> CheckStatusResponse:
        """
        Wait for a speech generation request to complete.

        Args:
            request_id: The ID of the request to wait for.
            timeout: Maximum time to wait in seconds. If None, wait indefinitely.
            poll_interval: Time between status checks in seconds. Defaults to 1 second.

        Returns:
            A CheckStatusResponse object containing the final status and details.

        Raises:
            TimeoutError: If the request does not complete within the timeout.
            ResourceNotFoundError: If the request ID is not found.
            AuthenticationError: If authentication fails.
            ServiceUnavailableError: If the service is unavailable.
            TsetsenError: For other API errors.
        """
        logger.debug(f"Waiting for request {request_id} to complete...")

        start_time = time.time()

        while True:
            # Check if timeout has been exceeded
            if timeout is not None and time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Request {request_id} did not complete within {timeout} seconds"
                )

            # Check status
            response = self.check_status(request_id)

            # If completed or failed, return the response
            if response.status in [RequestStatus.COMPLETED, RequestStatus.FAILED]:
                return response

            # Wait before next check
            time.sleep(poll_interval)

    def _handle_grpc_error(self, error: grpc.RpcError, message: str) -> None:
        """
        Handle a gRPC error by converting it to an appropriate Tsetsen exception.

        Args:
            error: The gRPC error to handle.
            message: A message to prepend to the error message.

        Raises:
            An appropriate TsetsenError subclass based on the gRPC status code.
        """
        status_code = error.code()

        # Get details from error
        details = {}
        for key, value in error.trailing_metadata() or []:
            details[key] = value

        # Convert gRPC status code to Tsetsen exception
        exception_class = GRPC_STATUS_TO_EXCEPTION.get(
            status_code.value[0], TsetsenError
        )

        # Create and raise the exception
        raise exception_class(
            message=f"{message}: {error.details()}",
            status_code=status_code.value[0],
            details=details,
        )

    @retry(max_retries=3)
    def stream_speech(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        callback: Optional[Callable[[bytes, bool, Optional[str]], None]] = None,
    ) -> Iterator[bytes]:
        """
        Stream speech generation from text with real-time audio chunks.

        This method allows for real-time streaming of audio as it's being generated,
        which is useful for applications requiring low latency.

        Note:
            - Only works with version "beta-v0.2" model voices
            - Limited to 5 minutes of audio per request
            - Rate limited to 1 request per minute for free tier users
            - Audio output is 24,000Hz, 16-bit, mono

        Args:
            text: The text to convert to speech.
            voice_id: The ID of the voice to use.
            speed: Speech speed multiplier. Defaults to 1.0.
            callback: Optional callback function that will be called for each chunk.
                    The callback receives (audio_chunk, is_final, error_message)

        Returns:
            An iterator that yields audio chunks as they are received

        Raises:
            InvalidRequestError: If the request parameters are invalid.
            AuthenticationError: If authentication fails.
            ServiceUnavailableError: If the service is unavailable.
            RateLimitExceededError: If rate limits are exceeded.
            TsetsenError: For other API errors.
        """
        logger.debug(
            f"Streaming speech for text ({len(text)} chars) with voice {voice_id}..."
        )

        # Create request
        request = {
            "api_key": self.auth.api_key,
            "text": text,
            "voice_id": voice_id,
            "speed": speed,
            "version": "beta-v0.2",  # Streaming only works with beta-v0.2
        }

        try:
            # Convert to gRPC request
            grpc_request = pb2.StreamSpeechRequest(
                api_key=request["api_key"],
                text=request["text"],
                voice_id=request["voice_id"],
                speed=request["speed"],
                version=request["version"],
            )

            # Make gRPC call
            metadata = [
                ("x-api-key", self.auth.api_key),
                ("x-goog-api-key", self.auth.api_key),
            ]

            # Create a stream call
            stream_response = self.stub.StreamSpeech(
                grpc_request, metadata=metadata, timeout=self.timeout
            )

            # Process the streaming response
            for response in stream_response:
                # If there's an error message, raise an exception
                if response.error_message:
                    raise TsetsenError(message=response.error_message)

                # Call the callback if provided
                if callback:
                    callback(
                        response.audio_chunk, response.is_final, response.error_message
                    )

                # Yield the audio chunk
                yield response.audio_chunk

                # Break if this is the final chunk
                if response.is_final:
                    break

            logger.debug("Streaming completed successfully")

        except grpc.RpcError as e:
            self._handle_grpc_error(e, "Error streaming speech")

    def stream_speech_to_file(
        self,
        text: str,
        voice_id: str,
        output_file: str,
        speed: float = 1.0,
        progress_callback: Optional[Callable[[int, bool], None]] = None,
    ) -> None:
        """
        Stream speech generation and save it directly to a file.

        This is a convenience method that streams the audio and saves it to a file
        in one operation. It's useful for simple use cases where you just want
        to get a file without handling the streaming manually.

        Args:
            text: The text to convert to speech.
            voice_id: The ID of the voice to use.
            output_file: Path to the file where the audio will be saved.
            speed: Speech speed multiplier. Defaults to 1.0.
            progress_callback: Optional callback that will be called with
                            (bytes_received, is_complete) for progress tracking.

        Raises:
            InvalidRequestError: If the request parameters are invalid.
            AuthenticationError: If authentication fails.
            ServiceUnavailableError: If the service is unavailable.
            TsetsenError: For other API errors.
        """
        logger.debug(f"Streaming speech to file: {output_file}")

        # Open the output file for writing in binary mode
        with open(output_file, "wb") as f:
            total_bytes = 0

            # Define callback to write chunks to file and track progress
            def handle_chunk(
                chunk: bytes, is_final: bool, error_message: Optional[str]
            ) -> None:
                nonlocal total_bytes
                if chunk:
                    f.write(chunk)
                    total_bytes += len(chunk)
                    if progress_callback:
                        progress_callback(total_bytes, is_final)

            # Stream the speech and handle each chunk
            for _ in self.stream_speech(
                text=text, voice_id=voice_id, speed=speed, callback=handle_chunk
            ):
                pass  # We're handling everything in the callback

        logger.debug(f"Saved {total_bytes} bytes of audio to {output_file}")
