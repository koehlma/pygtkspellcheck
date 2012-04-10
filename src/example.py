# -*- coding:utf-8 -*-

from __future__ import print_function

import locale

from gtkspellcheck import SpellChecker
from gi.repository import Gtk as gtk

def quit(*args):
    gtk.main_quit()

window = gtk.Window.new(gtk.WindowType(0))
view = gtk.TextView.new()
spellchecker = SpellChecker(view, locale.getdefaultlocale()[0])
    
for code, name in spellchecker.languages:
    print('code: %5s, language: %s' % (code, name))

window.set_default_size(600, 400)
window.add(view)
window.show_all()
window.connect('delete-event', quit)
gtk.main()