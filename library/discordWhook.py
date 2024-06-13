import urequests as requests
import keys

def notify(message) -> None:
    data = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(keys.WEBHOOK_URL, json=data, headers=headers)
    response.close()