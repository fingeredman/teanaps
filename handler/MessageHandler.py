from teanaps import configure as con

import requests
import json

class MessageHandler():  
    def __init__(self):
        self.webhook_url = con.WEBHOOK_URL

    def send_slack_msg(self, msg):
        payload = {"text": msg}
        requests.post(
            self.webhook_url, 
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )