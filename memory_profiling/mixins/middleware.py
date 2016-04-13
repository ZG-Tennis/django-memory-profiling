# -*- coding: utf-8 -*-
""" memory_profiling' middleware mixins """

from memory_profiling.settings import IGNORE_URLS_CONTAINING


class BaseMemoryMiddlewareMixin(object):
    """
    Base memory middleware mixin that executes a custom flow when
    the requested url does not include user defined patterns/words
    """

    def is_ignored(self, path):
        """ Verifies if the path provided should be ignored """
        for term in IGNORE_URLS_CONTAINING:
            if path.find(term) != -1:
                return True
        return False

    def process_request_actions(self, request):
        """
        This method shold be overriden with a custom flow to be run
        on process_request method only if the requested path is not
        ignored.
        """
        pass

    def process_request(self, request):
        """
        Runs a custom flow only if the requested path is not ignored
        """
        if not self.is_ignored(request.META['PATH_INFO']):
            self.process_request_actions(request)
