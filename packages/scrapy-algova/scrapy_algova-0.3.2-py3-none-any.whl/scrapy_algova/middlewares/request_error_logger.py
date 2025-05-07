# scrapy_algova/middlewares/request_error_logger.py
import json
import os
from scrapy import signals
from scrapy.exceptions import IgnoreRequest

class RequestErrorLoggerMiddleware:
    def __init__(self, settings):
        """
        Se apoya en settings para decidir el destino de los logs:
          - LOG_ERRORS_TO: 'console' | 'jsonl' | 'none' (u otro).
          - LOG_ERRORS_FILE: si es 'jsonl', ruta de archivo donde escribir.
          - O integraciones con Slack/Twilio (Notifiers) si quieres.
        """
        self.log_destination = settings.get("LOG_ERRORS_TO", "console")  # p.e. 'console', 'jsonl', etc.
        self.log_file_path = settings.get("LOG_ERRORS_FILE", "errors.jsonl")
        
        # Ejemplo: si quieres reutilizar tu Sender interno:
        self.sender_enabled = settings.getbool("LOG_ERRORS_SENDER", False)

        # Podrías cargar notifiers o el Sender:
        self.sender = None
        if self.sender_enabled:
            from ..sender.sender import Sender
            self.sender = Sender(settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        """Intercepta las respuestas con estatus >= 400."""
        if response.status >= 400:
            error_data = self._build_error_data(
                request=request,
                spider=spider,
                error=f"HTTP {response.status}",
                response=response
            )
            self._handle_error(error_data, spider)
            # Decide si devuelves el response o lo ignoras. 
            # Por defecto, devuelves para que el spider decida:
            return response
        return response

    def process_exception(self, request, exception, spider):
        """Captura excepciones (errores de red, timeouts, etc.)."""
        error_data = self._build_error_data(
            request=request,
            spider=spider,
            error=str(exception)
        )
        self._handle_error(error_data, spider)
        # Devuelve None para que Scrapy siga manejando la excepción o llame al errback.
        return None

    def _build_error_data(self, request, spider, error, response=None):
        # Construye un diccionario con la info que quieras guardar.
        return {
            "spider": spider.name,
            "url": request.url,
            "method": request.method,
            "body": request.body.decode("utf-8", errors="replace") if request.body else "",
            "error": error,
            "status": getattr(response, "status", None),
        }

    def _handle_error(self, error_data, spider):
        """Registra o envía la información dependiendo de la config."""
        if self.log_destination == "console":
            spider.logger.error(f"[RequestError] {error_data}")
        elif self.log_destination == "jsonl":
            self._write_jsonl(error_data)
        # O, si integras con Slack/Twilio, etc.:
        elif self.log_destination == "sender" and self.sender:
            msg = (
                f"Spider {error_data['spider']} encountered an error: {error_data['error']} "
                f"[{error_data['url']}]"
            )
            self.sender.notify(msg, context=error_data)
        else:
            pass  # 'none' u otra acción

    def _write_jsonl(self, error_data):
        """Guarda el error en un archivo JSON Lines."""
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(error_data, ensure_ascii=False) + "\n")