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

"""
A simple but quite powerful spellchecking library written in pure Python for Gtk
based on Enchant. It supports PyGObject as well as PyGtk for Python 2 and 3 with
automatic switching and binding detection. For automatic translation of the user
interface it can use Gedit’s translation files.
"""

import enchant
import gettext
import logging
import re
import sys
from collections import UserList

from pylocales import code_to_name as _code_to_name
from pylocales import LanguageNotFound, CountryNotFound

from gi.repository import Gio, GLib, GObject

# find any loaded gtk binding
if "gi.repository.Gtk" in sys.modules:
    gtk = sys.modules["gi.repository.Gtk"]
else:
    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk as gtk  # noqa: N813

# public objects
__all__ = ["SpellChecker", "NoDictionariesFound"]

# logger
logger = logging.getLogger(__name__)


class NoDictionariesFound(Exception):
    """
    There aren't any dictionaries installed on the current system so
    spellchecking could not work in any way.
    """


# map between Gedit's translation and PyGtkSpellcheck's
_GEDIT_MAP = {
    "Languages": "Languages",
    "Ignore All": "Ignore _All",
    "Suggestions": "Suggestions",
    "(no suggestions)": "(no suggested words)",
    'Add "{}" to Dictionary': "Add w_ord",
    "Unknown": "Unknown",
}

# translation
if gettext.find("gedit"):
    _gedit = gettext.translation("gedit", fallback=True).gettext

    def _(message):
        return _gedit(_GEDIT_MAP[message]).replace("_", "")

else:
    locale_name = "py{}gtkspellcheck".format(sys.version_info.major)
    _ = gettext.translation(locale_name, fallback=True).gettext


def code_to_name(code, separator="_"):
    try:
        return _code_to_name(code, separator)
    except (LanguageNotFound, CountryNotFound):
        return "{} ({})".format(_("Unknown"), code)


