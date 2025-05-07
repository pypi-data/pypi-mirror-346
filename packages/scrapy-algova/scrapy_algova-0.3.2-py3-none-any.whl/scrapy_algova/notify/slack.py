# src/notify/slack.py
import requests
from .base import BaseNotifier

class SlackNotifier(BaseNotifier):
    def notify(self, message: str, context: dict = None):
        url = self.settings.get("NOTIFIER_SLACK_WEBHOOK")
        if not url:
            return
        payload = {"text": message}
        requests.post(url, json=payload)
