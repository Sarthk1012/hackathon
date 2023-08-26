from modules.send_message import send_message_to_user


def fetch_jira_tickets(user_email: str):
    # Fetches JIRA tickets from the JIRA API
    # Returns a list of JIRA tickets
    return ["JIRA-1", "JIRA-2", "JIRA-3"]


def ask_update_for_ticket_of_particular_user(user_email: str):
    user_jira_tickets = fetch_jira_tickets(user_email)
    # Ask the user for an update for each ticket
    combined_tickets_string = ", ".join(user_jira_tickets)
    message = "What is the update for {}?. Please reply for each ticket in a separate messgae".format(
        combined_tickets_string
    )
    send_message_to_user(user_email, message)
    return "message sent"


def ask_daily_updates_controller():
    # Fetches all users from the database
    users = ["singh.raviranjan6@gmail.com"]

    for user in users:
        ask_update_for_ticket_of_particular_user(user)
