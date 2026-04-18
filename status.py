import requests
import os

# Haetaan tiedot GitHubin asetuksista (Secrets) tietoturvan vuoksi
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
MESSAGE_ID = os.getenv("MESSAGE_ID")
SERVER_ID = os.getenv("BATTLEMETRICS_SERVER_ID")

def get_server_data():
    # Haetaan tiedot BattleMetrics API:sta (ilmainen julkinen haku)
    url = f"https://battlemetrics.com{SERVER_ID}"
    response = requests.get(url).json()
    
    attr = response['data']['attributes']
    name = attr['name']
    players = attr['players']
    max_players = attr['maxPlayers']
    status = "🟢 Online" if attr['status'] == "online" else "🔴 Offline"
    
    return f"**{name}**\nStatus: {status}\nPlayers: {players}/{max_players}"

def update_discord(content):
    edit_url = f"{WEBHOOK_URL}/messages/{MESSAGE_ID}"
    payload = {
        "embeds": [{
            "title": "Server state",
            "description": content,
            "color": 3066993
        }]
    }
    requests.patch(edit_url, json=payload)

if __name__ == "__main__":
    try:
        data = get_server_data()
        update_discord(data)
        print("Updated succesfully!")
    except Exception as e:
        print(f"Error: {e}")
