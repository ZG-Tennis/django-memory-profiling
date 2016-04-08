# -*- encoding: utf-8 -*-
"""
Derived from Piotr Maliński's example with a few modifications
to use logging and:
http://www.rkblog.rk.edu.pl/w/p/profiling-django-object-size-and-memory-usage-pympler/
"""

import logging

from pympler import muppy
from pympler import summary
from pympler.asizeof import asizeof
from django.conf import settings


logger = logging.getLogger(__name__)


class MemoryMiddleware(object):
    """
    Measure memory taken by requested view, and response
    """

    IGNORE_URLS_CONTAINING = getattr(
        settings, 'IGNORE_URLS_CONTAINING', ['site_media', 'static'])

    def is_ignored(self, path):
        """ Verifies if the path provided should be ignored """
        for term in self.IGNORE_URLS_CONTAINING:
            if path.find(term) != -1:
                return True
        return False

    def process_request(self, request):
        if not self.is_ignored(request.META['PATH_INFO']):
            self.start_objects = muppy.get_objects()

    def process_response(self, request, response):
        path = request.META['PATH_INFO']

        if self.is_ignored(path):
            return response

        self.end_objects = muppy.get_objects()

        sum_start = summary.summarize(self.start_objects)
        sum_end = summary.summarize(self.end_objects)
        diff = summary.get_diff(sum_start, sum_end)

        logger.info(
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            '~~~~~~~~~~~~~~'
        )
        logger.info("Top 10 memory deltas after processing URL: %s", path)
        logger.info("%-60s %10s %10s", "type", "# objects", "total size")
        print '\n\n'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print "Top 10 memory deltas after processing URL: %s" % path
        print "%60s %10s %10s" % ("type", "# objects", "total size")

        for row in sorted(diff, key=lambda i: i[2], reverse=True)[:10]:
            logger.info("type: %60s , # objects: %10d, total size: %10d", *row)
            print "%60s %10d %10d" % tuple(row)

        start_size = asizeof(self.start_objects)
        end_size = asizeof(self.end_objects)

        logger.info(
            "Processed %s: memory delta %0.1f kB (%0.1f -> %0.1fMB), "
            "response size: %0.1f kB",
            path,
            (end_size - start_size) / 1024.0,
            start_size / 1048576.0,
            end_size / 1048576.0,
            len(response.content) / 1024.0,
        )
        print (
            "Processed %s: memory delta %0.1f kB (%0.1f -> %0.1fMB), "
            "response size: %0.1f kB" % (
                path,
                (end_size - start_size) / 1024.0,
                start_size / 1048576.0,
                end_size / 1048576.0,
                len(response.content) / 1024.0,
            )
        )
        logger.info(
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            '~~~~~~~~~~~~~~'
        )
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '\n\n'
        return response
