import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-userforeignkey',
    version=os.getenv('PACKAGE_VERSION', '0.0.0').replace('refs/tags/', ''),
    packages=find_packages(),
    include_package_data=True,
    long_description_content_type='text/markdown',
    license='BSD License',
    description='A simple Django app that will give you a UserForeignKey model field.',
    long_description=README,
    url='https://github.com/beachmachine/django-userforeignkey/',
    author='Andreas Stocker',
    author_email='andreas@stocker.co.it',
    python_requires='>=3.10',
    install_requires=[
        'Django>=4.2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
