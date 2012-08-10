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

# Load example if running from source, ignore this
import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '../src/'))

import locale

from gi.repository import Gtk as gtk

from gtkspellcheck import SpellChecker

if __name__ == '__main__':
    def quit(*args):
        gtk.main_quit()
        
    window = gtk.Window.new(gtk.WindowType.TOPLEVEL)
    window.set_title('PyGtkSpellCheck Example')
    view = gtk.TextView.new()
    
    spellchecker = SpellChecker(view, locale.getdefaultlocale()[0], collapse=False)
    
    for code, name in spellchecker.languages:
        print('code: %5s, language: %s' % (code, name))
    
    window.set_default_size(600, 400)
    window.add(view)
    window.show_all()
    window.connect('delete-event', quit)
    gtk.main()