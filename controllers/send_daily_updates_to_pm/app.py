from modules.send_message import send_message_to_user


async def send_daily_updates_to_pm_controller(ticket_status_map: dict, user_email: str):
    user_pm_email = "duggal.sarthak12@gmail.com"
    message = f"Daily updates for {user_email}:\n"
    for ticket in ticket_status_map.keys():
        message += f"{ticket}: {ticket_status_map[ticket]}\n"
    print("the message is", message)
    await send_message_to_user(user_pm_email, message)
