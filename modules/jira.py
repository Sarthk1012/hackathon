import httpx
import requests
import os
from dotenv import load_dotenv

load_dotenv()

jira_token = os.getenv("JIRA_TOKEN", "")
print("jira_token", jira_token)

JIRA_API_AUTH = ("duggal.sarthak12@gmail.com", jira_token)
JIRA_API_BASE_URL = "https://tifin-hackathon.atlassian.net"


async def get_jira_issue():
    url = f"{JIRA_API_BASE_URL}/rest/agile/1.0/board/1/issue"
    print(url, JIRA_API_AUTH)
    try:
        response = requests.get(url, auth=JIRA_API_AUTH)
        response.raise_for_status()
        result = response.json()
        return result
    except Exception as e:
        print("error", e)
