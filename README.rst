=====================
Django UserForeignKey
=====================

Django UserForeignKey is a simple Django app that will give you a UserForeignKey model field. This field extends
a regular ForeignKey model field, and has the option to automatically set the currently logged in user on insert
and/or update.

Quick start
-----------

1. Add "django_userforeignkey" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_userforeignkey',
    ]

2. Add "django_userforeignkey.middleware.UserForeignKeyMiddleware" to your MIDDLEWARE_CLASSES settings like this::

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
        'django_userforeignkey.middleware.UserForeignKeyMiddleware',
    )

  Make sure to insert the "django_userforeignkey" middleware after the authentication middleware.

Example usage
-------------

Just add "UserForeignKey" to your model::

    from django.db import models
    from django_userforeignkey.models.fields import UserForeignKey

    class MyModel(models.Model):
        my_data = models.CharField(max_length=64, verbose_name="Very important data that are somehow related to a user")
        user = UserForeignKey(auto_user_add=True, verbose_name="The user that is automatically assigned")
