=====================
Django UserForeignKey
=====================

.. image:: https://travis-ci.org/beachmachine/django-userforeignkey.svg?branch=master
    :target: https://travis-ci.org/beachmachine/django-userforeignkey

.. image:: https://img.shields.io/pypi/v/django-userforeignkey.svg?maxAge=2592000   :target:

Django UserForeignKey is a simple Django app (supporting Django 1.8 and 1.9) that will give you a UserForeignKey model field.
This field extends a regular ForeignKey model field, and has the option to automatically set the currently logged in user on
insert and/or update.

Currently, Django 1.8 (Python 2.7, Python 3.3+) and Django 1.9 (Python 2.7, Python 3.4+) are supported (Django 1.10a1 was tested too).

Quick start
-----------

1. Download and install using `pip install`

* either from `PyPi <https://pypi.python.org/pypi/django-userforeignkey/>`_

.. code-block:: bash

    pip install django-userforeignkey


* or directly from this git repo

.. code-block:: bash

    pip install git+https://github.com/beachmachine/django-userforeignkey.git


2. Add ``django_userforeignkey`` to your ``INSTALLED_APPS`` setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_userforeignkey',
    ]


3. Add ``django_userforeignkey.middleware.UserForeignKeyMiddleware`` to your ``MIDDLEWARE_CLASSES`` settings like this:

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

Just add ``UserForeignKey`` to your model like you would with any other foreign key:


.. code-block:: python

    from django.db import models
    from django_userforeignkey.models.fields import UserForeignKey

    class MyModel(models.Model):
        my_data = models.CharField(max_length=64, verbose_name="Very important data that are somehow related to a user")
        user = UserForeignKey(auto_user_add=True, verbose_name="The user that is automatically assigned", related_name="mymodels")


The ``UserForeignKey`` behaves just like a normal foreign key element (thus also has properties such as ``related_name``). However, whenever an object is created by calling an authenticated view (admin, REST API, ...) which contains a ``request.user`` object, the ``request.user`` object is automatically associated.

Development and Tests
---------------------

.. code-block:: bash

    git clone --recursive https://github.com/beachmachine/django-userforeignkey
    cd django-userforeignkey
    virtualenv -p python2.7 venv
    source venv/bin/activate
    python setup.py install
    pip install Django==1.9
    cd tests/user_foreign_key_testapp
    python manage.py test

