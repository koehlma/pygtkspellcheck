# -*- coding:utf-8 -*-
#
# Copyright (C) 2012, Maximilian Köhl <linuxmaxi@googlemail.com>
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

from gtkspellcheck import __version__

setup(name='pygtkspellchecker',
      version=__version__,
      description='a simple but quite powerful python spell checking library for gtktextviews based on enchant',
      long_description=('PyGtkSpellCheck is a spellchecking library written in pure Python for Gtk based on Enchant.'
                        'It works with PyGObject and PyGtk and of course with Python 2 and 3 (automatic switching).'
                        'I wrote this because there was no spellchecking library for Python 3 and PyGObject before.'
                        'For automatic translation of the user interface it can use GEdit\'s translation files.'),
      author='Maximilian Köhl',
      author_email='linuxmaxi@googlemail.com',
      url='http://www.github.com/koehlma/pygtkspellcheck',
      license='GPLv3',
      packages=['gtkspellcheck', 'pylocale'],     
      package_data={'pylocale' : ['locales.db', 'locales/*/*/*']})
