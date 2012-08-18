# -*- coding:utf-8 -*-
#
# Copyright (C) 2012, Maximilian Köhl <linuxmaxi@googlemail.com>
# Copyright (C) 2012, Carlos Jenkins <carlos@jenkins.co.cr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import os
import sys

from distutils.core import setup

cmdclass = {}
try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError as e:
    print(e)
    print('Unable to import Sphinx custom command. Documentation build will '
          'be unavailable. Install python-sphinx to solve this.')

try:
    from sphinx_pypi_upload import UploadDoc
    cmdclass['upload_sphinx'] = UploadDoc
except ImportError as e:
    print(e)
    print('Unable to import Sphinx custom command. Documentation upload '
          'be unavailable. Install http://pypi.python.org/pypi/Sphinx-PyPI-'
          'upload/ to solve this.')

sys.path.insert(0, './src/')
import gtkspellcheck as m

if len(sys.argv) > 1 and sys.argv[1] == 'register':
    m.__desc_long__ = open(os.path.join('.', 'doc', 'pypi', 'page.rst'), 'r').read()
    print('pypi registration: override `long_description`')

setup(name=m.__short_name__,
      version=m.__version__,
      description=m.__desc_short__,
      long_description=m.__desc_long__,
      author=m.__authors__,
      author_email=m.__emails__,
      url=m.__website__,
      download_url=m.__download_url__,
      license='GPLv3+',
      package_dir={'': 'src'},
      packages=['gtkspellcheck', 'pylocales'],
      package_data={'pylocales' : ['locales.db']},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: X11 Applications :: Gnome',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: MacOS :: MacOS X', # Should work on MacOS X I think...
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Localization'],
      cmdclass=cmdclass)
