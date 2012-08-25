oxt_extract reference
=====================

This library also includes an utility to extract Hunspell dictionary files out
of `LibreOffice .oxt extension dictionaries`_. This is especially useful for MS
Windows users because they could use the extensions to get new dictionaries.
After the dictionaries are extracted you could pass the path to the spellchecker
with the ``enchant.myspell.dictionary.path`` parameter.

.. _LibreOffice .oxt extension dictionaries: http://extensions.services.openoffice.org/dictionary

.. autofunction:: gtkspellcheck.oxt_extract.extract
