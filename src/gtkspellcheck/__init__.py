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

# Python 2/3 compat
import sys
if sys.version_info.major == 3:
    u = lambda x: x
else:
    u = lambda x: x.decode('UTF-8')

# Metadata
__version__    = '2.5'
__project__    = 'Python GTK Spellcheck'
__short_name__ = 'pygtkspellcheck'
__authors__    = u('Maximilian Köhl & Carlos Jenkins')
__emails__     = u('linuxmaxi@googlemail.com & carlos@jenkins.co.cr')
__website__    = 'http://pygtkspellcheck.readthedocs.org/'
__copyright__  = u('2012, Maximilian Köhl & Carlos Jenkins')
__desc_short__ = 'A spellchecking library written in pure Python for Gtk based on Enchant'
__desc_long__  =  \
"""\
It supports both Gtk's Python bindings, PyGObject and PyGtk, and for both Python \
2 and 3 with automatic switching and binding autodetection. For automatic \
translation of the user interface it can use GEdit's translation files.\
"""

try:
    from .spellcheck import SpellChecker
except Exception as exc:
    print(exc)

