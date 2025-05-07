# src/notify/base.py
class BaseNotifier:
    def __init__(self, settings):
        self.settings = settings

    def notify(self, message: str, context: dict = None):
        raise NotImplementedError("You must implement 'notify'.")
