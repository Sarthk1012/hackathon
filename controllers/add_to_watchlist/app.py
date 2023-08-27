import os
from supabase import create_client, Client


def add_to_watchlist(user_id: str, selected_options: list):
    local_selected_options = selected_options
    if selected_options is None:
        local_selected_options = []
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    for option in local_selected_options:
        ticket_id = option.get("value")
        try:
            data = (
                supabase.table("ticket_watch_list")
                .insert({"ticket_id": ticket_id, "watcher_id": user_id})
                .execute()
            )
            print(data)
        except Exception:
            pass
