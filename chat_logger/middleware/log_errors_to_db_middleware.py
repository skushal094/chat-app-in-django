import traceback
from datetime import datetime
import json
from contextlib import suppress
import pytz
from django.utils.deprecation import MiddlewareMixin
from chat_logger.models import Log5XXError


class Log5XXErrorsToDatabaseMiddleware(MiddlewareMixin):
    """
    This middleware will be catching all the exceptions and will
    store them in the database.
    """

    def process_exception(self, request, exception):
        """
        This method will store the exception in the database.
        :param request: HttpRequest object
        :param exception: Exception object
        :return: None
        """
        log = Log5XXError()
        log.exception = str(exception)
        with suppress(Exception):
            log.exception_traceback = "".join(
                traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))
            log.exception_class = exception.__class__.__name__
        log.time = datetime.now(tz=pytz.UTC)
        log.request_method = request.method
        with suppress(Exception):
            log.request_body = request.body.decode()
        with suppress(Exception):
            log.request_headers = json.dumps(dict(request.headers))
        log.request_is_ajax = request.is_ajax()
        log.request_is_secure = request.is_secure()
        log.request_scheme = request.scheme
        with suppress(Exception):
            log.save()
        return
