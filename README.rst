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


Showcase
--------
- `Nested Editor`_: “Specialized editor for structured documents.”
- `Cherry Tree`_: “A hierarchical note taking application, […].”
- `Zim`_: “Zim is a graphical text editor used to maintain a collection of wiki pages.”
- `REMARKABLE`_: “The best markdown editor for Linux and Windows.”
- `RedNotebook`_: “RedNotebook is a modern journal.”
- `Reportbug`_: “Reports bugs in the Debian distribution.”
- `UberWriter`_: “UberWriter is a writing application for markdown.”

.. _Nested Editor: http://nestededitor.sourceforge.net/about.html
.. _Cherry Tree: http://www.giuspen.com/cherrytree/
.. _Zim: http://zim-wiki.org/
.. _REMARKABLE: http://remarkableapp.github.io/
.. _RedNotebook: http://rednotebook.sourceforge.net/
.. _Reportbug: https://packages.debian.org/stretch/reportbug
.. _UberWriter: http://uberwriter.wolfvollprecht.de/


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
