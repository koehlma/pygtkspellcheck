# -*- coding:utf-8 -*-

# Copyright (c) 2012 Maximilian Köhl <linuxmaxi@googlemail.com>
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

import os.path
import re
import gettext

import enchant
import pylocale

from gi.repository import Gtk as gtk


NUMBER = re.compile('[0-9.,]+')

_ = gettext.translation('gtkspellcheck', os.path.join(os.path.dirname(__file__), 'locale'), fallback=True).gettext

languages = [(language, pylocale.code_to_name(language)) for language in enchant.list_languages()]
_language_map = dict(languages)

def language_exists(language):
    return language in _language_map
    
class SpellChecker(object):
    def __init__(self, view, language='en', prefix='gtkspellchecker'):
        self._view = view
        self._view.connect('button-press-event', self._button_press_event)
        self._view.connect('populate-popup', self._populate_popup)
        self._view.connect('popup-menu', self._popup_menu)
        self._prefix = prefix
        self._misspelled = gtk.TextTag.new('%s-misspelled' % (self._prefix))
        self._misspelled.set_property('underline', 4)
        self._language = language
        self._broker = enchant.Broker()
        self._dictionary = self._broker.request_dict(language)
        self._deferred_check = False
        self._ignore_regex = re.compile('')
        self._ignore_expressions = []
        self._line_regex = re.compile('')
        self._line_expressions = []
        self.buffer_setup()
    
    @property
    def language(self):
        return self._language
    
    @language.setter
    def language(self, language):
        self._language = language
        self._dictionary = self._broker.request_dict(language)
        self.recheck_all()
    
    def append_ignore_regex(self, regex):
        self._ignore_expressions.append(regex)
        self._ignore_regex = re.compile('|'.join(self._ignore_expressions))
    
    def remove_ignore_regex(self, regex):
        self._ignore_expressions.remove(regex)
        self._ignore_regex = re.compile('|'.join(self._ignore_expressions))
    
    def append_line_regex(self, regex):
        self._line_expressions.append(regex)
        self._line_regex = re.compile('|'.join(self._line_expressions))
        
    def remove_line_regex(self, regex):
        self._line_expressions.remove(regex)
        self._line_regex = re.compile('|'.join(self._line_expressions))
    
    def recheck_all(self):
        start, end = self._buffer.get_bounds()
        self._check_range(start, end, True)
    
    def buffer_setup(self):
        self._buffer = self._view.get_buffer()
        self._buffer.connect('insert-text', self._insert_text_before)
        self._buffer.connect_after('insert-text', self._insert_text_after)
        self._buffer.connect_after('delete-range', self._delete_range_after)
        self._buffer.connect_after('mark-set', self._mark_set)
        start = self._buffer.get_bounds()[0]
        self._mark_insert_start = self._buffer.create_mark('%s-insert-start' % (self._prefix), start, True)
        self._mark_insert_end = self._buffer.create_mark('%s-insert-end' % (self._prefix), start, True)
        self._mark_click = self._buffer.create_mark('%s-click' % (self._prefix), start, True)
        self._table = self._buffer.get_tag_table()
        self._table.add(self._misspelled)
        self.recheck_all()
    
    def _ignore_all(self, item, word):
        self._dictionary.add_to_session(word)
        self.recheck_all()
    
    def _add_to_dictionary(self, item, word):
        self._dictionary.add_to_pwl(word)
        self.recheck_all()
    
    def _language_change_callback(self, item, language):
        self.language = language
    
    def _replace_word(self, item, oldword, newword):
        start, end = self._word_extents_from_mark(self._mark_click)
        offset = start.get_offset()
        self._buffer.begin_user_action()
        self._buffer.delete(start, end)
        self._buffer.insert(self._buffer.get_iter_at_offset(offset), newword)
        self._buffer.end_user_action()
        self._dictionary.store_replacement(oldword, newword)
        
    def _word_extents_from_mark(self, mark):
        start = self._buffer.get_iter_at_mark(mark)
        if not start.starts_word():
            start.backward_word_start()
        end = self._clone_iter(start)
        if end.inside_word():
            end.forward_word_end()
        return start, end
    
    def _mark_inside_word(self, mark):
        iter = self._buffer.get_iter_at_mark(mark)
        return iter.inside_word()
    
    def _build_languages_menu(self):
        menu = gtk.Menu.new()
        menu.show()
        group = []
        for code, name in languages:
            item = gtk.RadioMenuItem.new_with_label(group, name)
            item.connect('activate', self._language_change_callback, code)
            item.show()
            if code == self.language:
                item.set_active(True)
            group.append(item)
            menu.append(item)
        return menu
    
    def _build_suggestion_menu(self, word):
        menu = gtk.Menu.new()
        menu.show()
        suggestions = self._dictionary.suggest(word)
        if not suggestions:
            item = gtk.MenuItem.new()
            label = gtk.Label.new('')
            label.set_markup('<i>(%s)</i>' % (_('no suggestions')))
            item.add(label)
            menu.append(item)
        else:
            for suggestion in suggestions:
                item = gtk.MenuItem.new()
                label = gtk.Label.new('')
                label.set_markup('<b>%s</b>' % (suggestion))
                label.set_halign(gtk.Align(1))
                item.add(label)
                item.connect('activate', self._replace_word, word, suggestion)
                menu.append(item)
        menu.append(gtk.SeparatorMenuItem.new())
        item = gtk.MenuItem.new_with_label(_('Add "%s" to Dictionary') % word)
        item.connect('activate', self._add_to_dictionary, word)
        menu.append(item)
        item = gtk.MenuItem.new_with_label(_('Ignore All'))
        item.connect('activate', self._ignore_all, word)
        menu.append(item)
        menu.show_all()
        return menu
    
    def _button_press_event(self, widget, event):
        if event.button == 3:
            if self._deferred_check:
                self._check_deferred_range(True)
            x, y = self._view.window_to_buffer_coords(2, event.x, event.y)
            iter = self._view.get_iter_at_location(x, y)
            self._buffer.move_mark(self._mark_click, iter)
        return False
    
    def _populate_popup(self, entry, menu):
        separator = gtk.SeparatorMenuItem.new()
        separator.show()
        menu.prepend(separator)
        languages = gtk.MenuItem.new_with_label(_('Languages'))
        languages.set_submenu(self._build_languages_menu())
        languages.show()
        menu.prepend(languages)
        if self._mark_inside_word(self._mark_click):
            start, end = self._word_extents_from_mark(self._mark_click)
            if start.has_tag(self._misspelled):
                word = self._buffer.get_text(start, end, False)
                suggestions = gtk.MenuItem.new_with_label(_('Suggestions'))
                suggestions.set_submenu(self._build_suggestion_menu(word))
                suggestions.show()
                menu.prepend(suggestions)
    
    def _popup_menu(self, *args):
        iter = self._buffer.get_iter_at_mark(self._buffer.get_insert())
        self._buffer.move_mark(self._mark_click, iter)
        return False 
    
    def _insert_text_before(self, textbuffer, location, text, len):
        self._buffer.move_mark(self._mark_insert_start, location)
    
    def _insert_text_after(self, textbuffer, location, text, len):
        start = self._buffer.get_iter_at_mark(self._mark_insert_start)
        self._check_range(start, location);
        self._buffer.move_mark(self._mark_insert_end, location);
    
    def _delete_range_after(self, textbuffer, start, end):
        self._check_range(start, end);
    
    def _mark_set(self, textbuffer, location, mark):
        if mark == self._buffer.get_insert() and self._deferred_check:
            self._check_deferred_range(False);
    
    def _clone_iter(self, iter):
        return self._buffer.get_iter_at_offset(iter.get_offset())
        
    def _check_word(self, start, end):
        word = self._buffer.get_text(start, end, False)
        if not NUMBER.match(word) and (not self._ignore_regex.match(word) or not len(self._ignore_expressions)):
            if len(self._line_expressions):
                lstart = self._buffer.get_iter_at_line(start.get_line())
                lend = self._clone_iter(end)
                lend.forward_to_line_end()
                line = self._buffer.get_text(lstart, lend, False)
                for match in self._line_regex.finditer(line):
                    if match.start() <= start.get_line_offset() <= match.end():
                        return
            if not self._dictionary.check(word):
                self._buffer.apply_tag(self._misspelled, start, end)
    
    def _check_range(self, start, end, force_all=False):
        if end.inside_word():
            end.forward_word_end()
        if not start.starts_word():
            if start.inside_word() or start.ends_word():
                start.backward_word_start()
            else:
                if start.forward_word_end():
                    start.backward_word_start()
        cursor = self._buffer.get_iter_at_mark(self._buffer.get_insert())
        precursor = self._clone_iter(cursor)
        precursor.backward_char()
        highlight = cursor.has_tag(self._misspelled) or precursor.has_tag(self._misspelled)
        self._buffer.remove_tag(self._misspelled, start, end)
        if not start.get_offset():
            start.forward_word_end()
            start.backward_word_start()
        wstart = self._clone_iter(start)
        while wstart.compare(end) < 0:
            wend = self._clone_iter(wstart)
            wend.forward_word_end()
            inword = (wstart.compare(cursor) < 0) and (cursor.compare(wend) <= 0)
            if inword and not force_all:
                if highlight:
                    self._check_word(wstart, wend)
                else:
                    self._deferred_check = True
            else:
                self._check_word(wstart, wend)
                self._deferred_check = False
            wend.forward_word_end()
            wend.backward_word_start()
            if wstart.equal(wend):
                break
            wstart = self._clone_iter(wend) 
    
    def _check_deferred_range(self, force_all):
        start = self._buffer.get_iter_at_mark(self._mark_insert_start)
        end = self._buffer.get_iter_at_mark(self._mark_insert_end)
        self._check_range(start, end, force_all)
  