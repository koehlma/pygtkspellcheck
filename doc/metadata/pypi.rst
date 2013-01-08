{% names['full'] %}
{% '=' * len(names['full']) %}
{% linkify(description['long'], 'rst') %}

Features
========
{% '- ' + '\n- '.join(features) %}

Documentation
=============
The documentation is available at `Read the Docs`_.

.. _Read the Docs: {% documentation %}

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
Ubuntu - Repository
-------------------

::

    sudo add-apt-repository ppa:koehlma/packages
    sudo apt-get update

Debian - Repository
-------------------

::

    sudo su
    echo "deb http://ppa.launchpad.net/koehlma/packages/ubuntu precise main" >> /etc/apt/sources.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 775B7DF6
    apt-get update

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

.. _GitHub: {% development %}

License
^^^^^^^
{% names['short'] %} is released under `GPLv3`_ or at your opinion any later version.

.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html
