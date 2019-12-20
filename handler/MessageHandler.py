import requests
import json

class MessageHandler():  
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_slack_msg(self, message):
        payload = {"text": message}
        requests.post(
            self.webhook_url, 
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )