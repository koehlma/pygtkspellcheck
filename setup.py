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

from distutils.core import setup

version = '2.3'
long_description = \
"""\
It supports both Gtk's Python bindings, PyGObject and PyGtk, and for both Python \
2 and 3 with automatic switching and binding autodetection. For automatic \
translation of the user interface it can use GEdit's translation files.\
"""

setup(name='pygtkspellchecker',
      version=version,
      description='A spellchecking library written in pure Python for Gtk based on Enchant',
      long_description=long_description,
      author='Maximilian Köhl & Carlos Jenkins',
      author_email='linuxmaxi@googlemail.com',
      url='http://www.github.com/koehlma/pygtkspellcheck',
      license='GPLv3',
      package_dir = {'': 'src'},
      packages=['gtkspellcheck'],
      package_data={'gtkspellcheck' : ['locales.db']}
)

