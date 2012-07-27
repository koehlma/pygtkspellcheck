Python GTK Spellcheck
=====================
PyGtkSpellcheck is a simple but quite powerful spellchecking library written in
pure Python for Gtk based on Enchant_. 
It supports PyGObject_ as well as PyGtk_ for Python 2 and 3 with automatic
switching and binding detection.
For automatic translation of the user interface it can use Gedit’s translation
files.

.. _Enchant: http://www.abisource.com/projects/enchant/
.. _PyGObject: https://live.gnome.org/PyGObject/
.. _PyGtk: http://www.pygtk.org/

Features
^^^^^^^^
- Localized names of the available languages.
- Supports word, line and multiline ignore regexes.
- Supports ignore custom tags on Gtk's TextBuffer.
- Enable and disable of spellchecking with preferences memory.
- Supports hotswap of Gtk's TextBuffers.
- PyGObject and PyGtk compatible with automatic detection.
- Python 2 and 3 support.
- As Enchant, support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries.


Documentation
^^^^^^^^^^^^^
You can find the documentation at `Read the Docs`_.

.. _Read the Docs: http://pygtkspellcheck.readthedocs.org/

Development
^^^^^^^^^^^
Development happens at `GitHub`_.

.. _GitHub: https://github.com/koehlma/pygtkspellcheck

License
^^^^^^^
PyGtkSpellcheck is released under `GPLv3`_ or at your opinion any later version.

.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html