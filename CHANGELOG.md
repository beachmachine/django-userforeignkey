# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.5.0]

### Added
- Added support for ASGI/async

### Removed
- Dropped support for Django 3.1


## [0.4.0]

### Added
- Added support for Django 2.2, 3.1 and 3.2

### Removed
- Dropped support for Django 1.11, 2.0 and 2.1


## [0.3.0]

### Added
- Added support for Django 2.1

### Removed
- Dropped support for Django 1.8, 1.9 and 1.10


## [0.2.1]

### Changed
- Improved `.travis.yml`

### Added
- Added `setup.cfg` with the `license_file` keyword, ensuring that the actual LICENSE file is also installed when 
  using `pip install`


## [0.2.0]

### Changed
- Behaviour change: Prior to 0.2.0 the UserForeignKey field had `editable` set to `False` only 
  if `auto_user == True`. Since 0.2.0 `editable` is set to `False` 
  if `auto_user == True or auto_user_add == True`

### Added
- Added support for Django 2.0


## [0.1.2]

### Added
- Initial Release on PyPi


[0.5.0]: https://github.com/beachmachine/django-userforeignkey/releases/tag/0.5.0
[0.4.0]: https://github.com/beachmachine/django-userforeignkey/releases/tag/0.4.0
[0.3.0]: https://github.com/beachmachine/django-userforeignkey/releases/tag/0.3.0
[0.2.1]: https://github.com/beachmachine/django-userforeignkey/releases/tag/0.2.1
[0.2.0]: https://github.com/beachmachine/django-userforeignkey/releases/tag/0.2.0
[0.1.2]: https://github.com/beachmachine/django-userforeignkey/releases/tag/0.1.2
