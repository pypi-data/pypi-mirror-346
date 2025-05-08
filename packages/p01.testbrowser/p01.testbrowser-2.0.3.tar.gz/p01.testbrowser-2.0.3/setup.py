##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup

$Id: setup.py 5262 2025-05-07 12:18:00Z roger.ineichen $
"""
from __future__ import absolute_import
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup (
    name='p01.testbrowser',
    version='2.0.3',
    author = "Roger Ineichen, Projekt01 GmbH",
    author_email = "dev@projekt01.ch",
    description = "Zope test brwoser based on webtest and wsgi app",
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    long_description_content_type='text/markdown',
    license = "ZPL 2.1",
    keywords = "ope z3c testing test browser Zope3",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    url = 'http://pypi.python.org/pypi/p01.testbrowser',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['p01'],
    test_suite='p01.testbrowser.tests',
    tests_require = [
        'zope.testing',
        # 'pyperf',
        ],
    extras_require = dict(
        test = [
            'p01.checker',
            'zope.testing',
            # 'pyperf',
            ],
        ),
    install_requires=[
        'setuptools',
        'beautifulsoup4',
        'soupsieve',
        'lxml',
        'pytz > dev',
        'six',
        'transaction',
        'WebTest >= 2.0.13',
        'WSGIProxy2',
        'z3c.json',
        'z3c.jsonrpc',
        'zope.cachedescriptors',
        'zope.component',
        'zope.configuration',
        'zope.interface',
        'zope.schema',
        'sgmllib3k;python_version>="3.0"',
    ],
    zip_safe = False,
    )
