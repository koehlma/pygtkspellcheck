# -*- coding:utf-8 -*-
#
# Copyright (C) 2012, Carlos Jenkins <carlos@jenkins.co.cr>
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

"""context.py: Context class for multiplatform and multilanguage applications."""

import os
import sys
import gettext
import logging

class Manager(logging.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_level = logging.WARNING
    
    def getLogger(self, name):
        if name in self.loggerDict:
            return super().getLogger(name)
        else:
            logger = super().getLogger(name)
            logger.addHandler(logging.StreamHandler()) # FIXME: Windows TODO: should not be hardcoded
            logger.setLevel(self._current_level) # TODO: should not be hardcoded
            return logger
    
    def setLevels(self, level):
        if level < logging.NOTSET or level > logging.CRITICAL: return
        self._current_level = level
        for logger in self.loggerDict.values():
            logger.setLevel(level)

# Do some monkey patching, so applications and libraries could just use the
# python standard way `logging.getLogger` and must not carry context.py to work
# correctly with it.
logging.Manager = Manager
_manager = Manager(logging.root)
logging.Logger.manager = _manager
logging.manager = _manager
logging.setLevels = _manager.setLevels

logger = logging.getLogger(__name__)

def find_where_am_i(file_var):
    """
    Allows any module to know where he is.
    $file_var must be current module __file__
    """
    frozen = getattr(sys, 'frozen', '')
    if not frozen:
        where_am_i = os.path.normpath(os.path.dirname(os.path.abspath(os.path.realpath(file_var))))
    elif frozen in ('dll', 'console_exe', 'windows_exe'):
        where_am_i = os.path.normpath(os.path.dirname(sys.executable))
    return where_am_i

class Gettext():
    _translation = gettext.translation
    def __init__(self):
        self._builder_used = False
        self._root = find_where_am_i(__file__)
        default_locale = {'linux' : '/usr/share/locale',
                          'win' : os.path.join(self._root, 'l10n')}
        self._locale_dir = default_locale['linux']
        if sys.platform.startswith('win'):
            self._locale_dir = default_locale['win']
        if os.getenv('LANG') is None:
            import locale
            lang, enc = locale.getdefaultlocale()
            os.environ['LANG'] = lang         
        
    def translation(self, domain, localedir=None, languages=None, class_=None,
                    fallback=False, codeset=None, builder=False):
        # Only one application can be 'Builder' (Application that uses GtkBuilder)
        if builder and not self._builder_used and sys.platform.startswith('win'):
            self._builder_used = True
            # Glade file translations
            try:
                import ctypes
                libintl = ctypes.cdll.LoadLibrary('intl.dll')
                libintl.bindtextdomain(domain, self._locale_dir)
                libintl.bind_textdomain_codeset(domain, 'UTF-8')
            except:
                logger.error('Error loading translations into Glade file.')
        if gettext.find(domain, self._locale_dir):
            return Gettext._translation(domain, self._locale_dir, languages, class_,
                                        True, codeset)
        return Gettext._translation(domain, localedir, languages, class_,
                                    True, codeset)
    
    def set_locale_dir(self, locale_dir):
        self._locale_dir = locale_dir

_gettext = Gettext()
gettext.translation = _gettext.translation
gettext.set_locale_dir = _gettext.set_locale_dir