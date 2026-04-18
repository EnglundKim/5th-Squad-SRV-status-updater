import requests
import os
from datetime import datetime

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK", "").replace("*", "").strip()
MESSAGE_ID = os.getenv("MESSAGE_ID", "").replace("*", "").strip()
SERVER_ID = os.getenv("BATTLEMETRICS_SERVER_ID", "").replace("*", "").strip()

def get_server_data():
    url = f"https://api.battlemetrics.com/servers/{SERVER_ID}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    attr = data['data']['attributes']
    details = attr.get('details', {})

    return {
        "name": attr.get('name', 'N/A'),
        "status": "Online" if attr.get('status') == "online" else "Offline",
        "players": f"{attr.get('players', 0)}/{attr.get('maxPlayers', 0)}",
        "map": details.get('map', 'Unknown')
    }

def update_discord(data):
    base_url = WEBHOOK_URL.split('?')[0].rstrip('/')
    edit_url = f"{base_url}/messages/{MESSAGE_ID}"

    payload = {
        "embeds": [{
            "title": "Server Status",
            "color": 5814783,
            "fields": [
                {"name": "Server Name", "value": data['name'], "inline": False},
                {"name": "Status", "value": data['status'], "inline": True},
                {"name": "Players", "value": data['players'], "inline": True},
                {"name": "Map", "value": data['map'], "inline": False}
            ],
            "footer": {"text": "Updated via GitHub Actions"},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }]
    }

    resp = requests.patch(edit_url, json=payload)
    if resp.status_code == 200:
        print("✅ Updatet successfully!")
    else:
        print(f"❌ Discord error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    try:
        s_info = get_server_data()
        update_discord(s_info)
    except Exception as e:
        print(f"Critical error: {e}")
        exit(1)
