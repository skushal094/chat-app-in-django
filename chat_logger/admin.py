from django.contrib import admin
from . import models


class Log5XXErrorAdmin(admin.ModelAdmin):
    """
    This is the class which will organize how we see and interact with the model
    from the admin panel.
    """
    list_display = (
        'exception_class', 'exception', 'time', 'request_method',
        'status'
    )
    list_editable = ('status',)
    list_filter = ('status', 'time')
    date_hierarchy = 'time'
    ordering = ('-time', )
    actions = ["mark_resolved"]
    search_fields = ('exception_class', 'exception')
    readonly_fields = (
        'exception_class', 'exception_traceback', 'exception',
        'time', 'request_method', 'request_scheme', 'request_is_ajax',
        'request_is_secure', 'request_body', 'request_headers'
    )
    fieldsets = (
        ('Exception Details', {
            'fields': (
                'exception_class', 'exception_traceback',
                'exception', 'time', 'status'
            )
        }),
        ('Advanced Details', {
            'classes': ('collapse',),
            'fields': (
                ('request_method', 'request_scheme'),
                ('request_is_ajax', 'request_is_secure'),
                ('request_body', 'request_headers')
            ),
        }),
    )
    # radio_fields = {'status': admin.VERTICAL}

    def mark_resolved(self, request, queryset):
        queryset.update(status="1")  # This will mark the error(s) as resolved.

    mark_resolved.short_description = "Mark selected errors as resolved."


admin.site.register(models.Log5XXError, Log5XXErrorAdmin)
