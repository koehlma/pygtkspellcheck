---
layout: default
title: Python GTK Spellchecker
repository: pygtkspellcheck
downloads:
- class: archlinux
  url: https://github.com/downloads/koehlma/pygtkspellcheck/python-gtkspellcheck-3.0-1-any.pkg.tar.xz
  text: Python 3
- class: archlinux
  url: https://github.com/downloads/koehlma/pygtkspellcheck/python2-gtkspellcheck-3.0-1-any.pkg.tar.xz
  text: Python 2
- class: debian
  url: https://github.com/downloads/koehlma/pygtkspellcheck/python3-gtkspellcheck_3.0-1_all.deb
  text: Python 3
- class: debian
  url: https://github.com/downloads/koehlma/pygtkspellcheck/python-gtkspellcheck_3.0-1_all.deb
  text: Python 2
---

{% linkify(description['long'], 'markdown') %}

# Features
{% '* ' + '\n* '.join(features) %}

# Screenshots
![Screenshot](/projects/pygtkspellcheck/screenshot.png)

## Documentation
The documentation is available at [Read the Docs]({% documentation %}).

# Examples
* [PyGObject Simple Example](https://github.com/koehlma/pygtkspellcheck/blob/master/examples/simple_pygobject.py)
* [PyGtk Simple Example](https://github.com/koehlma/pygtkspellcheck/blob/master/examples/simple_pygtk.py)

# Distribution
## Cheeseshop
PyPI package is available at: http://pypi.python.org/pypi/pygtkspellcheck/

    pip install pygtkspellcheck

## Archlinux - AUR
### Python 3
* `yaourt -S python-gtkspellcheck`
* [AUR Package](https://aur.archlinux.org/packages.php?ID=61200)

### Python 2
* `yaourt -S python2-gtkspellcheck`
* [AUR Package](https://aur.archlinux.org/packages.php?ID=61199)
