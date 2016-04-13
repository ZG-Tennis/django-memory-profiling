# -*- coding: utf-8 -*-
""" memory_profiling's psutil_middleware """

import os
import psutil
import logging

from django.template.defaultfilters import filesizeformat
from templated_email import send_templated_mail

from memory_profiling.mixins.middleware import BaseMemoryMiddlewareMixin
from memory_profiling.settings import MEMORY_VIEW_THRESHOLD, \
    MEMORY_WARNINGS_RECEIVERS, MEMORY_WARNING_EMAIL_TEMPLATE_PATH, \
    SHOW_MEMORY_USAGE_PER_REQUEST, SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL, \
    MEMORY_SENDER_EMAIL

from memory_profiling.utils import memory_info, warning, info


logger = logging.getLogger(__name__)
THRESHOLD = MEMORY_VIEW_THRESHOLD*1024*1024


class MemoryUsageMiddleware(BaseMemoryMiddlewareMixin):
    """
    A Django middleware for tracking memory usage and generating a usable
    result immediately, needs to hook both process request and process
    response. In other words, look at difference between start and finish
    of request and log a warning if exceeds some threshold.

    Inspired on
    http://stackoverflow.com/questions/12249150/how-to-log-memory-usage-of-an-django-app-per-request#answer-12254394
    """

    def process_request_actions(self, request):
        """
        Defines the custom flow to be run on process_request method only
        if the requested path is not ignored.
        """
        request._mem = memory_info(psutil.Process(os.getpid()))

    def process_response(self, request, response):
        """
        * Analizes memory usage
        * Shows memory used, if configured to do so
        * If memory threshold is surpassed, then a warning message is print
          and a warning email is sent to a user defined email list
        """
        if hasattr(request, "_mem"):
            mem = memory_info(psutil.Process(os.getpid()))
            diff = mem.rss - request._mem.rss
            memory_usage = u'MEMORY USAGE ({}, {})'.format(
                filesizeformat(diff), request.path)

            if SHOW_MEMORY_USAGE_PER_REQUEST:
                info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                     '~~~~~~~~~~~~~~~~~~~~~~~~~~')
                info(memory_usage)
                info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                     '~~~~~~~~~~~~~~~~~~~~~~~~~~')
                if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                    logger.info(
                        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                        '~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    )
                    logger.info(memory_usage)
                    logger.info(
                        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                        '~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    )

            if diff > THRESHOLD:
                humanized_threshold = filesizeformat(THRESHOLD)
                msg = u'MEMORY THRESHOLD OF {} HAS BEEN SURPASSED'.format(
                    humanized_threshold)

                warning(
                    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    '~~~~~~~~~~~~~~~~~~~~~~~~~~')
                warning(msg)
                warning(memory_usage)
                warning(
                    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    '~~~~~~~~~~~~~~~~~~~~~~~~~~')
                if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                    logger.warning(
                        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    )
                    logger.warning(msg)
                    logger.warning(memory_usage)
                    logger.warning(
                        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    )

                if MEMORY_WARNINGS_RECEIVERS and MEMORY_SENDER_EMAIL:
                    send_templated_mail(
                        template_name=MEMORY_WARNING_EMAIL_TEMPLATE_PATH,
                        from_email=MEMORY_SENDER_EMAIL,
                        recipient_list=MEMORY_WARNINGS_RECEIVERS,
                        context=dict(
                            subject='MEMORY WARNING',
                            threshold=humanized_threshold,
                            details=memory_usage
                        )
                    )

        return response
