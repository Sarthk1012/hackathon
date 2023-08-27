from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv
from controllers.ask_daily_updates_controller.app import ask_daily_updates_controller
from modules.get_response_from_prompt import get_response_from_prompt
from modules.jira import get_jira_issue
from controllers.send_daily_updates_to_pm.app import send_daily_updates_to_pm_controller

load_dotenv()

app = FastAPI()


# @app.post("/slack/events")
# async def handle_slack_events(request: Request):
#     data = await request.json()

#     # Check if the request has a challenge parameter
#     if "challenge" in data:
#         return {"challenge": data["challenge"]}

#     # Handle other events as needed
#     # Your event handling logic goes here

#     return {"message": "Event received"}


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


@app.get("/ask-daily-updates")
async def ask_daily_updates():
    await ask_daily_updates_controller()


@app.get("/jira")
async def get_jira_stuff():
    response = await get_jira_issue()
    return JSONResponse(content={"data": response}, status_code=200)


@app.post("/slack/events")
async def slack_events(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    headers = request.headers
    data = await request.json()
    print("body", body)
    background_tasks.add_task(handle_slack_events, body, headers, data)
    return JSONResponse(content={"message": "Event received"}, status_code=200)
