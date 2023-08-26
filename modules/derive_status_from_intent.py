def derive_status_from_message(intent: str):
    if intent == "ticket_status_done":
        return "Done"
    elif intent == "ticket_status_progress":
        return "In Progress"
    elif intent == "ticket_status_delayed":
        return "Delayed"
    elif intent == "ticket_blocked":
        return "Blocked"
    else:
        return "To Do"
