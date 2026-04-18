import requests
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
MESSAGE_ID = os.getenv("MESSAGE_ID").strip() # strip() poistaa vahinkovälilyönnit
SERVER_ID = os.getenv("BATTLEMETRICS_SERVER_ID")

def get_server_data():
    url = f"https://battlemetrics.com{SERVER_ID}"
    response = requests.get(url).json()
    
    attr = response['data']['attributes']
    name = attr['name']
    players = attr['players']
    max_players = attr['maxPlayers']
    # Squad-palvelimissa on usein myös jono (queue), lisätään se jos mahdollista
    queue = attr.get('details', {}).get('rust_queued_players', 0) # Esimerkki, Squadilla eri kenttä
    
    status = "🟢 Online" if attr['status'] == "online" else "🔴 Offline"
    return f"**{name}**\n\nTila: {status}\nPelaajat: **{players}/{max_players}**"

def update_discord(content):
    # Varmistetaan että URL on oikeassa muodossa
    # HUOM: Webhook-URL ei saa päättyä vinoviivaan
    base_url = WEBHOOK_URL.split('?')[0].rstrip('/')
    edit_url = f"{base_url}/messages/{MESSAGE_ID}"
    
    payload = {
        "embeds": [{
            "title": "Palvelimen reaaliaikainen tila",
            "description": content,
            "color": 3066993,
            "footer": {"text": "Päivitetty automaattisesti GitHub Actionsilla"}
        }]
    }

    response = requests.patch(edit_url, json=payload)
    
    if response.status_code == 200:
        print("✅ Viesti päivitetty onnistuneesti!")
    else:
        print(f"❌ Virhe päivityksessä: {response.status_code}")
        print(f"Vastaus: {response.text}")
        # Tämä aiheuttaa GitHub Actionssiin punaisen valon jos epäonnistuu
        exit(1) 

if __name__ == "__main__":
    data = get_server_data()
    update_discord(data)
