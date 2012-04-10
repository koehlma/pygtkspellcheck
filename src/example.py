# -*- coding:utf-8 -*-

import locale

from gtkspellcheck import SpellChecker, languages, language_exists
from gi.repository import Gtk as gtk

def quit(*args):
    gtk.main_quit()

for code, name in languages:
    print('code: %5s, language: %s' % (code, name))

window = gtk.Window.new(gtk.WindowType(0))
view = gtk.TextView.new()
if language_exists(locale.getdefaultlocale()[0]):
    spellchecker = SpellChecker(view, locale.getdefaultlocale()[0])
else:
    spellchecker = SpellChecker(view)

# Change TextBuffer...
buffer = gtk.TextBuffer.new(None)
view.set_buffer(buffer)
spellchecker.buffer_setup()
# Ignore URLs
spellchecker.append_line_regex('http://[a-zA-Z.0-9/]*')

window.set_default_size(600, 400)
window.add(view)
window.show_all()
window.connect('delete-event', quit)
gtk.main()