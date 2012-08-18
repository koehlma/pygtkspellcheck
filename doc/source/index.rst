Python GTK Spellcheck
=====================

PyGtkSpellCheck is a spellchecking library written in pure Python for Gtk based 
on Enchant_.
It supports both Gtk's Python bindings, PyGObject_ and PyGtk_, and for both
Python 2 and 3 with automatic switching and binding autodetection. For
automatic translation of the user interface it can use GEdit's translation
files.

.. _Enchant: http://www.abisource.com/projects/enchant/
.. _PyGObject: https://live.gnome.org/PyGObject/
.. _PyGtk: http://www.pygtk.org/


Features
--------

- Localized names of the available languages.
- Supports word, line and multiline ignore regexes.
- Supports ignore custom tags on Gtk's TextBuffer.
- Enable and disable of spellchecking with preferences memory.
- Supports hotswap of Gtk's TextBuffers.
- PyGObject and PyGtk compatible with automatic detection.
- Python 2 and 3 support.
- As Enchant, support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries.


Download
--------

Source distribution
^^^^^^^^^^^^^^^^^^^

PyPI package available at: http://pypi.python.org/pypi/pygtkspellcheck/

    ``pip install pygtkspellcheck``

Ubuntu/Debian
^^^^^^^^^^^^^

Install packages:

- Python 3:
    - https://github.com/downloads/koehlma/pygtkspellcheck/python3-gtkspellcheck_3.0-1_all.deb

- Python 2:
    - https://github.com/downloads/koehlma/pygtkspellcheck/python-gtkspellcheck_3.0-1_all.deb

- Documentation:
    - https://github.com/downloads/koehlma/pygtkspellcheck/python-gtkspellcheck-doc_3.0-1_all.deb

Archlinux
^^^^^^^^^

Available in the `Archlinux User Repository`_:

.. _Archlinux User Repository: https://aur.archlinux.org/

- Python 3:
    - ``yaourt -S python-gtkspellcheck``
    - https://aur.archlinux.org/packages.php?ID=61200
    - https://github.com/downloads/koehlma/pygtkspellcheck/python-gtkspellcheck-3.0-1-any.pkg.tar.xz

- Python 2:
    - ``yaourt -S python2-gtkspellcheck``
    - https://aur.archlinux.org/packages.php?ID=61199
    - https://github.com/downloads/koehlma/pygtkspellcheck/python2-gtkspellcheck-3.0-1-any.pkg.tar.xz

Hacking
^^^^^^^

Development repository is available at: https://github.com/koehlma/pygtkspellcheck

    ``git clone git://github.com/koehlma/pygtkspellcheck.git``

Or download last sources in a `ZIP`_ or `Tarball`_ file.

.. _ZIP: https://github.com/koehlma/pygtkspellcheck/zipball/master
.. _Tarball: https://github.com/koehlma/pygtkspellcheck/tarball/master


API Reference
-------------

The main object is called Spellchecker and can be associated with any
GtkTextView:

.. toctree::
   :maxdepth: 1

   spellchecker

This library also includes a utility module to unpack `LibreOffice .oxt
extension dictionaries`_ (Hunspell). This is especially useful for MS Windows
users to include dictionaries for this library. Use this to extract the
Hunspell dictionaries out of the extension and then pass to the Spellchecker
the path to the location of the extraction in the params argument with the key
``enchant.myspell.dictionary.path``.

.. _LibreOffice .oxt extension dictionaries: http://extensions.services.openoffice.org/dictionary

.. toctree::
   :maxdepth: 1

   oxt_import


Examples
--------

- `PyGObject Simple Example`_
- `PyGtk Simple Example`_

.. _PyGObject Simple Example: https://github.com/koehlma/pygtkspellcheck/blob/master/examples/simple_pygobject.py
.. _PyGtk Simple Example: https://github.com/koehlma/pygtkspellcheck/blob/master/examples/simple_pygtk.py


License
-------

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
