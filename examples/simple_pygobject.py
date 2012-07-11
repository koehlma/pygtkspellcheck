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

import locale

# PyGObject example
from gi.repository import Gtk

from gtkspellcheck import SpellChecker

if __name__ == '__main__':
    def quit(*args):
        Gtk.main_quit()
        
    window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
    view = Gtk.TextView.new()
    
    spellchecker = SpellChecker(view, locale.getdefaultlocale()[0])
    
    for code, name in spellchecker.languages:
        print('code: %5s, language: %s' % (code, name))
    
    window.set_default_size(600, 400)
    window.add(view)
    window.show_all()
    window.connect('delete-event', quit)
    Gtk.main()
