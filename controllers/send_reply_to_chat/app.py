import os
from slack_sdk import WebClient
from modules.get_response_from_prompt import get_response_from_prompt
from modules.send_message import send_message_to_user


async def send_reply_to_chat(
    message: str,
    user_id: str,
):
    SLACK_TOKEN = os.getenv("SLACK_TOKEN", "")
    client = WebClient(token=SLACK_TOKEN)
    users_list = client.users_list()
    user_email = None
    for user in users_list["members"]:
        if user["id"] == user_id:
            user_email = user["profile"].get("email")
            break
    message = get_response_from_prompt(message)
    if user_email:
        await send_message_to_user(user_email, message, [])
