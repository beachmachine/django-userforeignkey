# -*- coding: utf-8 -*-
import logging
from django_userforeignkey.request import set_current_request

# import Django 1.10 middleware
try:
    from django.utils.deprecation import MiddlewareMixin
except:
    class MiddlewareMixin(object):
        def __init__(self, get_response=None):
            self.get_response = get_response
            super(MiddlewareMixin, self).__init__()
    
        def __call__(self, request):
            response = None
            if hasattr(self, 'process_request'):
                response = self.process_request(request)
            if not response:
                response = self.get_response(request)
            if hasattr(self, 'process_response'):
                response = self.process_response(request, response)
            return response


logger = logging.getLogger(__name__)


class UserForeignKeyMiddleware(MiddlewareMixin):
    """Middleware RequestMiddleware

    This middleware saves the currently processed request
    in the working thread. This allows us to access the
    request everywhere, and don't need to pass it to every
    function.
    """

    def process_request(self, request):
        logger.debug(u"Process request")
        set_current_request(request)

    def process_response(self, request, response):
        logger.debug(u"Process response")

        # we have to keep the request in memory if we are in test mode, so get_current_user is working
        if request.META.get('SERVER_NAME', None) != 'testserver':
            set_current_request(None)

        return response

