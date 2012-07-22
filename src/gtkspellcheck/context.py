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

# Expose
__all__ = ['AppContext']

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
manager = Manager(logging.root)
logging.Logger.manager = manager
logging.manager = manager
logging.setLevels = manager.setLevels

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

class AppContext(object):
    """
    Context for a particular application.
    """

    LOGGER_DEBUG = logging.DEBUG

    ROOT = find_where_am_i(__file__)
    DEFAULT_LOCALE = {'linux' : '/usr/share/locale',
                      'win'   : os.path.join(ROOT, 'l10n')}
    LOCALE_DIR = DEFAULT_LOCALE['linux']
    DEFAULT_APP = 'default'
    
    _instances = {}
    _builder_used = False

    def __new__(cls, app=DEFAULT_APP, builder=False):
        """
        Singleton map kind of factory sort stuff :P
        """
        if not app in AppContext._instances.keys():
            logger.debug('Creating context: ' + app)
            AppContext._instances[app] = super(AppContext, cls).__new__(cls)
        return AppContext._instances[app]

    def __init__(self, app=DEFAULT_APP, builder=False):
        """
        Start environment for given application.
        """
        
        self.APP = app

        # Only one application can be 'Builder' (Application that uses GtkBuilder)
        if builder and not AppContext._builder_used and sys.platform.startswith('win'):
            AppContext._builder_used = True
            # Glade file translations
            try:
                import ctypes
                libintl = ctypes.cdll.LoadLibrary('intl.dll')
                libintl.bindtextdomain(self.APP, AppContext.LOCALE_DIR)
                libintl.bind_textdomain_codeset(self.APP, 'UTF-8')
            except:
                logger.error('Error loading translations into Glade file.')

        self._translation = gettext.translation(self.APP, AppContext.LOCALE_DIR, fallback=True)
        self._ = self._translation.gettext

    def what_do_i_speak(self):
        """
        Allows all modules to share a common translation context.
        """
        return self._

    @classmethod
    def where_am_i(cls, file_var):
        """
        find_where_am_i() wrapper in case user only imports AppContext class.
        """
        return find_where_am_i(file_var)

    @classmethod
    def get_logger(cls, logger_name):
        """
        get_logger() wrapper in case user only imports AppContext class.
        """
        return logging.getLogger(logger_name)

    @classmethod
    def set_logger_level(cls, level):
        """
        set_logger_level() wrapper in case user only imports AppContext class.
        """
        return logging.setLevels(level)

# Hack for MS Windows
if sys.platform.startswith('win'):
    # Set $LANG on MS Windows for gettext
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang
    # Set LOCALE_DIR for MS Windows
    AppContext.LOCALE_DIR = AppContext.DEFAULT_LOCALE['win']