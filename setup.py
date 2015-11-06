# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from setuptools import setup, find_packages


setup(
    name='testmonkey',
    version='0.0.1a',
    packages=find_packages(),
    tests_require=[
        'requests',
    ]
)

