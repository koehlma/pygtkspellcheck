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

import distutils.cmd
import distutils.command.install
import distutils.command.install_data
import os
import sys

from distutils.core import setup

commands = {}
try:
    from sphinx.setup_command import BuildDoc
    commands['build_sphinx'] = BuildDoc
except ImportError:
    print('build_sphinx command is unavailable, please install Sphinx to solve this')

__path__ = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(__path__, 'src'))

sys.modules['gtk'] = None
import gtkspellcheck
    
if len(sys.argv) > 1 and sys.argv[1] == 'register':
    with open(os.path.join(__path__, 'doc', 'pypi', 'page.rst'), 'rb') as _pypi:
        gtkspellcheck.__desc_long__ = _pypi.read().decode('utf-8')
    print('pypi registration: override `long_description`')

class InstallLocale(distutils.command.install_data.install_data):
    def run(self):
        locale_name = 'py{}gtkspellcheck.mo'.format(sys.version_info.major)
        base = os.path.join(self.install_dir, 'share', 'locale')
        self.mkpath(base)
        for lang in os.listdir(os.path.join(__path__, 'locale')):
            path = os.path.join(base, lang, 'LC_MESSAGES')
            self.mkpath(path)
            self.copy_file(os.path.join(__path__, 'locale', lang,
                                        'pygtkspellcheck.mo'),
                           os.path.join(path, locale_name))
            
commands['install_locale'] = InstallLocale
distutils.command.install.install.sub_commands.append(('install_locale',
                                                       lambda self: True))

data_files = []
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    windows_locale = os.path.join('dist', 'windows', 'locale')
    for lang in os.listdir(windows_locale):
        data_files.append((os.path.join('share', 'locale', lang, 'LC_MESSAGES'),
                           [os.path.join(windows_locale, lang, 'LC_MESSAGES', message_file)
                            for message_file in os.listdir(os.path.join(windows_locale, lang, 'LC_MESSAGES'))
                            if message_file.endswith('.mo')]))
    print('windows bdist_wininst include iso message files')

py_modules = []
gtkspell = os.getenv('GTKSPELL')
if sys.version_info.major == 2 and gtkspell is not None and gtkspell.lower() == 'true':
    py_modules.append('gtkspell')

setup(name=gtkspellcheck.__short_name__,
      version=gtkspellcheck.__version__,
      description=gtkspellcheck.__desc_short__,
      long_description=gtkspellcheck.__desc_long__,
      author=gtkspellcheck.__authors__,
      author_email=gtkspellcheck.__emails__,
      url=gtkspellcheck.__website__,
      download_url=gtkspellcheck.__download_url__,
      license='GPLv3+',
      py_modules=py_modules,
      packages=['gtkspellcheck', 'pylocales'],
      package_dir={'': 'src'},
      package_data={'pylocales' : ['locales.db']},
      data_files=data_files,
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: X11 Applications :: Gnome',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Localization'],
      cmdclass=commands)
