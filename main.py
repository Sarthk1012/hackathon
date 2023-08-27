from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from controllers.add_to_watchlist.app import add_to_watchlist
from controllers.ask_daily_updates_controller.app import ask_daily_updates_controller
from controllers.send_reply_to_chat.app import send_reply_to_chat
from tasks.app import handle_slack_events, handle_ticket_update
import urllib.parse
import json
from modules.jira import get_jira_issue


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
    background_tasks.add_task(handle_slack_events, body, headers, data)
    return JSONResponse(content={"message": "Event received"}, status_code=200)


@app.post("/slack/triggers")
async def slack_triggers(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    decoded_payload = urllib.parse.unquote(body.split(b"=")[1].decode("utf-8"))
    data = json.loads(decoded_payload)
    current_action = data.get("actions")[0]
    user = data.get("user")
    action_id = current_action.get("action_id")
    value = current_action.get("value")
    user_id = user.get("id")
    split_string = "ACTION___"

    if action_id.startswith("WATCH_TICKET_ACTION__"):
        background_tasks.add_task(
            add_to_watchlist, user_id, current_action.get("selected_options")
        )

    if action_id.startswith("START_CHAT_ACTION__"):
        background_tasks.add_task(send_reply_to_chat, value, user_id)
    if action_id.startswith("JIRA_TICKET_UPDATE_ACTION"):
        action_id = action_id.split(split_string)[1]
        background_tasks.add_task(handle_ticket_update, action_id, value, user_id)

    return JSONResponse(content={"message": "Triggered"}, status_code=200)


@app.post("/slack/ask")
async def slack_chat(request: Request):
    blocks = [
        {
            "type": "input",
            "dispatch_action": True,
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "START_CHAT_ACTION__",
            },
            "label": {
                "type": "plain_text",
                "text": "Please type your query here",
                "emoji": True,
            },
        }
    ]

    content = {"blocks": blocks}

    return JSONResponse(content=content, status_code=200)


async def fetch_jira_tickets_from_sprint():
    response = await get_jira_issue()
    issues = response.get("issues") or []
    shaped_issues = []
    for issue in issues:
        key = issue.get("key")
        fields = issue.get("fields") or {}
        summary = fields.get("summary") or ""
        parent = fields.get("parent")
        if parent:
            shaped_issues.append({"id": key, "summary": summary})
    return shaped_issues


@app.post("/slack/watch-ticket")
async def slack_watch_ticket(request: Request):
    current_sprint_tickets = await fetch_jira_tickets_from_sprint()

    options = []
    for ticket in current_sprint_tickets:
        options.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": ticket["id"] + ":" + ticket["summary"],
                    "emoji": True,
                },
                "value": ticket["id"],
            },
        )
    content = {
        "blocks": [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "checkboxes",
                        "options": options,
                        "action_id": "WATCH_TICKET_ACTION__",
                    }
                ],
            }
        ]
    }
    return JSONResponse(content=content, status_code=200)
