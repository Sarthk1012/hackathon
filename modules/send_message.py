import os
from slack_sdk import WebClient


async def send_message_to_user(user_email: str, message: str):
    SLACK_TOKEN = os.getenv("SLACK_TOKEN", "")
    client = WebClient(token=SLACK_TOKEN)
    users_list = client.users_list()
    user_id = None
    for user in users_list["members"]:
        if user["profile"].get("email") == user_email:
            user_id = user["id"]
            break
    print("user_id", user_id)
    if user_id:
        client.chat_postMessage(channel=user_id, text=message)
    else:
        print("User not found.")
