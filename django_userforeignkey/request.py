# -*- coding: utf-8 -*-
import contextvars
import logging

from django.contrib.auth.models import AnonymousUser

current_request = contextvars.ContextVar("Current request")

logger = logging.getLogger(__name__)


def set_current_request(request):
    """
    Binds the request to the current thread.

    :param request: Django request object
    :return:
    """
    logger.debug(u"Save request in current thread")
    return current_request.set(request)


def get_current_request():
    """
    Gets the request from the current thread.

    :return: Django request object
    """
    return current_request.get(None)


def get_current_user():
    """
    Gets the current user from the current request. In case there is no current
    request, or there is no user information attached to the request, an AnonymousUser object
    is returned.

    :return: User object
    """
    request = get_current_request()
    if not request or not hasattr(request, 'user'):
        return AnonymousUser()
    return request.user
