# -*- coding: utf-8 -*-

# Copyright (C) 2016, Maximilian Köhl <mail@koehlma.de>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3 as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__path__ = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(__path__, 'src'))

sys.modules['gtk'] = None

import pylocales
import gtkspellcheck

WARNING_MESSAGE = '''
==========================================================================
Warning: Do not use this script to create PyPi distributions!
It is a placeholder for the "pylocales" package! Its only purpose is to
prevent others from reusing this name which would otherwise lead to naming
conflicts with the "pygtkspellcheck" package.
==========================================================================
'''.strip()

if sys.version_info >= (3, 0, 0):
    raw_input = input

print(WARNING_MESSAGE)

while True:
    answer = raw_input('Do you want to proceed? (y/n) ').lower()
    if answer == 'y':
        break
    elif answer == 'n':
        sys.exit(0)

setup(
    name='pylocales',
    version=pylocales.__version__,
    description='convert ISO639 and ISO3166 codes to human readable names',
    author='Maximilian Köhl',
    author_email='mail@koehlma.de',
    url=gtkspellcheck.__website__,
    license='GPLv3+',
    packages=['pylocales'],
    package_dir={'': 'src'},
    package_data={'pylocales': ['locales.db']},
    extras_require={
        'building the documentation': ['sphinx']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Localization'
    ]
)
