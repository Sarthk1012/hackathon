from fastapi import FastAPI, Request
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv
from controllers.ask_daily_updates_controller.app import ask_daily_updates_controller
from modules.get_response_from_prompt import get_response_from_prompt
from controllers.send_daily_updates_to_pm.app import send_daily_updates_to_pm_controller


load_dotenv()

app = FastAPI()


@app.get("/ask-daily-updates")
async def ask_daily_updates():
    ask_daily_updates_controller()


@app.post("/slack/events")
async def slack_events(request: Request):
    try:
        verifier = SignatureVerifier("f175948102001cbe9fd4e227d3a97419")
        body = await request.body()

        headers = dict(request.headers)

        if not verifier.is_valid_request(body, headers):
            return "Unauthorized", 403

        data = await request.json()

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
                {"JIRA-1": status}, "singh.raviranjan6@gmail.com"
            )
            return "Success"
    except Exception as e:
        print("Error posting message", str(e))
        return f"Error posting message: {str(e)}", 500
