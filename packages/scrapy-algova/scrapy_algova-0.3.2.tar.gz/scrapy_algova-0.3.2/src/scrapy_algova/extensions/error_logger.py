# scrapy_algova/extensions/error_logger.py
import json
from scrapy import signals

class ErrorLoggerExtension:
    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings

        # Ejemplo de configuración para destino
        self.log_destination = self.settings.get("LOG_ERRORS_TO", "console")
        self.log_file_path = self.settings.get("LOG_ERRORS_FILE", "errors.jsonl")

        # Si quieres usar tu clase Sender, igual que antes
        self.sender_enabled = self.settings.getbool("LOG_ERRORS_SENDER", False)
        self.sender = None
        if self.sender_enabled:
            from ..sender.sender import Sender
            self.sender = Sender(self.settings)

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        # Conectar la señal spider_error
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        return ext

    def spider_error(self, failure, response, spider):
        """
        Maneja cualquier excepción ocurrida dentro de un callback del spider.
        'failure.request' indica la request que provocó el error.
        """
        error_data = self._build_error_data(failure, response, spider)
        self._handle_error(error_data, spider)

    def _build_error_data(self, failure, response, spider):
        # 'failure.request' y 'failure.value' te permiten detallar la excepción
        req = getattr(response, 'request', None)
        return {
            "spider": spider.name,
            "exception_type": type(failure.value).__name__,
            "error_message": failure.getErrorMessage(),
            "traceback": failure.getTraceback(),  # si quieres más info
            "url": req.url if req else None,
            "method": req.method if req else None,
            "body": req.body.decode("utf-8", errors="replace") if req and req.body else "",
            "status": getattr(response, "status", None)
        }

    def _handle_error(self, error_data, spider):
        """ Decide dónde guardar o enviar el error. """
        if self.log_destination == "console":
            spider.logger.error(f"[ParseError] {error_data}")
        elif self.log_destination == "jsonl":
            self._write_jsonl(error_data)
        elif self.log_destination == "sender" and self.sender:
            msg = (
                f"Spider '{error_data['spider']}' encountered an error: {error_data['error_message']} "
                f"({error_data['exception_type']}). Request: {error_data['url']}"
            )
            self.sender.notify(msg, context=error_data)
        else:
            pass  # 'none', etc.

    def _write_jsonl(self, data):
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")