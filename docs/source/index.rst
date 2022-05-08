Python GTK Spellcheck
=====================

Python GTK Spellcheck is a simple but quite powerful spellchecking library for GTK written in pure Python. It's spellchecking component is based on Enchant_ and it supports both GTK 3 and 4 via PyGObject_.

.. _Enchant: http://www.abisource.com/projects/enchant/
.. _PyGObject: https://live.gnome.org/PyGObject/
.. _ISO-Codes: http://pkg-isocodes.alioth.debian.org/

Features
--------
- **spellchecking** based on Enchant_ for `GtkTextViews`
- support for word, line and multiple line **ignore regular expressions**
- support for both **GTK 3 or 4** via PyGObject_ for Python 3
- localized names of the available languages based on ISO-Codes_
- support for custom ignore tags and hot swap of `GtkTextBuffers`
- enable and disable of spellchecking with preferences memory
- support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries
- supports extraction of dictionaries out of LibreOffice extension files


Automatic Version Detection
---------------------------

Python GTK Spellcheck will automatically detect the version of GKT (3 or 4) used by your project. To this end, you have to import GTK before importing `gtkspellcheck`. For example:


.. code-block::
   
   import gi

   gi.require_version("Gtk", "4.0")
   from gi.repository import Gtk

   from gtkspellcheck import SpellChecker


Python GTK Spellcheck will configure itself to use GTK 4 for the example above.


API Reference
-------------
.. autoclass:: gtkspellcheck.spellcheck.SpellChecker
   :members:
   
.. autoclass:: gtkspellcheck.spellcheck.NoDictionariesFound


Deprecated API Reference
------------------------
.. warning::

   The following functions are deprecated since version 4.0.5, they will be removed
   from "pygtkspellcheck" in 5.0.


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
