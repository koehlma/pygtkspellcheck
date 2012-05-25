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

from __future__ import print_function

import locale

from gtkspellcheck import SpellChecker

try:
    from gi.repository import Gtk as gtk
    _gobject = True
except ImportError:
    import gtk
    _gobject = False

if __name__ == '__main__':
    def quit(*args):
        gtk.main_quit()
    
    if _gobject:
        window = gtk.Window.new(gtk.WindowType(0))
        view = gtk.TextView.new()
    else:
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        view = gtk.TextView()
    
    spellchecker = SpellChecker(view, locale.getdefaultlocale()[0])
        
    for code, name in spellchecker.languages:
        print('code: %5s, language: %s' % (code, name))
    
    window.set_default_size(600, 400)
    window.add(view)
    window.show_all()
    window.connect('delete-event', quit)
    gtk.main()