# -*- coding: utf-8 -*-
import logging

from django.utils.deprecation import MiddlewareMixin

from django_userforeignkey.request import set_current_request


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
        set_current_request(None)
        return response
