Django UserForeignKey
=====================

[![PyPI version](https://img.shields.io/pypi/v/django-userforeignkey.svg?maxAge=2592000)](https://pypi.org/project/django-userforeignkey/)
[![Linter and tests](https://github.com/beachmachine/django-userforeignkey/workflows/Module%20tests/badge.svg)](https://github.com/beachmachine/django-userforeignkey/actions)
[![Codecov](https://img.shields.io/codecov/c/gh/beachmachine/django-userforeignkey)](https://codecov.io/gh/beachmachine/django-userforeignkey)

Django UserForeignKey is a simple Django app that will give you a `UserForeignKey` model field for Django models.
This field extends a regular ForeignKey model field, and has the option to automatically set the currently logged in 
user on insert and/or update.

Currently, Django 2.2 (Python 3.7+) and Django 3.2 (Python 3.7+) are supported.

If you need support for the insecure and deprecated Python 3.6, please fall back to version 0.4.0.

If you need support for the insecure and deprecated Django 1.11 and/or Python2, please fall back to version 0.3.0.

If you need support for the insecure and deprecated Django 1.8 (and possibly 1.9 and 1.10), please fall back to 
version 0.2.1.

There also is a [video tutorial on YouTube](https://www.youtube.com/watch?v=iJCbYMgUDW8>) that shows you basic 
functionality of this package.

## Quickstart

1. Install the package from pypi using pip:
```bash
pip install django-userforeignkey
```

2. Add `django_userforeignkey` to your `INSTALLED_APPS` within your Django settings file:
```python
INSTALLED_APPS = [
    ...
    'django_userforeignkey',
]
```

3. Add `django_userforeignkey.middleware.UserForeignKeyMiddleware` to your `MIDDLEWARE` settings like this:

```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
    'django_userforeignkey.middleware.UserForeignKeyMiddleware',
]
```

Make sure to insert the `UserForeignKeyMiddleware` middleware **after** `AuthenticationMiddleware`.

## Example usage

Just add `UserForeignKey` to your model like you would with any other foreign key.


```python
from django.db import models
from django_userforeignkey.models.fields import UserForeignKey

class MyModel(models.Model):
    my_data = models.CharField(max_length=64, verbose_name="Very important data that are somehow related to a user")
    user = UserForeignKey(auto_user_add=True, verbose_name="The user that is automatically assigned", related_name="mymodels")
```

The `UserForeignKey` behaves just like a normal foreign key to the user model (using `settings.AUTH_USER_MODEL`), and 
thus also has properties such as ``related_name``. However, whenever an object is created by calling an authenticated 
view (admin, REST API, ...) which contains a ``request.user`` object, the ``request.user`` object is automatically 
associated.


## Configuration options

The configuration options are similar to Django's [DateField](https://docs.djangoproject.com/en/4.1/ref/models/fields/#datefield).

* `auto_user`: Automatically sets the current user everytime the object is saved (e.g., created or updated). This is 
  useful for **last modified by** information.
* `auto_user_add`: Automatically sets the current user when the object is first created. This is useful 
  for **created by** information.


## Development and tests

```bash
git clone --recursive https://github.com/beachmachine/django-userforeignkey
cd django-userforeignkey
python -m venv ./venv
source venv/bin/activate
pip install -e .
pip install Django
cd tests/user_foreign_key_testapp
python manage.py test
```
