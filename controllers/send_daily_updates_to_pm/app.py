import os
from slack_sdk import WebClient
from modules.send_message import send_message_to_user
from supabase import create_client, Client


def find_slack_email_from_user_id(user_id: str):
    SLACK_TOKEN = os.getenv("SLACK_TOKEN", "")
    client = WebClient(token=SLACK_TOKEN)
    users_list = client.users_list()
    for user in users_list["members"]:
        if user_id == user["id"]:
            return user["profile"]["email"]


async def send_daily_updates_to_pm_controller(ticket_status_map: dict):
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    watcher_tickers_map = {}

    for ticket in ticket_status_map.keys():
        response = (
            supabase.table("ticket_watch_list")
            .select("watcher_id")
            .eq("ticket_id", ticket)
            .execute()
        )
        watchers = response.data
        watcher_ids = [watcher["watcher_id"] for watcher in watchers]
        for watcher_id in watcher_ids:
            if watcher_id not in watcher_tickers_map:
                watcher_tickers_map[watcher_id] = []
            watcher_tickers_map[watcher_id].append(ticket)

    for watcher_id in watcher_tickers_map.keys():
        user_pm_email = find_slack_email_from_user_id(watcher_id)
        message = ""
        for ticket in watcher_tickers_map[watcher_id]:
            message += f"{ticket}: {ticket_status_map[ticket]}\n"
        await send_message_to_user(user_pm_email, message, [])
