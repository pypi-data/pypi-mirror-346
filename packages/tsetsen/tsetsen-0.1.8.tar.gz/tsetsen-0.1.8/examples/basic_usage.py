#!/usr/bin/env python3
"""
Basic usage example for Tsetsen TTS Python SDK

This example demonstrates how to use the Tsetsen TTS Python SDK to:
1. Initialize the client
2. List available voices
3. Generate speech from text
4. Check request status and get the audio URL
5. Get user balance

To run this example:
1. Set your API key in the TSETSEN_API_KEY environment variable or pass it directly
2. Run: python basic_usage.py
"""
import os
import time
import sys
import logging
from typing import Optional

# Add the package root to the path for development
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tsetsen import Client, RequestStatus
from src.tsetsen.exceptions import TsetsenError


def setup_logging():
    """Set up basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Enable debug logging for the tsetsen client
    logging.getLogger("tsetsen").setLevel(logging.DEBUG)


def main():
    """Main entry point for the example."""
    setup_logging()
    
    # Get API key from environment or use default for demo
    api_key = os.environ.get("TSETSEN_API_KEY")
    if not api_key:
        print("Please set the TSETSEN_API_KEY environment variable or provide an API key.")
        print("Example: TSETSEN_API_KEY=your-api-key python basic_usage.py")
        sys.exit(1)
    
    try:
        # Initialize the client
        with Client(api_key=api_key, secure=True) as client:
            # 1. List available voices
            print("\n=== Listing Available Voices ===")
            voices_response = client.list_voices(version="beta-v0.1")
            
            print(f"Found {len(voices_response.voices)} voices:")
            for i, voice in enumerate(voices_response.voices[:5]):  # Limit to first 5 for brevity
                print(f"  {i+1}. ID: {voice.id}, Name: {voice.name}, Gender: {voice.gender.name}")
            
            if len(voices_response.voices) > 5:
                print(f"  ...and {len(voices_response.voices) - 5} more")
            
            # Select the first voice for the demo, if available
            if not voices_response.voices:
                print("No voices available. Exiting.")
                return
            
            selected_voice = voices_response.voices[0]
            print(f"\nSelected voice: {selected_voice.name} ({selected_voice.id})")
            
            # 2. Check user balance
            print("\n=== Checking User Balance ===")
            balance = client.get_user_balance()
            print(f"Available credits: {balance.credits}")
            
            # 3. Generate speech
            print("\n=== Generating Speech ===")
            text = "Hello, this is a test of the Tsetsen Text-to-Speech API. It converts text to natural-sounding speech."
            
            generate_response = client.generate_speech(
                text=text,
                voice_id=selected_voice.id,
                speed=1.0
            )
            
            request_id = generate_response.request_id
            print(f"Generation request submitted. Request ID: {request_id}")
            
            # 4. Monitor status until complete
            print("\n=== Monitoring Status ===")
            status = generate_response.status
            
            start_time = time.time()
            try:
                while status != RequestStatus.COMPLETED and status != RequestStatus.FAILED:
                    time.sleep(1)  # Poll every second
                    
                    status_response = client.check_status(request_id=request_id)
                    status = status_response.status
                    
                    elapsed = time.time() - start_time
                    print(f"Status after {elapsed:.1f}s: {status.name}")
                    
                    if status == RequestStatus.COMPLETED:
                        print("\n=== Speech Generation Complete ===")
                        print(f"Audio URL: {status_response.audio_url}")
                        
                        if status_response.metrics:
                            metrics = status_response.metrics
                            print("\nPerformance Metrics:")
                            if metrics.queue_time is not None:
                                print(f"  Queue time: {metrics.queue_time/1000:.2f}s")
                            if metrics.processing_time is not None:
                                print(f"  Processing time: {metrics.processing_time/1000:.2f}s")
                            if metrics.total_time is not None:
                                print(f"  Total time: {metrics.total_time/1000:.2f}s")
                            if metrics.audio_length is not None:
                                print(f"  Audio length: {metrics.audio_length:.2f}s")
                            if metrics.credits_used is not None:
                                print(f"  Credits used: {metrics.credits_used}")
                            if metrics.character_count is not None:
                                print(f"  Character count: {metrics.character_count}")
                        
                    elif status == RequestStatus.FAILED:
                        print("\n=== Speech Generation Failed ===")
                        print(f"Error message: {status_response.error_message}")
                    
                    # Timeout after 60 seconds
                    if elapsed > 60:
                        print("Request is taking too long. You can continue checking the status manually.")
                        break
            
            except KeyboardInterrupt:
                print("\nMonitoring interrupted. You can check the status later with the request ID.")
            
            # 5. Final status check using the helper method
            print("\n=== Using wait_for_completion Helper ===")
            print("The wait_for_completion method simplifies waiting for a request to complete.")
            print("Example: client.wait_for_completion(request_id, timeout=30)")
    
    except TsetsenError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()