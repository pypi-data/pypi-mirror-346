#!/usr/bin/env python
"""
Test script for the IndoxRouter client.
This script tests authentication and basic functionality of the client.
"""

import os
import sys
import logging
from indoxrouter import Client, AuthenticationError, NetworkError

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("indoxrouter_test")


def test_client(api_key=None, debug=False):
    """
    Test the IndoxRouter client with the provided API key.

    Args:
        api_key: API key to use for authentication
        debug: Whether to enable debug logging
    """
    if debug:
        logging.getLogger("indoxrouter").setLevel(logging.DEBUG)

    logger.info("Testing IndoxRouter client...")

    # If no API key is provided, try to get it from environment variable
    if not api_key:
        api_key = os.environ.get("INDOX_ROUTER_API_KEY")
        if not api_key:
            logger.error(
                "No API key provided. Please provide an API key as an argument or set the INDOX_ROUTER_API_KEY environment variable."
            )
            sys.exit(1)

    try:
        # Initialize client
        logger.info("Initializing client...")
        client = Client(api_key=api_key)

        # Test connection
        logger.info("Testing connection...")
        connection_info = client.test_connection()
        logger.info(f"Connection test: {connection_info['status']}")

        # Try to get available models
        logger.info("Fetching available models...")
        models = client.models()

        # Display some models
        providers = [p.get("name") for p in models]
        logger.info(f"Available providers: {', '.join(providers)}")

        # Try a simple chat completion
        logger.info("Testing chat completion...")
        response = client.chat(
            messages=[{"role": "user", "content": "Hello, who are you?"}],
            model="openai/gpt-3.5-turbo",
            max_tokens=30,
        )

        logger.info("Chat completion successful!")
        logger.info(f"Response: {response['choices'][0]['message']['content']}")

        logger.info("All tests passed! The client is working correctly.")

    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        logger.error("Please check that your API key is correct.")
        sys.exit(1)
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        logger.error(
            "Please check your internet connection and that the IndoxRouter server is accessible."
        )
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test the IndoxRouter client")
    parser.add_argument("--api-key", "-k", help="API key to use for authentication")
    parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug logging"
    )

    args = parser.parse_args()

    test_client(api_key=args.api_key, debug=args.debug)
