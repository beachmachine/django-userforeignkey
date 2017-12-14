=====================
Django UserForeignKey
=====================

.. image:: https://travis-ci.org/beachmachine/django-userforeignkey.svg?branch=master
    :target: https://travis-ci.org/beachmachine/django-userforeignkey

.. image:: https://img.shields.io/pypi/v/django-userforeignkey.svg?maxAge=2592000   :target:

Django UserForeignKey is a simple Django app (supporting Django 1.8 up to Django 2.0) that will give you a UserForeignKey model field.
This field extends a regular ForeignKey model field, and has the option to automatically set the currently logged in user on
insert and/or update.

Currently, Django 1.8, 1.11 (Python 2.7, Python 3.4+) and Django 2.0 (Python 3.4+) are supported.

*Note*: Django 1.9 and 1.10 should work too, but both versions are insecure and deprecated. Consider upgrading to a newer Django Version!

Quick start
-----------

1. Download and install using `pip install`

* either from `PyPi <https://pypi.python.org/pypi/django-userforeignkey/>`_

.. code-block:: bash

    pip install django-userforeignkey


* or directly from this git repo if you prefer the development version from the master branch

.. code-block:: bash

    pip install git+https://github.com/beachmachine/django-userforeignkey.git


2. Add ``django_userforeignkey`` to your ``INSTALLED_APPS`` setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_userforeignkey',
    ]


3. Add ``django_userforeignkey.middleware.UserForeignKeyMiddleware`` to your ``MIDDLEWARE`` settings like this:

.. code-block:: python

    MIDDLEWARE = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
        'django_userforeignkey.middleware.UserForeignKeyMiddleware',
    )


or if you are still using the an older Django version (e.g., Django 1.8) with ``MIDDLEWARE_CLASSES``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
        'django_userforeignkey.middleware.UserForeignKeyMiddleware',
    )


Make sure to insert the ``UserForeignKeyMiddleware`` middleware **after** ``AuthenticationMiddleware``.

Example usage
-------------

Just add ``UserForeignKey`` to your model like you would with any other foreign key.


.. code-block:: python

    from django.db import models
    from django_userforeignkey.models.fields import UserForeignKey

    class MyModel(models.Model):
        my_data = models.CharField(max_length=64, verbose_name="Very important data that are somehow related to a user")
        user = UserForeignKey(auto_user_add=True, verbose_name="The user that is automatically assigned", related_name="mymodels")



The ``UserForeignKey`` behaves just like a normal foreign key to the user model (using ``settings.AUTH_USER_MODEL``), and thus also has properties such as ``related_name``.
 However, whenever an object is created by calling an authenticated view (admin, REST API, ...) which contains a ``request.user`` object,
 the ``request.user`` object is automatically associated.


Configuration options
---------------------

The configuration options are similar to Djangos `DateField <https://docs.djangoproject.com/en/1.11/ref/models/fields/#datefield>`_

* ``auto_user``  Automatically sets the current user everytime the object is saved (e.g., created or updated). This is useful for *last modified by* information
* ``auto_user_add`` Automatically sets the current user when the object is first created. This is useful for *created by* information


Changelog
---------

0.2.0

* Tested for Django 2.0 support
* Updated test app for Django 2.0 support
* Updated tox and travis for automated tests with Django 2.0
* Behaviour change: Prior to 0.2.0 the UserForeignKey field had ``editable`` set to ``False`` only if ``auto_user == True``. Since 0.2.0 ``editable`` is set to ``False`` if ``auto_user == True or auto_user_add == True``

0.1.2

* Initial Release on PyPi


Development and Tests
---------------------

.. code-block:: bash

    git clone --recursive https://github.com/beachmachine/django-userforeignkey
    cd django-userforeignkey
    virtualenv -p python2 venv # or virtualenv -p python3
    source venv/bin/activate
    python setup.py install
    pip install Django
    cd tests/user_foreign_key_testapp
    python manage.py test


You can also use `tox` for testing, as it will test against several Django and Python versions automatically. See ``tox.ini`` for details.
