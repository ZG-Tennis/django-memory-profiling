# -*- coding: utf-8 -*-
""" memory_profiling's settings """

from django.conf import settings


# MemoryMiddleware1 settings
SHOW = {
    'request_summary': getattr(settings, 'SHOW_REQUEST_SUMMARY', True),
    'response_summary': getattr(settings, 'SHOW_RESPONSE_SUMMARY', True),
    'compared_request_response_summaries': getattr(
        settings, 'SHOW_COMPARED_REQUEST_RESPONSE_SUMMARIES', True),
}

# MemoryMiddleware2 settings
SHOW_TOP_X_MEMORY_DELTAS = getattr(
    settings, 'SHOW_TOP_X_MEMORY_DELTAS', 10)

# MemoryUsageMiddleware settings
MEMORY_VIEW_THRESHOLD = getattr(
    settings, 'MEMORY_VIEW_THRESHOLD', 10)  # in Megabytes
SHOW_MEMORY_USAGE_PER_REQUEST = getattr(
    settings, 'SHOW_MEMORY_USAGE_PER_REQUEST', False)
MEMORY_WARNINGS_RECEIVERS = getattr(
    settings, 'MEMORY_WARNINGS_RECEIVERS', None)
MEMORY_SENDER_EMAIL = getattr(
    settings, 'MEMORY_SENDER_EMAIL',
    getattr(settings, 'DEFAULT_FROM_EMAIL', None)
)
MEMORY_WARNING_EMAIL_TEMPLATE_PATH = getattr(
    settings, 'MEMORY_WARNING_TEMPLATE_PATH',
    'memory_profiling/memory_warning_email'
)

# General settings (applies to all memory_profiling middlewares)
IGNORE_URLS_CONTAINING = getattr(
    settings, 'IGNORE_URLS_CONTAINING', ['site_media', 'static', '__debug__'])
SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL = getattr(
    settings, 'SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL', True)
