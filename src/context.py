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

"""
Context module for multiplatform and multilanguage applications. It uses monkey
patching to support modules written for the standard library. Modules just use
`logging.getLogger` and `gettext.translation` and this modules cares about
setting the right handlers and levels for logging as well as the searching paths
for translation files. It also provides a `os.path.get_data_path` function to
let modules know where they could find their data.
"""

import gettext
import logging
import os
import os.path
import sys

# Public Objects
__all__ = ['getLogger', 'get_logger', 'setLevels', 'set_levels', 'Gettext',
           'translation', 'set_locale_dir', 'get_data_path']

# Save the old `logging.Manager` and the old `gettext.translation`.
logging._OldManager = logging.Manager
gettext._old_translation = gettext.translation

# New manager for logging which supports a setLevels method to set the same
# levels to all loggers requested with `logging.getLogger`.
class Manager(logging.Manager):
    def __init__(self, *args, **kwargs):
        logging._OldManager.__init__(self, *args, **kwargs)
        self._current_level = logging.WARNING
    
    def getLogger(self, name):
        if name in self.loggerDict:
            return logging._OldManager.getLogger(self, name)
        else:
            logger = logging._OldManager.getLogger(self, name)
            # FIXME: Windows TODO: should not be hardcoded
            logger.addHandler(logging.StreamHandler())
            # TODO: should not be hardcoded
            logger.setLevel(self._current_level) 
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

getLogger = _manager.getLogger
get_logger = getLogger # PEP 8
setLevels = _manager.setLevels
set_levels = setLevels # PEP 8

# logging for the rest of the module
logger = logging.getLogger(__name__)


# Monkey patch a `os.path.get_data_path` function to allow applications that
# support this monkey patch locate the directory where static data is located.
# The default behavior is to return the directory where the requesting source
# file is located. If this is not possible because of a frozen environment
# (py2exe for example) it returns the path where the exe or dll is located.
def get_data_path(file_var):
    """
    Allows any module to know where to find his data also for frozen
    environments. The `file_var` must be the current module's `__file__`.
    """
    frozen = getattr(sys, 'frozen', '')
    if not frozen:
        return os.path.normpath(os.path.dirname(os.path.abspath(os.path.realpath(file_var))))
    elif frozen in ('dll', 'console_exe', 'windows_exe'):
        return os.path.normpath(os.path.dirname(sys.executable))
    
os.path.get_data_path = get_data_path

# A new `gettext.translation` function that cares about the localedir for every
# application that uses it. So a default path for all translation files could be
# given. Also the `fallback` argument would be `True` for every translation.
class Gettext():
    BUILDER_USED = False # Only one translation could use GtkBuilder
    ROOT = get_data_path(__file__)
    DEFAULT_LOCALE = 'default' # if domain is `None`. This is not compatible
                               # with the python standard library. So then
                               # context.py is required.
    DEFAULT_DIRS = {'linux' : '/usr/share/locale',
                    'windows' : os.path.join(ROOT, 'l10n')}
    LOCALE_DIR = DEFAULT_DIRS['linux']
    if sys.platform.startswith('win'):
        LOCALE_DIR = DEFAULT_DIRS['windows']   
        
    def translation(self, domain=None, localedir=None, languages=None, class_=None,
                    fallback=False, codeset=None, builder=False):
        domain = Gettext.DEFAULT_LOCALE if domain is None else domain
        logger.debug('requesting translation for domain "{}"'.format(domain))
        # Only one application can be 'Builder' (Application that uses GtkBuilder)
        if builder and not Gettext.BUILDER_USED and sys.platform.startswith('win'):
            self._builder_used = True
            # Glade file translations
            try:
                import ctypes
                libintl = ctypes.cdll.LoadLibrary('intl.dll')
                libintl.bindtextdomain(domain, Gettext.LOCALE_DIR)
                libintl.bind_textdomain_codeset(domain, 'utf-8')
            except:
                logger.error('Error loading translations into Glade file.')
        # search in default locale directory first
        if gettext.find(domain, Gettext.LOCALE_DIR):
            return gettext._old_translation(domain, Gettext.LOCALE_DIR, languages, class_,
                                            True, codeset)
        # then in given locale directory
        return gettext._old_translation(domain, localedir, languages, class_,
                                        True, codeset)
    
    def set_locale_dir(self, locale_dir):
        Gettext.LOCALE_DIR = locale_dir

# Do some monkey patching, so applications and libraries could just use the
# python standard way `gettext.translation` and must not carry context.py to
# work correctly with it.
_gettext = Gettext()
gettext.translation = _gettext.translation
gettext.set_locale_dir = _gettext.set_locale_dir

translation = _gettext.translation
set_locale_dir = _gettext.set_locale_dir

# setting LANG environment variable if not already set
if os.getenv('LANG') is None:
    import locale
    lang, enc = locale.getdefaultlocale()
    os.environ['LANG'] = lang