import requests
import os
from datetime import datetime

# Haetaan tiedot GitHub Secretsistä
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
MESSAGE_ID = os.getenv("MESSAGE_ID").strip()
SERVER_ID = os.getenv("BATTLEMETRICS_SERVER_ID")

def get_server_data():
    # Haetaan tiedot BattleMetrics API:sta
    url = f"https://battlemetrics.com{SERVER_ID}"
    response = requests.get(url).json()
    
    attr = response['data']['attributes']
    details = attr.get('details', {})
    
    # Valmistellaan tiedot
    server_name = attr.get('name', 'N/A')
    status = "Online" if attr.get('status') == "online" else "Offline"
    players = f"{attr.get('players', 0)}/{attr.get('maxPlayers', 0)}"
    map_name = details.get('map', 'Unknown')

    return {
        "name": server_name,
        "status": status,
        "players": players,
        "map": map_name
    }

def update_discord(data):
    # Puhdistetaan webhook-osoite varmuuden vuoksi
    base_url = WEBHOOK_URL.split('?')[0].rstrip('/')
    edit_url = f"{base_url}/messages/{MESSAGE_ID}"
    
    # Käytetään Pipedream-koodisi mukaista ulkoasua
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
            "image": {
                "url": "https://discordapp.com&"
            },
            "footer": {"text": "Updated"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    response = requests.patch(edit_url, json=payload)
    
    if response.status_code == 200:
        print("✅ Viesti päivitetty onnistuneesti!")
    else:
        print(f"❌ Virhe: {response.status_code}")
        print(f"Vastaus: {response.text}")
        exit(1)

if __name__ == "__main__":
    try:
        server_info = get_server_data()
        update_discord(server_info)
    except Exception as e:
        print(f"Kriittinen virhe: {e}")
        exit(1)
