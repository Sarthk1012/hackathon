def get_message_from_slack_payload(data: dict):
    if (
        "event" in data
        and "text" in data["event"]
        and data["event"].get("type") == "message"
        and data["event"].get("client_msg_id") is not None
    ):
        event = data["event"]
        message_text = event["text"]
        user_id = event["user"]
        return {"message": message_text, "user_id": user_id}
    return {"message": None, "user_id": None}
