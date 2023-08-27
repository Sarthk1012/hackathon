from fastapi.responses import JSONResponse
from slack_sdk.signature import SignatureVerifier
from modules.get_response_from_prompt import get_response_from_prompt
from controllers.send_daily_updates_to_pm.app import send_daily_updates_to_pm_controller


async def handle_slack_events(body, headers, data):
    try:
        verifier = SignatureVerifier("f175948102001cbe9fd4e227d3a97419")

        if not verifier.is_valid_request(body, headers):
            return "Unauthorized", 403

        if (
            "event" in data
            and "text" in data["event"]
            and data["event"].get("type") == "message"
            and data["event"].get("client_msg_id") is not None
        ):
            event = data["event"]
            message_text = event["text"]
            print("message_text", message_text)
            status = get_response_from_prompt(
                f"Provide a one-word JIRA status for the developer comment: {message_text}"
            )
            print("status", status)
            await send_daily_updates_to_pm_controller(
                {"JIRA-1": status}, "duggal.sarthak12@gmail.com"
            )
            return JSONResponse(content={"message": "Event received"}, status_code=200)
    except Exception as e:
        print(e)
        return f"Error posting message: {str(e)}", 500


async def handle_ticket_update(
    ticket_no: str, current_status_string: str, user_id: str
):
    status = get_response_from_prompt(
        f"""Provide a one-word JIRA status for the developer comment: {current_status_string}. Nothing less nothing more. Just the status as output.
        Only choose your answer from ['In Progress','Delayed','Blocked','In QA','Not Started','Done']"""
    )
    await send_daily_updates_to_pm_controller({"JIRA-1": status})
    return JSONResponse(content={"message": "Event received"}, status_code=200)
