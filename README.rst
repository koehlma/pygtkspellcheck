Python GTK Spellcheck
=====================

|pypi| |docs|

Python GTK Spellcheck is a simple but quite powerful spellchecking library for GTK written
in pure Python. It's spellchecking component is based on Enchant_ and it supports both GTK
bindings (PyGObject_, PyGTK_) as well as Python 3 and 2.


Features
--------
- **spellchecking** based on Enchant_ for `GtkTextViews`
- support for word, line and multiple line **ignore regular expressions**
- PyGObject_ and PyGtk_ (automatic detection) as well as Python 3 and 2 compatible
- localized names of the available languages based on ISO-Codes_
- support for custom ignore tags and hot swap of `GtkTextBuffers`
- enable and disable of spellchecking with preferences memory
- support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries
- supports extraction of dictionaries out of LibreOffice extension files
- legacy API for Python GtkSpell

.. image:: https://raw.githubusercontent.com/koehlma/pygtkspellcheck/master/doc/screenshots/screenshot.png
    :alt: Python GTK Spellcheck Screenshot
    :align: center

.. _Enchant: http://www.abisource.com/projects/enchant/
.. _PyGObject: https://live.gnome.org/PyGObject/
.. _PyGTK: http://www.pygtk.org/
.. _ISO-Codes: http://pkg-isocodes.alioth.debian.org/


Versions
--------
Version numbers follow `Semantic Versioning`_. However version change from 3 to 4 pertains
only API incompatible changes in `oxt_extract` and not the spellchecking component.

.. _Semantic Versioning: http://semver.org/


Documentation
-------------
The documentation is available at `Read the Docs`_.

.. _Read the Docs: http://pygtkspellcheck.readthedocs.org/


.. |pypi| image:: https://img.shields.io/pypi/v/pygtkspellcheck.svg?style=flat-square&label=latest%20version
    :target: https://pypi.python.org/pypi/pygtkspellcheck

.. |docs| image:: https://readthedocs.org/projects/pygtkspellcheck/badge/?version=latest&style=flat-square
    :target: https://pygtkspellcheck.readthedocs.org/en/latest/
