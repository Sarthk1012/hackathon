from modules.jira import get_jira_issue
from modules.send_message import send_message_to_user


async def fetch_jira_tickets():
    response = await get_jira_issue()
    issues = response.get("issues") or []
    shaped_issues = []
    for issue in issues:
        key = issue.get("key")
        fields = issue.get("fields") or {}
        summary = fields.get("summary") or ""
        parent = fields.get("parent")
        assignee = fields.get("assignee")
        if parent and assignee:
            shaped_issues.append(
                {
                    "id": key,
                    "summary": summary,
                    "user": assignee["emailAddress"],
                }
            )
    return shaped_issues


async def ask_update_for_ticket_of_particular_user(user_email: str, tickets: list):
    blocks = []
    for ticket in tickets:
        blocks.append(
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "JIRA_TICKET_UPDATE_ACTION___" + ticket["id"],
                },
                "label": {
                    "type": "plain_text",
                    "text": ticket["id"] + ticket["summary"],
                    "emoji": True,
                },
            }
        )
    message = "What is the update for the following Jira tickets"
    await send_message_to_user(user_email, message, blocks)
    return "message sent"


async def ask_daily_updates_controller():
    # Fetches all users from the database
    jira_tickets = await fetch_jira_tickets()
    unique_users = set()
    for ticket in jira_tickets:
        unique_users.add(ticket["user"])

    for user_email in unique_users:
        user_tickets = [
            ticket for ticket in jira_tickets if ticket["user"] == user_email
        ]
        await ask_update_for_ticket_of_particular_user(user_email, user_tickets)
    return "Task initiated"
