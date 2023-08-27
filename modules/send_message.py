import os
from slack_sdk import WebClient


async def send_message_to_user(user_email: str, message: str, blocks: list):
    SLACK_TOKEN = os.getenv("SLACK_TOKEN", "")
    client = WebClient(token=SLACK_TOKEN)
    users_list = client.users_list()
    user_id = None
    message_blocks = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": message,
                "emoji": True,
            },
        },
        {"type": "divider"},
    ]
    message_blocks.extend(blocks)

    message_payload = {
        "text": message,
        "blocks": message_blocks,
    }

    for user in users_list["members"]:
        print(user["profile"].get("email"), user_email)
        if user["profile"].get("email") == user_email:
            user_id = user["id"]
            break
    if user_id:
        client.chat_postMessage(channel=user_id, **message_payload)
    else:
        print("User not found.")
