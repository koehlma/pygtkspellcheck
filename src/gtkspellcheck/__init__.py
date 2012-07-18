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

import sys

try:
    from collections import UserList
    _list = UserList
except ImportError:
    _list = list
    
import gettext
import os.path
import re

import pylocale

try:
    from gi.repository import Gtk as gtk
    _gobject = True
except ImportError:
    import gtk
    _gobject = False

import enchant

__author__ = 'Maximilian Köhl'
__copyright__ = 'Copyright (C) 2012, Maximilian Köhl'
__license__ = 'GPLv3'
__version__ = '2.2.2'
__status__ = 'Production'
__all__ = ['SpellChecker']

_GEDIT_MAP = {'Languages' : 'Languages',
              'Ignore All' : 'Ignore _All',
              'Suggestions' : 'Suggestions',
              '(no suggestions)' : '(no suggested words)',
              'Add "{word}" to Dictionary' : 'Add w_ord'}

if gettext.find('gedit'):
    _gedit = gettext.translation('gedit', fallback=True).gettext
    _ = lambda message: _gedit(_GEDIT_MAP[message]).replace('_', '')
else:
    _ = gettext.translation('gtkspellcheck', os.path.join(os.path.dirname(__file__), 'locale'), fallback=True).gettext


class SpellChecker(object):
    '''
    Main spellchecking class, everything important happens here.
        
    :param view: GtkTextView the SpellChecker should be attached to
    :param language: the language which should be used for spellchecking (use codes like en_US or de_DE)
    :param prefix: a prefix for some internal GtkTextMarks
    :param params: enchant broker parameters that should be set e.g. `enchant.myspell.dictionary.path`
    
    .. attribute:: languages
        
        A list of supported languages.
        
        .. function:: exists(language)
        
            checks if a language exists
            
            :param language: language to check
    '''
    FILTER_WORD = 'word'
    FILTER_LINE = 'line'
    FILTER_TEXT = 'text'
    
    DEFAULT_FILTERS = {FILTER_WORD : [r'[0-9.,]+'],
                       FILTER_LINE : [r'(https?|ftp|file):((//)|(\\\\))+[\w\d:#@%/;$()~_?+-=\\.&]+',
                                      r'[\w\d]+@[\w\d.]+'],
                       FILTER_TEXT : []}
    
    class _LanguageList(_list):
        def __init__(self, *args, **kwargs):
            if sys.version_info.major == 3:
                super().__init__(*args, **kwargs)
            else:
                _list.__init__(self, *args, **kwargs)
            self.mapping = dict(self)
        
        @classmethod
        def from_broker(cls, broker):
            return cls([(language, pylocale.code_to_name(language))
                        for language in broker.list_languages()])
        
        def exists(self, language):
            return language in self.mapping
    
    class _Mark():
        def __init__(self, buffer, name, start):
            self._buffer = buffer
            self._name = name
            self._mark = self._buffer.create_mark(self._name, start, True)
        
        @property
        def iter(self):
            return self._buffer.get_iter_at_mark(self._mark)
        
        @property
        def inside_word(self):
            return self.iter.inside_word()            
     
        @property
        def word(self):
            start = self.iter
            if not start.starts_word():
                start.backward_word_start()
            end = self.iter
            if end.inside_word():
                end.forward_word_end()
            return start, end
        
        def move(self, location):
            self._buffer.move_mark(self._mark, location)    
    
    def __init__(self, view, language='en', prefix='gtkspellchecker', params={}):
        self._view = view
        self._view.connect('populate-popup', lambda entry, menu: self._extend_menu(menu))
        self._view.connect('popup-menu', self._click_move_popup)
        self._view.connect('button-press-event', self._click_move_button)
        self._prefix = prefix
        if _gobject:
            self._misspelled = gtk.TextTag.new('%s-misspelled' % (self._prefix))
        else:
            self._misspelled = gtk.TextTag('%s-misspelled' % (self._prefix))
        self._misspelled.set_property('underline', 4)
        self._language = language
        self._broker = enchant.Broker()
        for param, value in params: self._broker.set_param(param, value) 
        self.languages = SpellChecker._LanguageList.from_broker(self._broker)
        self._language = language if self.languages.exists(language) else 'en'
        self._dictionary = self._broker.request_dict(language)
        self._deferred_check = False
        self._filters = dict(SpellChecker.DEFAULT_FILTERS)
        self._regexes = {SpellChecker.FILTER_WORD : re.compile('|'.join(self._filters[SpellChecker.FILTER_WORD])),
                         SpellChecker.FILTER_LINE : re.compile('|'.join(self._filters[SpellChecker.FILTER_LINE])),
                         SpellChecker.FILTER_TEXT : re.compile('|'.join(self._filters[SpellChecker.FILTER_TEXT]), re.MULTILINE)}
        self._enabled = True
        self.buffer_initialize()
    
    @property
    def language(self):
        '''
        The language used for spellchecking
        '''
        return self._language
    
    @language.setter
    def language(self, language):
        if self.languages.exists(language):
            self._language = language
            self._dictionary = self._broker.request_dict(language)
            self.recheck()
    
    @property
    def enabled(self):
        '''
        Enable or disable spellchecking
        '''
        return self._enabled
    
    @enabled.setter
    def enabled(self, enabled):
        if enabled and not self._enabled:
            self.enable()
        elif not enabled and self._enabled:
            self.disable()
    
    def buffer_initialize(self):
        '''
        Initialize the GtkTextBuffer associated with the GtkTextView.
        If you associate a new GtkTextBuffer with the GtkTextView call this method.
        ''' 
        self._buffer = self._view.get_buffer()
        self._buffer.connect('insert-text', self._before_text_insert)
        self._buffer.connect_after('insert-text', self._after_text_insert)
        self._buffer.connect_after('delete-range', self._range_delete)
        self._buffer.connect_after('mark-set', self._mark_set)
        start = self._buffer.get_bounds()[0]
        self._marks = {'insert-start' : SpellChecker._Mark(self._buffer, '%s-insert-start' % (self._prefix), start),
                       'insert-end' : SpellChecker._Mark(self._buffer, '%s-insert-end' % (self._prefix), start),
                       'click' : SpellChecker._Mark(self._buffer, '%s-click' % (self._prefix), start)}
        self._table = self._buffer.get_tag_table()
        self._table.add(self._misspelled)
        self.ignored_tags = []
        def tag_added(tag, *args):
            if hasattr(tag, 'spell_check') and not getattr(tag, 'spell_check'):
                self.ignored_tags.append(tag) 
        def tag_removed(tag, *args):
            if tag in self.ignored_tags:
                self.ignored_tags.remove(tag)
        self._table.connect('tag-added', tag_added)
        self._table.connect('tag-removed', tag_removed)
        self._table.foreach(tag_added, None)
        self.no_spell_check = self._table.lookup('no-spell-check')
        if not self.no_spell_check:
            if _gobject:
                self.no_spell_check = gtk.TextTag.new('no-spell-check')
            else:
                self.no_spell_check = gtk.TextTag('no-spell-check')
            self._table.add(self.no_spell_check)
        self.recheck()
    
    def recheck(self):
        '''
        Rechecks the spelling of the whole text.
        '''
        start, end = self._buffer.get_bounds()
        self.check_range(start, end, True)
    
    def disable(self):
        '''
        Disable spellchecking.
        '''
        self._enabled = False
        start, end = self._buffer.get_bounds()
        self._buffer.remove_tag(self._misspelled, start, end)
    
    def enable(self):
        '''
        Enable spellchecking.
        '''
        self._enabled = True
        self.recheck()
    
    def append_filter(self, regex, filter_type):
        '''
        Append a new filter to the filter list.
        Filters are useful to ignore some misspelled words based on regular expressions.
              
        :param regex: the regex which used for filtering
        :param filter_type: the type of the filter
        
        Filter Types:
             
        :const:`SpellChecker.FILTER_WORD`: The regex must match the whole word you want to filter.
        The word separation is done by Pangos so for example urls won't work here because they, are separated in many words.
        
        :const:`SpellChecker.FILTER_LINE`: If the expression you want to match is a single line expression use this type.
        It should not be an open end expression because then the rest of the line with the text you want to filter become correct to.
         
        :const:`SpellChecker.FILTER_TEXT`: Use this if you want to filter multiline expressions.
        The regex will be compiled with the `MULTILINE` flag.
        Same with open end expressions here.
        '''
        self._filters[filter_type].append(regex)
        if filter_type == SpellChecker.FILTER_TEXT:
            self._regexes[filter_type] = re.compile('|'.join(self._filters[filter_type]), re.MULTILINE)
        else:
            self._regexes[filter_type] = re.compile('|'.join(self._filters[filter_type]))
    
    def remove_filter(self, regex, filter_type):
        '''
        Remove a filter from the filter list.
              
        :param regex: the regex which used for filtering
        :param filter_type: the type of the filter
        '''
        self._filters[filter_type].remove(regex)
        if filter_type == SpellChecker.FILTER_TEXT:
            self._regexes[filter_type] = re.compile('|'.join(self._filters[filter_type]), re.MULTILINE)
        else:
            self._regexes[filter_type] = re.compile('|'.join(self._filters[filter_type]))
    
    def append_ignore_tag(self, tag):
        '''
        Appends a tag to the list of ignored tags.
        A string will be automatic resolved into a tag object.
        
        :param tag: tag object or tag name
        '''
        if sys.version_info.major == 3:
            if isinstance(tag, str):
                tag = self._table.lookup(tag)
        else:
            if isinstance(tag, basestring):
                tag = self._table.lookup(tag)        
        self.ignored_tags.append(tag)
    
    def remove_ignore_tag(self, tag):
        '''
        Removes a tag from the list of ignored tags.
        A string will be automatic resolved into a tag object.
        
        :param tag: tag object or tag name
        '''
        if sys.version_info.major == 3:
            if isinstance(tag, str):
                tag = self._table.lookup(tag)
        else:
            if isinstance(tag, basestring):
                tag = self._table.lookup(tag)
        self.ignored_tags.remove(tag)
    
    def add_to_dictionary(self, word):
        '''
        Adds a word to user's dictionary.
        
        :param word: the word to add
        '''
        self._dictionary.add_to_pwl(word)
        self.recheck()
    
    def ignore_all(self, word):
        '''
        Ignores a word for the current session.
        
        :param word: the word to ignore
        '''
        self._dictionary.add_to_session(word)
        self.recheck()       
    
    def check_range(self, start, end, force_all=False):
        '''
        Checks a specified range between two GtkTextIters.
        
        :param start: start iter - checking starts here
        :param end: end iter - checking ends here
        '''
        if not self._enabled:
            return
        if end.inside_word(): end.forward_word_end()
        if not start.starts_word() and (start.inside_word() or start.ends_word()): start.backward_word_start()
        self._buffer.remove_tag(self._misspelled, start, end)
        cursor = self._buffer.get_iter_at_mark(self._buffer.get_insert())
        precursor = cursor.copy()
        precursor.backward_char()
        highlight = cursor.has_tag(self._misspelled) or precursor.has_tag(self._misspelled)
        if not start.get_offset():
            start.forward_word_end()
            start.backward_word_start()
        word_start = start.copy()
        while word_start.compare(end) < 0:
            word_end = word_start.copy()
            word_end.forward_word_end()
            in_word = (word_start.compare(cursor) < 0) and (cursor.compare(word_end) <= 0)
            if in_word and not force_all:
                if highlight:
                    self._check_word(word_start, word_end)
                else:
                    self._deferred_check = True
            else:
                self._check_word(word_start, word_end)
                self._deferred_check = False
            word_end.forward_word_end()
            word_end.backward_word_start()
            if word_start.equal(word_end):
                break
            word_start = word_end.copy() 
    
    def _languages_menu(self):
        def _set_language(item, code):
            self.language = code
        if _gobject:
            menu = gtk.Menu.new()
            group = []
        else:
            menu = gtk.Menu()
            group = gtk.RadioMenuItem()
        for code, name in self.languages:
            if _gobject:
                item = gtk.RadioMenuItem.new_with_label(group, name)
                group.append(item)
            else:
                item = gtk.RadioMenuItem(group, name)
            item.connect('activate', _set_language, code)
            if code == self.language:
                item.set_active(True)            
            menu.append(item)
        return menu
    
    def _suggestion_menu(self, word):
        if _gobject:
            menu = gtk.Menu.new()
        else:
            menu = gtk.Menu()
        suggestions = self._dictionary.suggest(word)
        if not suggestions:
            if _gobject:
                item = gtk.MenuItem.new()
                label = gtk.Label.new('')
            else:
                item = gtk.MenuItem()
                label = gtk.Label()
            try:
                label.set_halign(gtk.Align.LEFT)
            except AttributeError:
                label.set_alignment(0.0, 0.5)
            label.set_markup('<i>%s</i>' % (_('(no suggestions)')))
            item.add(label)
            menu.append(item)
        else:
            for suggestion in suggestions:
                if _gobject:
                    item = gtk.MenuItem.new()
                    label = gtk.Label.new('')
                else:
                    item = gtk.MenuItem()
                    label = gtk.Label()
                label.set_markup('<b>%s</b>' % (suggestion))
                try:
                    label.set_halign(gtk.Align.LEFT)
                except AttributeError:
                    label.set_alignment(0.0, 0.5)
                item.add(label)
                item.connect('activate', self._replace_word, word, suggestion)
                menu.append(item)
        if _gobject:
            menu.append(gtk.SeparatorMenuItem.new())
            item = gtk.MenuItem.new_with_label(_('Add "{word}" to Dictionary').format(word=word))
        else:
            menu.append(gtk.SeparatorMenuItem())
            item = gtk.MenuItem(_('Add "{word}" to Dictionary').format(word=word))
        item.connect('activate', lambda *args: self.add_to_dictionary(word))
        menu.append(item)
        if _gobject:
            item = gtk.MenuItem.new_with_label(_('Ignore All'))
        else:
            item = gtk.MenuItem(_('Ignore All'))
        item.connect('activate', lambda *args: self.ignore_all(word))
        menu.append(item)
        menu.show_all()
        return menu
    
    def _extend_menu(self, menu):
        if not self._enabled:
            return
        if _gobject:
            separator = gtk.SeparatorMenuItem.new()
        else:
            separator = gtk.SeparatorMenuItem()
        separator.show()
        menu.prepend(separator)
        if _gobject:
            languages = gtk.MenuItem.new_with_label(_('Languages'))
        else:
            languages = gtk.MenuItem(_('Languages'))
        languages.set_submenu(self._languages_menu())
        languages.show_all()
        menu.prepend(languages)
        if self._marks['click'].inside_word:
            start, end = self._marks['click'].word
            if start.has_tag(self._misspelled):
                word = self._buffer.get_text(start, end, False)
                if _gobject:
                    suggestions = gtk.MenuItem.new_with_label(_('Suggestions'))
                else:
                    suggestions = gtk.MenuItem(_('Suggestions'))
                suggestions.set_submenu(self._suggestion_menu(word))
                suggestions.show_all()
                menu.prepend(suggestions)
    
    def _click_move_popup(self, *args):
        self._marks['click'].move(self._buffer.get_iter_at_mark(self._buffer.get_insert()))
        return False
    
    def _click_move_button(self, widget, event):
        if event.button == 3:
            if self._deferred_check:  self._check_deferred_range(True)
            x, y = self._view.window_to_buffer_coords(2, int(event.x), int(event.y))
            self._marks['click'].move(self._view.get_iter_at_location(x, y))
        return False
    
    def _before_text_insert(self, textbuffer, location, text, length):
        self._marks['insert-start'].move(location)
    
    def _after_text_insert(self, textbuffer, location, text, length):
        start = self._marks['insert-start'].iter
        self.check_range(start, location)
        self._marks['insert-end'].move(location)
    
    def _range_delete(self, textbuffer, start, end):
        self.check_range(start, end)
        
    def _mark_set(self, textbuffer, location, mark):
        if mark == self._buffer.get_insert() and self._deferred_check:
            self._check_deferred_range(False)
    
    def _replace_word(self, item, old_word, new_word):
        start, end = self._marks['click'].word
        offset = start.get_offset()
        self._buffer.begin_user_action()
        self._buffer.delete(start, end)
        self._buffer.insert(self._buffer.get_iter_at_offset(offset), new_word)
        self._buffer.end_user_action()
        self._dictionary.store_replacement(old_word, new_word)
    
    def _check_deferred_range(self, force_all):
        start = self._marks['insert-start'].iter
        end = self._marks['insert-end'].iter 
        self.check_range(start, end, force_all)
            
    def _check_word(self, start, end):
        if start.has_tag(self.no_spell_check):
            return
        for tag in self.ignored_tags:
            if start.has_tag(tag):
                return
        word = self._buffer.get_text(start, end, False).strip()
        if len(self._filters[SpellChecker.FILTER_WORD]):
            if self._regexes[SpellChecker.FILTER_WORD].match(word):
                return
        if len(self._filters[SpellChecker.FILTER_LINE]):
            line_start = self._buffer.get_iter_at_line(start.get_line())
            line_end = end.copy()
            line_end.forward_to_line_end()
            line = self._buffer.get_text(line_start, line_end, False)
            for match in self._regexes[SpellChecker.FILTER_LINE].finditer(line):
                if match.start() <= start.get_line_offset() <= match.end():
                    start = self._buffer.get_iter_at_line_offset(start.get_line(), match.start())
                    end = self._buffer.get_iter_at_line_offset(start.get_line(), match.end())
                    self._buffer.remove_tag(self._misspelled, start, end)
                    return
        if len(self._filters[SpellChecker.FILTER_TEXT]):
            text_start, text_end = self._buffer.get_bounds()
            text = self._buffer.get_text(text_start, text_end, False)
            for match in self._regexes[SpellChecker.FILTER_TEXT].finditer(text):
                if match.start() <= start.get_offset() <= match.end():
                    start = self._buffer.get_iter_at_offset(match.start())
                    end = self._buffer.get_iter_at_offset(match.end())
                    self._buffer.remove_tag(self._misspelled, start, end)
                    return
        if not self._dictionary.check(word):
            self._buffer.apply_tag(self._misspelled, start, end)