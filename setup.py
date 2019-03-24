#!/usr/bin/env python
import os

from setuptools import setup, find_packages

requires = [
    "sqlalchemy",
    "sanic",
    "sanic-restful",
    "pyjwt",
    "pytest",
    "pytest-sanic",
    "pytest-ordering"
]

version = os.environ.get('VERSION')

if version is None:
    with open(os.path.join('.', 'VERSION')) as version_file:
        version = version_file.read().strip()

setup_options = {
    'name': 'kakaopay',
    'version': version,
    'description': 'kakaopay api',
    'long_description_content_type': 'text/markdown',
    'long_description': open('README.md').read(),
    'url': 'https://github.com/nh32001/kakaopay',
    'author': 'nh32001',
    'author_email': 'nh32001@naver.com',
    'packages': find_packages(exclude=['tests*', 'docs']),
    'package_data': {'kakaopay': ['*']},
    'license': "Apache License 2.0",
    'install_requires': requires,
    'entry_points': {
        'console_scripts': [
            'kakaopay=kakaopay.cli:main'
        ],
    },
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers', 
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7'
    ],
    'test_suite': 'tests'
}

setup(**setup_options)
