import traceback
from datetime import datetime
import pytz
from django.utils.deprecation import MiddlewareMixin


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
        print(str(exception))
        traceback.print_tb(exception.__traceback__)
        print(exception.__class__.__name__)
        print(datetime.now(tz=pytz.UTC))
        print(request.method)
        print(request.body.decode())
        print(request.get_raw_uri())
        print(request.headers)
        print(request.is_ajax())
        print(request.is_secure())
        print(request.scheme)
        return
