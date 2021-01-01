from django.db import models


class Log5XXError(models.Model):
    """
    Model class that will contain all the exceptions that happen during the runtime.
    """
    exception = models.CharField(max_length=255, null=True, blank=True)
    exception_traceback = models.TextField(null=True, blank=True)
    exception_class = models.CharField(max_length=255, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    request_method = models.CharField(max_length=15, null=True, blank=True)
    request_body = models.TextField(null=True, blank=True)
    request_headers = models.TextField(null=True, blank=True)
    request_is_ajax = models.BooleanField(null=True, blank=True)
    request_is_secure = models.BooleanField(null=True, blank=True)
    request_scheme = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=5, choices=(
        ("0", "Open"),
        ("1", "Resolved"),
    ), default="0")

    def __str__(self):
        return str(self.exception_class) + " at " + str(self.time)
