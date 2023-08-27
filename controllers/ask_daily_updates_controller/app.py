from modules.send_message import send_message_to_user


def fetch_jira_tickets(user_email: str):
    # Fetches JIRA tickets from the JIRA API
    # Returns a list of JIRA tickets
    return ["JIRA-1", "JIRA-2", "JIRA-3"]


async def ask_update_for_ticket_of_particular_user(user_email: str):
    user_jira_tickets = fetch_jira_tickets(user_email)
    blocks = []
    for ticket in user_jira_tickets:
        blocks.append(
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "JIRA_TICKET_UPDATE_ACTION___" + ticket,
                },
                "label": {"type": "plain_text", "text": ticket, "emoji": True},
            }
        )
    message = "What is the update for the following Jira tickets"
    await send_message_to_user(user_email, message, blocks)
    return "message sent"


async def ask_daily_updates_controller():
    # Fetches all users from the database
    users = ["singh.raviranjan6@gmail.com"]

    for user in users:
        await ask_update_for_ticket_of_particular_user(user)
