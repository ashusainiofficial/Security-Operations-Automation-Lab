import json
import requests

# Paste your unique Shuffle Webhook URL between the quotes below
SHUFFLE_WEBHOOK_URL = "https://shuffler.io"

alert_data = {
    "message": "Failed Windows login detected",
    "event": 4625,
    "user": "HackerAttackerAccount",
    "source_ip": "185.220.101.5"
}

try:
    response = requests.post(SHUFFLE_WEBHOOK_URL, json=alert_data, headers={"Content-Type": "application/json"})
    print(f"Status Code: {response.status_code}")
    print("Response text:", response.text)
except Exception as e:
    print(f"Delivery failed: {e}")
