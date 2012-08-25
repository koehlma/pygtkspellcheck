{% names['full'] %}
{% '=' * len(names['full']) %}
{% linkify(description['long'], 'rst') %}

Features
--------
{% '- ' + '\n- '.join(features) %}

Download
--------
Source Distribution
^^^^^^^^^^^^^^^^^^^
PyPI package available at: http://pypi.python.org/pypi/pygtkspellcheck/

    ``pip install pygtkspellcheck``

Ubuntu & Debian
^^^^^^^^^^^^^^^
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

Development
-----------
Development happens at `GitHub`_.

.. _GitHub: {% development %}

	``git clone git://github.com/koehlma/pygtkspellcheck.git``

Download last sources in a `ZIP`_ or `Tarball`_ file.

.. _ZIP: https://github.com/koehlma/pygtkspellcheck/zipball/master
.. _Tarball: https://github.com/koehlma/pygtkspellcheck/tarball/master

Website
-------
Checkout the `official project website`_.

.. _official project website: {% homepage %}.

API Reference
-------------
.. toctree::
   spellchecker

This library also includes an utility to extract Hunspell dictionary files out
of `LibreOffice .oxt extension dictionaries`_. This is especially useful for MS
Windows users because they could use the extensions to get new dictionaries.
After the dictionaries are extracted you could pass the path to the spellchecker
with the ``enchant.myspell.dictionary.path`` parameter.

.. _LibreOffice .oxt extension dictionaries: http://extensions.services.openoffice.org/dictionary

.. toctree::
   oxt_import

Examples
--------
- `PyGObject Simple Example`_
- `PyGtk Simple Example`_

.. _PyGObject Simple Example: https://github.com/koehlma/pygtkspellcheck/blob/master/examples/simple_pygobject.py
.. _PyGtk Simple Example: https://github.com/koehlma/pygtkspellcheck/blob/master/examples/simple_pygtk.py


License
-------
{% names['short'] %} is released under `GPLv3`_ or at your opinion any later version.

.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html    