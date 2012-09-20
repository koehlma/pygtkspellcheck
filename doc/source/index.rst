Python GTK Spellchecker
=======================
A simple but quite powerful spellchecking library written in pure Python for Gtk based on `Enchant`_. It supports `PyGObject`_ as well as `PyGtk`_ for Python 2 and 3 with automatic switching and binding detection. For automatic translation of the user interface it can use Gedit’s translation files.

.. _PyGObject: https://live.gnome.org/PyGObject/
.. _Enchant: http://www.abisource.com/projects/enchant/
.. _PyGtk: http://www.pygtk.org/

Features
--------
- localized names of the available languages
- supports word, line and multiple line ignore regular expressions
- supports ignore custom tags on GtkTextBuffer
- enable and disable of spellchecking with preferences memory
- supports hotswap of GtkTextBuffers
- PyGObject and PyGtk compatible with automatic detection
- Python 2 and 3 supportas Enchant, support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries
- extract dictionaries out of LibreOffice extension files
- legacy API for Python GtkSpell

API Reference
-------------
.. autoclass:: gtkspellcheck.spellcheck.SpellChecker
   :members:
   
.. autoclass:: gtkspellcheck.spellcheck.NoDictionariesFound

.. autoclass:: gtkspellcheck.spellcheck.NoGtkBindingFound
	
.. autofunction:: pylocales.code_to_name

.. autofunction:: gtkspellcheck.oxt_extract.extract

.. autofunction:: gtkspellcheck.oxt_extract.batch_extract

.. autoclass:: gtkspellcheck.oxt_extract.BadXml

.. autoclass:: gtkspellcheck.oxt_extract.BadExtensionFile

.. autoclass:: gtkspellcheck.oxt_extract.ExtractPathIsNoDirectory

Development
-----------
Development happens at `GitHub`_.

.. _GitHub: https://github.com/koehlma/pygtkspellcheck

	``git clone git://github.com/koehlma/pygtkspellcheck.git``

Download last sources in a `ZIP`_ or `Tarball`_ file.

.. _ZIP: https://github.com/koehlma/pygtkspellcheck/zipball/master
.. _Tarball: https://github.com/koehlma/pygtkspellcheck/tarball/master

Website
-------
Checkout the `official project website`_ for additional information.

.. _official project website: http://koehlma.github.com/projects/pygtkspellcheck.html

Examples
--------
- `PyGObject Simple Example`_
- `PyGtk Simple Example`_

.. _PyGObject Simple Example: https://github.com/koehlma/pygtkspellcheck/blob/master/examples/simple_pygobject.py
.. _PyGtk Simple Example: https://github.com/koehlma/pygtkspellcheck/blob/master/examples/simple_pygtk.py


License
-------
PyGtkSpellcheck is released under `GPLv3`_ or at your opinion any later version.

.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html    