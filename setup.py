#! /usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import os
import re

from pip.req import parse_requirements
from setuptools import setup, find_packages


def read(*names):
    with open(os.path.join(os.path.dirname(__file__), *names)) as f:
        return f.read()


special_members = {}
for line in ast.parse(read('flask_template', '__init__.py')).body:
    if (not isinstance(line, ast.Assign) or len(line.targets) != 1 or
            not isinstance(line.targets[0], ast.Name) or
            not re.match(r'__.*?__', line.targets[0].id) or
            not isinstance(line.value, ast.Str)):
        continue
    special_members[line.targets[0].id] = line.value.s

pkg_name = special_members['__pkg_name__']

setup(
    name=pkg_name,
    version=special_members.get('__version__'),
    description=special_members.get('__description__'),
    long_description=read('README.md') + '\n\n\n' + read('LICENSE'),
    author=special_members.get('__author__'),
    author_email=special_members.get('__author_email__'),
    url=special_members.get('__url__'),
    packages=find_packages(exclude=['tests']),
    copyright=special_members.get('__copyright__'),
    license=special_members.get('__license__'),
    classifiers=[
        'Private :: Do Not Upload',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Database :: Front-Ends'
    ],
    install_requires=[str(x.req) for x in parse_requirements('install-requirements.txt', session=False)],
    tests_require=[str(x.req) for x in parse_requirements('requirements.txt', session=False)],
    include_package_data=True,
    zip_safe=False
)
