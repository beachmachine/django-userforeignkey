Changelog
---------

0.4.0

* Dropped support for Django 1.11, 2.0 and 2.1
* Added support for Django 2.2, 3.1 and 3.2

0.3.0 (Meta release, no actual code changes)

* Dropped support for Django 1.8, 1.9 and 1.10
* Added support for Django 2.1

0.2.1

* Added ``setup.cfg`` with the ``license_file`` keyword, ensuring that the actual LICENSE file is also installed when using ``pip install``
* Improved ``.travis.yml``

0.2.0

* Tested for Django 2.0 support
* Updated test app for Django 2.0 support
* Updated tox and travis for automated tests with Django 2.0
* Behaviour change: Prior to 0.2.0 the UserForeignKey field had ``editable`` set to ``False`` only if ``auto_user == True``. Since 0.2.0 ``editable`` is set to ``False`` if ``auto_user == True or auto_user_add == True``

0.1.2

* Initial Release on PyPi
