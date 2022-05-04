Python GTK Spellchecker
=======================
A simple but quite powerful spellchecking library written in pure Python for Gtk based on `Enchant`_. It supports `PyGObject`_ as well as `PyGtk`_ for Python 2 and 3 with automatic switching and binding detection. For automatic translation of the user interface it can use Gedit’s translation files.

.. _PyGObject: https://live.gnome.org/PyGObject/
.. _Enchant: http://www.abisource.com/projects/enchant/
.. _PyGtk: http://www.pygtk.org/

Features
========
- localized names of the available languages
- supports word, line and multiple line ignore regular expressions
- supports ignore custom tags on GtkTextBuffer
- enable and disable of spellchecking with preferences memory
- supports hotswap of GtkTextBuffers
- PyGObject and PyGtk compatible with automatic detection
- Python 2 and 3 supportas Enchant, support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries
- extract dictionaries out of LibreOffice extension files
- legacy API for Python GtkSpell

Documentation
=============
The documentation is available at `Read the Docs`_.

.. _Read the Docs: http://pygtkspellcheck.readthedocs.org/

Distribution
============
Cheeseshop
^^^^^^^^^^
`PyPI package`_ is available:

.. _PyPI package: http://pypi.python.org/pypi/pygtkspellcheck/

::

    pip install pygtkspellcheck

Archlinux - AUR
^^^^^^^^^^^^^^^
Python 3
--------

::

    pacman -S python-gtkspellcheck

Python 2
--------

::

    pacman -S python2-gtkspellcheck

Ubuntu / Debian
^^^^^^^^^^^^^^^
Python 2
--------

::
    
    sudo apt-get install python-gtkspellcheck

Python 3
--------

::

    sudo apt-get install python3-gtkspellcheck

Development
^^^^^^^^^^^
Development happens at `GitHub`_.

.. _GitHub: https://github.com/koehlma/pygtkspellcheck

License
^^^^^^^
PyGtkSpellcheck is released under `GPLv3`_ or at your opinion any later version.

.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html
