# -*- coding: utf-8 -*-
""" memory_profiling's settings """

from django.conf import settings


# just for MemoryMiddleware1
SHOW = {
    'request_summary': getattr(settings, 'SHOW_REQUEST_SUMMARY', True),
    'response_summary': getattr(settings, 'SHOW_RESPONSE_SUMMARY', True),
    'compared_request_response_summaries': getattr(
        settings, 'SHOW_COMPARED_REQUEST_RESPONSE_SUMMARIES', True),
}


# just for MemoryMiddleware2
SHOW_TOP_X_MEMORY_DELTAS = getattr(
    settings, 'SHOW_TOP_X_MEMORY_DELTAS', 10)

# for both
IGNORE_URLS_CONTAINING = getattr(
    settings, 'IGNORE_URLS_CONTAINING', ['site_media', 'static', '__debug__'])

# for both
SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL = getattr(
    settings, 'SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL', True)
