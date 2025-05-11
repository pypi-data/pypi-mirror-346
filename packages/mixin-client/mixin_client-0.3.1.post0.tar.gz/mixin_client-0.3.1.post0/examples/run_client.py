"""
Mixin Client Example
~~~~~~~~~~~~~~~~~~

This example demonstrates how to use the MixinClient to interact with the Mixin Network API.
"""

from mixin_client import MixinBotConfig, MixinClient


def main():
    # config = MixinBotConfig.from_file("config.json")

    client = MixinClient(MixinBotConfig.from_file("keystore.json"))

    try:
        # Test the client by calling the /me endpoint
        user_info = client.get_me()
        print("Successfully connected to Mixin Network!")
        print("\nUser Information:")
        print(f"User ID: {user_info.data.user_id}")
        print(f"Full Name: {user_info.data.full_name}")
        print(f"Identity Number: {user_info.data.identity_number}")
        print(f"Email: {user_info.data.email}")
        print(f"Biography: {user_info.data.biography}")
        print(f"Created At: {user_info.data.created_at}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()
