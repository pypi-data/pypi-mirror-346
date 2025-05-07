# src/sender/sender.py
import importlib

class Sender:
    """
    Manejador de notificaciones que unifica múltiples notifiers.
    """

    def __init__(self, settings, notifiers_paths=None):
        self.settings = settings

        if notifiers_paths is None:
            notifiers_paths = settings.getlist("NOTIFIER_CLASSES", [])

        self.notifiers = [self._import_notifier(path) for path in notifiers_paths if path]

    @classmethod
    def from_crawler(cls, crawler):
        """Facilita la creación en spiders con 'self.crawler'."""
        return cls(crawler.settings)

    def _import_notifier(self, class_path):
        """Dada la ruta 'package.module:ClassName', instancia la clase."""
        try:
            module_name, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            cls_ = getattr(module, class_name)
            return cls_(self.settings)
        except (ValueError, ImportError, AttributeError):
            return None

    def notify(self, message: str, context: dict = None, channels=None):
        """
        Envía 'message' a todos los notifiers.
        - 'channels' permite usar un subconjunto de notifiers si se desea.
        """
        if context is None:
            context = {}

        if channels:
            notifiers = [self._import_notifier(ch) for ch in channels]
        else:
            notifiers = self.notifiers

        for notifier in notifiers:
            if notifier:
                notifier.notify(message, context)
