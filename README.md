## About
A simple but quite powerful spellchecking library written in pure Python for Gtk based on [Enchant](http://www.abisource.com/projects/enchant/). It supports [PyGObject](https://live.gnome.org/PyGObject/) as well as [PyGtk](http://www.pygtk.org/) for Python 2 and 3 with automatic switching and binding detection. For automatic translation of the user interface it can use Gedit’s translation files.

## Features
* localized names of the available languages
* supports word, line and multiple line ignore regular expressions
* supports ignore custom tags on GtkTextBuffer
* enable and disable of spellchecking with preferences memory
* supports hotswap of GtkTextBuffers
* PyGObject and PyGtk compatible with automatic detection
* Python 2 and 3 supportas Enchant, support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries
* extract dictionaries out of LibreOffice extension files
* legacy API for Python GtkSpell

## Documentation
The documentation is available at [Read the Docs](http://pygtkspellcheck.readthedocs.org/).

## Website
Checkout the [official project website](http://koehlma.github.com/projects/pygtkspellcheck.html).

## License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
