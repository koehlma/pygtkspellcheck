{% names['full'] %}
{% '=' * len(names['full']) %}
{% linkify(description['long'], 'rst') %}

Features
--------
{% '- ' + '\n- '.join(features) %}

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

.. _GitHub: {% development %}

	``git clone git://github.com/koehlma/pygtkspellcheck.git``

Download last sources in a `ZIP`_ or `Tarball`_ file.

.. _ZIP: https://github.com/koehlma/pygtkspellcheck/zipball/master
.. _Tarball: https://github.com/koehlma/pygtkspellcheck/tarball/master

Website
-------
Checkout the `official project website`_ for additional information.

.. _official project website: {% homepage %}

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