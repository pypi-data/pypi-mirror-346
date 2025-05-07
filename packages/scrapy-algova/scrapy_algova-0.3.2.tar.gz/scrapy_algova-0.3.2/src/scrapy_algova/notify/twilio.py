# src/notify/twilio.py
from twilio.rest import Client
from .base import BaseNotifier

class TwilioNotifier(BaseNotifier):
    def notify(self, message: str, context: dict = None):
        sid = self.settings.get("TWILIO_ACCOUNT_SID")
        token = self.settings.get("TWILIO_AUTH_TOKEN")
        from_ = self.settings.get("TWILIO_FROM_NUMBER")
        to_   = self.settings.get("TWILIO_TO_NUMBER")

        if not all([sid, token, from_, to_]):
            return

        client = Client(sid, token)
        client.messages.create(
            body=message,
            from_=from_,
            to=to_
        )
