# -*- coding: utf-8 -*-
""" memory_profiling's pympler_middleware """

import logging

# from django.conf import settings
from django.template.defaultfilters import filesizeformat
from pympler import muppy
from pympler import summary
from pympler.asizeof import asizeof
# from pympler import refbrowser
# from pympler import asizeof

from memory_profiling.settings import IGNORE_URLS_CONTAINING, SHOW, \
    SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL, SHOW_TOP_X_MEMORY_DELTAS


logger = logging.getLogger(__name__)


def output_function(o):
    return str(type(o))


class BaseMemoryMiddleware(object):
    """  """
    def is_ignored(self, path):
        """ Verifies if the path provided should be ignored """
        for term in IGNORE_URLS_CONTAINING:
            if path.find(term) != -1:
                return True
        return False

    def process_request(self, request):
        if not self.is_ignored(request.META['PATH_INFO']):
            self.start_objects = muppy.get_objects()


class MemoryMiddleware1(BaseMemoryMiddleware):
    """
    Measure memory taken by requested view, and response using pympler.muppy
    https://pythonhosted.org/Pympler/muppy.html#muppy
    * Derived from
      http://www.rkblog.rk.edu.pl/w/p/profiling-django-object-size-and-memory-usage-pympler/
      with a few modifications to use logging in order to print
      loggin panel of django debug toolbar.
    """

    def process_response(self, request, response):
        req = request.META['PATH_INFO']
        if not self.is_ignored(req):
            if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                logger.info(
                    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    '~~~~~~~~~~~~~~'
                )
            print '\n\n'
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
                '~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
                '~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
                '~~~~~~~~~~~~~~~~~~~~~~~~~~'
            if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                logger.info(u'REQUESTED URL: {}'.format(req))
            print u'REQUESTED URL: {}'.format(req)
            self.end_objects = muppy.get_objects()
            if SHOW['request_summary']:
                sum_start = summary.summarize(self.start_objects)
                if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                    logger.info(
                        '~~~~~~~~~ SUMMARIZE REQUEST OBJECTS ~~~~~~~~~')
                    for row in sorted(
                            sum_start, key=lambda i: i[2], reverse=True)[:15]:
                        logger.info(
                            "type: %60s , # objects: %10d, total size: %s",
                            *(row[0], row[1], filesizeformat(row[2]))
                        )
                print '~~~~~~~~~ SUMMARIZE REQUEST OBJECTS ~~~~~~~~~'
                summary.print_(sum_start)

            if SHOW['response_summary']:
                sum_end = summary.summarize(self.end_objects)
                if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                    logger.info(
                        '~~~~~~~~~ SUMMARIZE RESPONSE OBJECTS ~~~~~~~~~')
                    for row in sorted(
                            sum_end, key=lambda i: i[2], reverse=True)[:15]:
                        logger.info(
                            "type: %60s , # objects: %10d, total size: %s",
                            *(row[0], row[1], filesizeformat(row[2]))
                        )
                print '~~~~~~~~~ SUMMARIZE RESPONSE OBJECTS ~~~~~~~~~'
                summary.print_(sum_end)

            if SHOW['compared_request_response_summaries']:
                diff = summary.get_diff(sum_start, sum_end)
                if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                    logger.info(
                        '~~~~~~~~~ COMPARED REQUEST & RESPONSE SUMMARIES '
                        '~~~~~~~~~'
                    )
                    for row in sorted(
                            diff, key=lambda i: i[2], reverse=True)[:15]:
                        logger.info(
                            "type: %60s , # objects: %10d, total size: %s",
                            *(row[0], row[1], filesizeformat(row[2]))
                        )
                print \
                    '~~~~~~~~~ COMPARED REQUEST & RESPONSE SUMMARIES ~~~~~~~~~'
                summary.print_(diff)

            # print '~~~~~~~~~'
            # cb = refbrowser.ConsoleBrowser(
            #     response, maxdepth=2, str_func=output_function)
            # cb.print_tree()

            a = asizeof(response)
            a_string = 'Total size of response object in kB: %s' % \
                str(a/1024.0)
            b = asizeof(self.end_objects)
            b_string = 'Total size of end_objects in MB: %s' % str(b/1048576.0)
            c = asizeof(self.start_objects)
            c_string = 'Total size of start_objects in MB: %s' % \
                str(c/1048576.0)

            if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                logger.info(
                    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    '~~~~~~~~~~~~~~'
                )
                logger.info(a_string)
                logger.info(b_string)
                logger.info(c_string)
                logger.info(
                    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    '~~~~~~~~~~~~~~'
                )

            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
                '~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print a_string
            print b_string
            print c_string
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
                '~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
                '~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
                '~~~~~~~~~~~~~~~~~~~~~~~~~~'

        return response


class MemoryMiddleware2(BaseMemoryMiddleware):
    """
    Measure memory taken by requested view, and response
    * Derived from https://gist.github.com/dnordberg/289141
      with some modifications to use logging in order to print
      in loggin panel of django debug toolbar.
    """

    def process_response(self, request, response):
        path = request.META['PATH_INFO']

        if self.is_ignored(path):
            return response

        self.end_objects = muppy.get_objects()

        sum_start = summary.summarize(self.start_objects)
        sum_end = summary.summarize(self.end_objects)
        diff = summary.get_diff(sum_start, sum_end)

        if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
            logger.info(
                '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                '~~~~~~~~~~~~~~'
            )
            logger.info(
                "Top %d memory deltas after processing URL: %s",
                SHOW_TOP_X_MEMORY_DELTAS, path
            )
            logger.info("%-60s %10s %10s", "type", "# objects", "total size")
        print '\n\n'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print "Top %d memory deltas after processing URL: %s" % (
            SHOW_TOP_X_MEMORY_DELTAS, path)
        print "%60s %10s %10s" % ("type", "# objects", "total size")

        for row in sorted(diff, key=lambda i: i[2], reverse=True
                          )[:SHOW_TOP_X_MEMORY_DELTAS]:
            if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
                logger.info(
                    "type: %60s , # objects: %10d, total size: %s",
                    *(row[0], row[1], filesizeformat(row[2]))
                )
            print "%60s %10d %s" % (row[0], row[1], filesizeformat(row[2]))

        start_size = asizeof(self.start_objects)
        end_size = asizeof(self.end_objects)

        if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
            logger.info(
                '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                '~~~~~~~~~~~~~~'
            )
            logger.info(
                "Processed %s: memory delta %0.1f kB (%0.1f -> %0.1fMB), "
                "response size: %0.1f kB",
                path,
                (end_size - start_size) / 1024.0,
                start_size / 1048576.0,
                end_size / 1048576.0,
                len(response.content) / 1024.0,
            )
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'\
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
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
        if SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL:
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
