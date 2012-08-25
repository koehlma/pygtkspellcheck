{% names['full'] %}
{% '=' * len(names['full']) %}
{% linkify(description['long'], 'rst') %}

Features
^^^^^^^^
{% '- ' + '\n- '.join(features) %}

Documentation
^^^^^^^^^^^^^
The documentation is available at `Read the Docs`_.

.. _Read the Docs: {% documentation %}

Development
^^^^^^^^^^^
Development happens at `GitHub`_.

.. _GitHub: {% development %}

License
^^^^^^^
{% names['short'] %} is released under `GPLv3`_ or at your opinion any later version.

.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html
