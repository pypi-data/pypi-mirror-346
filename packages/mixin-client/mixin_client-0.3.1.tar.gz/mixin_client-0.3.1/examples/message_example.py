"""
Mixin Message API Example
~~~~~~~~~~~~~~~~~~~~~~~

This example demonstrates how to use the MixinClient to send text messages.
"""

import sys
import time

from mixin_client import MixinBotConfig, MixinClient
from mixin_client.http import RequestError, RequestTimeoutError


def send_message_with_retry(client, conversation_id, content, max_retries=3, retry_delay=2):
    """Send a message with retry logic."""
    for attempt in range(max_retries):
        try:
            message = client.api.message.send_text_message(
                conversation_id=conversation_id,
                content=content
            )
            return message
        except RequestTimeoutError as e:
            if attempt < max_retries - 1:
                print(f"Request timed out (attempt {attempt+1}/{max_retries}): {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Increase retry delay for next attempt
                retry_delay *= 1.5
            else:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
        except RequestError as e:
            print(f"API error: {e}")
            raise


def main():
    print("Initializing Mixin client...")
    try:
        client = MixinClient(MixinBotConfig.from_file("keystore.json"))
    except Exception as e:
        print(f"Failed to initialize client: {e}")
        sys.exit(1)

    try:
        # Get the current user's profile
        print("Getting user profile...")
        user_info = client.api.user.get_me()
        print(f"Logged in as: {user_info.data.full_name} ({user_info.data.user_id})")

        # You can replace this with your own conversation ID
        conversation_id = "ad6df1ea-b9ca-3057-b8ed-e3a5a58f1468"
        print(f"Using conversation ID: {conversation_id}")

        # Prepare message content
        message_content = "Hello from Mixin Python Client!"
        
        # Send a simple text message
        print("\nSending a text message...")
        print(f"Content: {message_content}")
        
        try:
            message = send_message_with_retry(
                client,
                conversation_id,
                message_content
            )
            print(f"Message sent successfully with ID: {message.data.message_id}")
            print("\nMessage details from API response:")
            print(f"  Category: {message.data.category}")
            # Note: The content field might be empty in the API response
            # This is normal and doesn't mean the message wasn't sent
            print(f"  Content: {message.data.content or '(empty in response)'}")
            print(f"  Created at: {message.data.created_at}")
            
        except Exception as e:
            print(f"Error sending message: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main() 