class SpellChecker(GObject.Object):
    """
    Main spellchecking class, everything important happens here.

    :param view: GtkTextView the SpellChecker should be attached to.
    :param language: The language which should be used for spellchecking.
        Use a combination of two letter lower-case ISO 639 language code with a
        two letter upper-case ISO 3166 country code, for example en_US or de_DE.
    :param prefix: A prefix for some internal GtkTextMarks.
    :param collapse: Enclose suggestions in its own menu.
    :param params: Dictionary with Enchant broker parameters that should be set
      e.g. `enchant.myspell.dictionary.path`.

    .. attribute:: languages

        A list of supported languages.

        .. function:: exists(language)

            Checks if a language exists.

            :param language: language to check
    """

    FILTER_WORD = "word"
    FILTER_LINE = "line"
    FILTER_TEXT = "text"

    DEFAULT_FILTERS = {
        FILTER_WORD: [r"[0-9.,]+"],
        FILTER_LINE: [
            (r"(https?|ftp|file):((//)|(\\\\))+[\w\d:" r"#@%/;$()~_?+-=\\.&]+"),
            r"[\w\d]+@[\w\d.]+",
        ],
        FILTER_TEXT: [],
    }

    class _LanguageList(UserList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.mapping = dict(self)

        @classmethod
        def from_broker(cls, broker):
            return cls(
                sorted(
                    [
                        (language, code_to_name(language))
                        for language in broker.list_languages()
                    ],
                    key=lambda language: language[1],
                )
            )

        def exists(self, language):
            return language in self.mapping

    class _Mark:
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

    def __init__(
        self, view, language="en", prefix="gtkspellchecker", collapse=True, params=None
    ):
        super().__init__()
        self._view = view
        self.collapse = collapse
        if gtk.MAJOR_VERSION < 4:
            self._view.connect(
                "populate-popup", lambda entry, menu: self._extend_menu(menu)
            )
            self._view.connect("popup-menu", self._click_move_popup)
            self._view.connect("button-press-event", self._click_move_button)
        self._prefix = prefix
        self._broker = enchant.Broker()
        if params is not None:
            for param, value in params.items():
                self._broker.set_param(param, value)
        self.languages = SpellChecker._LanguageList.from_broker(self._broker)
        if self.languages.exists(language):
            self._language = language
        elif self.languages.exists("en"):
            logger.warning(
                (
                    'no installed dictionary for language "{}", '
                    "fallback to english".format(language)
                )
            )
            self._language = "en"
        else:
            if self.languages:
                self._language = self.languages[0][0]
                logger.warning(
                    (
                        'no installed dictionary for language "{}" '
                        "and english, fallback to first language in"
                        'language list ("{}")'
                    ).format(language, self._language)
                )
            else:
                logger.critical("no dictionaries found")
                raise NoDictionariesFound()
        self._dictionary = self._broker.request_dict(self._language)
        self._deferred_check = False
        self._filters = dict(SpellChecker.DEFAULT_FILTERS)
        self._regexes = {
            SpellChecker.FILTER_WORD: re.compile(
                "|".join(self._filters[SpellChecker.FILTER_WORD])
            ),
            SpellChecker.FILTER_LINE: re.compile(
                "|".join(self._filters[SpellChecker.FILTER_LINE])
            ),
            SpellChecker.FILTER_TEXT: re.compile(
                "|".join(self._filters[SpellChecker.FILTER_TEXT]), re.MULTILINE
            ),
        }

        self._languages_menu = None
        if gtk.MAJOR_VERSION > 3:
            extra_menu = self._view.get_extra_menu()
            if extra_menu is None:
                extra_menu = Gio.Menu()
                self._view.set_extra_menu(extra_menu)
            self._spelling_menu = Gio.Menu()
            extra_menu.append_section(None, self._spelling_menu)

            controller = gtk.GestureClick()
            controller.set_button(0)
            controller.connect("pressed", self.__on_click_pressed)
            self._view.add_controller(controller)

            self._setup_actions()

        self._enabled = True
        self.buffer_initialize()

    @GObject.Property(type=str, default="")
    def language(self):
        """
        The language used for spellchecking.
        """
        return self._language

    @language.setter
    def language(self, language):
        if language != self._language and self.languages.exists(language):
            self._language = language
            self._dictionary = self._broker.request_dict(language)
            self.recheck()

    @GObject.Property(type=bool, default=False)
    def enabled(self):
        """
        Enable or disable spellchecking.
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        if enabled and not self._enabled:
            self.enable()
        elif not enabled and self._enabled:
            self.disable()

    def buffer_initialize(self):
        """
        Initialize the GtkTextBuffer associated with the GtkTextView. If you
        have associated a new GtkTextBuffer with the GtkTextView call this
        method.
        """
        self._misspelled = gtk.TextTag.new("{}-misspelled".format(self._prefix))
        self._misspelled.set_property("underline", 4)
        self._buffer = self._view.get_buffer()
        self._buffer.connect("insert-text", self._before_text_insert)
        self._buffer.connect_after("insert-text", self._after_text_insert)
        self._buffer.connect_after("delete-range", self._range_delete)
        self._buffer.connect_after("mark-set", self._mark_set)
        start = self._buffer.get_bounds()[0]
        self._marks = {
            "insert-start": SpellChecker._Mark(
                self._buffer, "{}-insert-start".format(self._prefix), start
            ),
            "insert-end": SpellChecker._Mark(
                self._buffer, "{}-insert-end".format(self._prefix), start
            ),
            "click": SpellChecker._Mark(
                self._buffer, "{}-click".format(self._prefix), start
            ),
        }
        self._table = self._buffer.get_tag_table()
        self._table.add(self._misspelled)
        self.ignored_tags = []

        def tag_added(tag, *args):
            if hasattr(tag, "spell_check") and not tag.spell_check:
                self.ignored_tags.append(tag)

        def tag_removed(tag, *args):
            if tag in self.ignored_tags:
                self.ignored_tags.remove(tag)

        self._table.connect("tag-added", tag_added)
        self._table.connect("tag-removed", tag_removed)
        self._table.foreach(tag_added, None)
        self.no_spell_check = self._table.lookup("no-spell-check")
        if not self.no_spell_check:
            self.no_spell_check = gtk.TextTag.new("no-spell-check")
            self._table.add(self.no_spell_check)
        self.recheck()

    def recheck(self):
        """
        Rechecks the spelling of the whole text.
        """
        start, end = self._buffer.get_bounds()
        self.check_range(start, end, True)

    def disable(self):
        """
        Disable spellchecking.
        """
        self._enabled = False
        start, end = self._buffer.get_bounds()
        self._buffer.remove_tag(self._misspelled, start, end)

    def enable(self):
        """
        Enable spellchecking.
        """
        self._enabled = True
        self.recheck()

    def append_filter(self, regex, filter_type):
        """
        Append a new filter to the filter list. Filters are useful to ignore
        some misspelled words based on regular expressions.

        :param regex: The regex used for filtering.
        :param filter_type: The type of the filter.

        Filter Types:

        :const:`SpellChecker.FILTER_WORD`: The regex must match the whole word
            you want to filter. The word separation is done by Pango's word
            separation algorithm so, for example, urls won't work here because
            they are split in many words.

        :const:`SpellChecker.FILTER_LINE`: If the expression you want to match
            is a single line expression use this type. It should not be an open
            end expression because then the rest of the line with the text you
            want to filter will become correct.

        :const:`SpellChecker.FILTER_TEXT`: Use this if you want to filter
           multiline expressions. The regex will be compiled with the
           `re.MULTILINE` flag. Same with open end expressions apply here.
        """
        self._filters[filter_type].append(regex)
        if filter_type == SpellChecker.FILTER_TEXT:
            self._regexes[filter_type] = re.compile(
                "|".join(self._filters[filter_type]), re.MULTILINE
            )
        else:
            self._regexes[filter_type] = re.compile(
                "|".join(self._filters[filter_type])
            )

    def remove_filter(self, regex, filter_type):
        """
        Remove a filter from the filter list.

        :param regex: The regex which used for filtering.
        :param filter_type: The type of the filter.
        """
        self._filters[filter_type].remove(regex)
        if filter_type == SpellChecker.FILTER_TEXT:
            self._regexes[filter_type] = re.compile(
                "|".join(self._filters[filter_type]), re.MULTILINE
            )
        else:
            self._regexes[filter_type] = re.compile(
                "|".join(self._filters[filter_type])
            )

    def append_ignore_tag(self, tag):
        """
        Appends a tag to the list of ignored tags. A string will be automatic
        resolved into a tag object.

        :param tag: Tag object or tag name.
        """
        if isinstance(tag, str):
            tag = self._table.lookup(tag)
        self.ignored_tags.append(tag)

    def remove_ignore_tag(self, tag):
        """
        Removes a tag from the list of ignored tags. A string will be automatic
        resolved into a tag object.

        :param tag: Tag object or tag name.
        """
        if isinstance(tag, str):
            tag = self._table.lookup(tag)
        self.ignored_tags.remove(tag)

    def add_to_dictionary(self, word):
        """
        Adds a word to user's dictionary.

        :param word: The word to add.
        """
        self._dictionary.add_to_pwl(word)
        self.recheck()

    def ignore_all(self, word):
        """
        Ignores a word for the current session.

        :param word: The word to ignore.
        """
        self._dictionary.add_to_session(word)
        self.recheck()

    def check_range(self, start, end, force_all=False):
        """
        Checks a specified range between two GtkTextIters.

        :param start: Start iter - checking starts here.
        :param end: End iter - checking ends here.
        """
        if not self._enabled:
            return
        if end.inside_word():
            end.forward_word_end()
        if not start.starts_word() and (start.inside_word() or start.ends_word()):
            start.backward_word_start()
        self._buffer.remove_tag(self._misspelled, start, end)
        cursor = self._buffer.get_iter_at_mark(self._buffer.get_insert())
        precursor = cursor.copy()
        precursor.backward_char()
        highlight = cursor.has_tag(self._misspelled) or precursor.has_tag(
            self._misspelled
        )
        if not start.get_offset():
            start.forward_word_end()
            start.backward_word_start()
        word_start = start.copy()
        while word_start.compare(end) < 0:
            word_end = word_start.copy()
            word_end.forward_word_end()
            in_word = (word_start.compare(cursor) < 0) and (
                cursor.compare(word_end) <= 0
            )
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

    def _setup_actions(self) -> None:
        action_group = Gio.SimpleActionGroup.new()

        action = Gio.SimpleAction.new("ignore-all", GLib.VariantType("s"))
        action.connect(
            "activate", lambda _action, word: self.ignore_all(word.get_string())
        )
        action_group.add_action(action)

        action = Gio.SimpleAction.new("add-to-dictionary", GLib.VariantType("s"))
        action.connect(
            "activate", lambda _action, word: self.add_to_dictionary(word.get_string())
        )
        action_group.add_action(action)

        action = Gio.SimpleAction.new("replace-word", GLib.VariantType("s"))
        action.connect(
            "activate",
            lambda _action, suggestion: self._replace_word(suggestion.get_string()),
        )
        action_group.add_action(action)

        language = Gio.PropertyAction.new("language", self, "language")
        action_group.add_action(language)

        self._view.insert_action_group("spelling", action_group)

    def _get_languages_menu(self):
        if gtk.MAJOR_VERSION > 3:
            if self._languages_menu is None:
                self._languages_menu = self._build_languages_menu()
            return self._languages_menu
        else:
            return self._build_languages_menu()

    def _build_languages_menu(self):
        if gtk.MAJOR_VERSION > 3:
            menu = Gio.Menu.new()
        else:

            def _set_language(item, code):
                self.language = code

            menu = gtk.Menu.new()
            group = []
            connect = []

        for code, name in self.languages:
            if gtk.MAJOR_VERSION > 3:
                item = Gio.MenuItem.new(name, None)
                item.set_action_and_target_value(
                    "spelling.language", GLib.Variant.new_string(code)
                )
                menu.append_item(item)
            else:
                item = gtk.RadioMenuItem.new_with_label(group, name)
                group.append(item)
                if code == self.language:
                    item.set_active(True)
                connect.append((item, code))
                menu.append(item)
        if gtk.MAJOR_VERSION < 4:
            for item, code in connect:
                item.connect("activate", _set_language, code)

        if gtk.MAJOR_VERSION > 3:
            return Gio.MenuItem.new_submenu(_("Languages"), menu)
        return menu

    def _suggestion_menu(self, word):
        menu = []
        suggestions = self._dictionary.suggest(word)
        if not suggestions:
            if gtk.MAJOR_VERSION < 4:
                item = gtk.MenuItem.new()
                label = gtk.Label.new("")
                try:
                    label.set_halign(gtk.Align.LEFT)
                except AttributeError:
                    label.set_alignment(0.0, 0.5)
                label.set_markup("<i>{text}</i>".format(text=_("(no suggestions)")))
                item.add(label)
                menu.append(item)
        else:
            for suggestion in suggestions:
                if gtk.MAJOR_VERSION > 3:
                    escaped = suggestion.replace("'", "\\'")
                    item = Gio.MenuItem.new(
                        suggestion, f"spelling.replace-word('{escaped}')"
                    )
                else:
                    item = gtk.MenuItem.new()
                    label = gtk.Label.new("")
                    label.set_markup("<b>{text}</b>".format(text=suggestion))
                    try:
                        label.set_halign(gtk.Align.LEFT)
                    except AttributeError:
                        label.set_alignment(0.0, 0.5)
                    item.add(label)
                    item.connect(
                        "activate", lambda *args: self._replace_word(suggestion)
                    )
                menu.append(item)
        add_to_dict_menu_label = _('Add "{}" to Dictionary').format(word)
        word_escaped = word.replace("'", "\\'")
        if gtk.MAJOR_VERSION > 3:
            item = Gio.MenuItem.new(
                add_to_dict_menu_label, f"spelling.add-to-dictionary('{word_escaped}')"
            )
        else:
            menu.append(gtk.SeparatorMenuItem.new())
            item = gtk.MenuItem.new_with_label(add_to_dict_menu_label)
            item.connect("activate", lambda *args: self.add_to_dictionary(word))
        menu.append(item)
        ignore_menu_label = _("Ignore All")
        if gtk.MAJOR_VERSION > 3:
            item = Gio.MenuItem.new(
                ignore_menu_label, f"spelling.ignore-all('{word_escaped}')"
            )
        else:
            item = gtk.MenuItem.new_with_label(ignore_menu_label)
            item.connect("activate", lambda *args: self.ignore_all(word))
        menu.append(item)
        return menu

    def _extend_menu(self, menu):
        if gtk.MAJOR_VERSION > 3:
            menu.remove_all()

        if not self._enabled:
            return

        if gtk.MAJOR_VERSION > 3:
            menu.append_item(self._get_languages_menu())
        else:
            separator = gtk.SeparatorMenuItem.new()
            separator.show()
            menu.prepend(separator)
            languages = gtk.MenuItem.new_with_label(_("Languages"))
            languages.set_submenu(self._get_languages_menu())
            languages.show_all()
            menu.prepend(languages)

        if self._marks["click"].inside_word:
            start, end = self._marks["click"].word
            if start.has_tag(self._misspelled):
                word = self._buffer.get_text(start, end, False)
                items = self._suggestion_menu(word)
                if self.collapse:
                    menu_label = _("Suggestions")
                    if gtk.MAJOR_VERSION > 3:
                        suggestions = Gio.MenuItem.new(menu_label, None)
                        submenu = Gio.Menu.new()
                    else:
                        suggestions = gtk.MenuItem.new_with_label(menu_label)
                        submenu = gtk.Menu.new()
                    for item in items:
                        if gtk.MAJOR_VERSION > 3:
                            submenu.append_item(item)
                        else:
                            submenu.append(item)
                    suggestions.set_submenu(submenu)
                    if gtk.MAJOR_VERSION > 3:
                        menu.prepend_item(suggestions)
                    else:
                        suggestions.show_all()
                        menu.prepend(suggestions)
                else:
                    items.reverse()
                    for item in items:
                        if gtk.MAJOR_VERSION > 3:
                            menu.prepend_item(item)
                        else:
                            menu.prepend(item)
                            menu.show_all()

    def _click_move_popup(self, *args):
        self._marks["click"].move(
            self._buffer.get_iter_at_mark(self._buffer.get_insert())
        )
        return False

    def _click_move_button(self, widget, event):
        if event.button == 3:
            self._move_mark_for_input(event.x, event.y)
        return False

    def _move_mark_for_input(self, input_x, input_y):
        if self._deferred_check:
            self._check_deferred_range(True)
        x, y = self._view.window_to_buffer_coords(2, int(input_x), int(input_y))
        iter = self._view.get_iter_at_location(x, y)
        if isinstance(iter, tuple):
            iter = iter[1]
        self._marks["click"].move(iter)

    def __on_click_pressed(self, click, n_press, x, y) -> None:
        # TODO this type of approach would be better (and is eg. what gnome-text-editor uses)
        #      but get_current_sequence always returns null
        # sequence = click.get_current_sequence()
        # event = click.get_last_event(sequence)
        # if n_press != 1 or not Gdk.Event.triggers_context_menu(event):
        #     return

        if n_press != 1 or click.get_current_button() != 3:
            return

        self._move_mark_for_input(x, y)
        self._extend_menu(self._spelling_menu)

    def _before_text_insert(self, textbuffer, location, text, length):
        self._marks["insert-start"].move(location)

    def _after_text_insert(self, textbuffer, location, text, length):
        start = self._marks["insert-start"].iter
        self.check_range(start, location)
        self._marks["insert-end"].move(location)

    def _range_delete(self, textbuffer, start, end):
        self.check_range(start, end)

    def _mark_set(self, textbuffer, location, mark):
        if mark == self._buffer.get_insert() and self._deferred_check:
            self._check_deferred_range(False)

    def _replace_word(self, new_word):
        start, end = self._marks["click"].word
        old_word = start.get_text(end)
        offset = start.get_offset()
        self._buffer.begin_user_action()
        self._buffer.delete(start, end)
        self._buffer.insert(self._buffer.get_iter_at_offset(offset), new_word)
        self._buffer.end_user_action()
        self._dictionary.store_replacement(old_word, new_word)

    def _check_deferred_range(self, force_all):
        start = self._marks["insert-start"].iter
        end = self._marks["insert-end"].iter
        self.check_range(start, end, force_all)

    def _check_word(self, start, end):
        if start.has_tag(self.no_spell_check):
            return
        for tag in self.ignored_tags:
            if start.has_tag(tag):
                return
        word = self._buffer.get_text(start, end, False).strip()
        if not word:
            return
        if len(self._filters[SpellChecker.FILTER_WORD]):
            if self._regexes[SpellChecker.FILTER_WORD].match(word):
                return
        if len(self._filters[SpellChecker.FILTER_LINE]):
            if gtk.MAJOR_VERSION > 3:
                _success, line_start = self._buffer.get_iter_at_line(start.get_line())
            else:
                line_start = self._buffer.get_iter_at_line(start.get_line())
            line_end = end.copy()
            line_end.forward_to_line_end()
            line = self._buffer.get_text(line_start, line_end, False)
            for match in self._regexes[SpellChecker.FILTER_LINE].finditer(line):
                if match.start() <= start.get_line_offset() <= match.end():
                    if gtk.MAJOR_VERSION > 3:
                        _success, start = self._buffer.get_iter_at_line_offset(
                            start.get_line(), match.start()
                        )
                        _success, end = self._buffer.get_iter_at_line_offset(
                            start.get_line(), match.end()
                        )
                    else:
                        start = self._buffer.get_iter_at_line_offset(
                            start.get_line(), match.start()
                        )
                        end = self._buffer.get_iter_at_line_offset(
                            start.get_line(), match.end()
                        )
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
