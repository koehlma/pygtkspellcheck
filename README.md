# Python GTK Spellcheck

[![PyPi Project Page](https://img.shields.io/pypi/v/pygtkspellcheck.svg?style=flat-square&label=latest%20version)](https://pypi.python.org/pypi/pygtkspellcheck)
[![Documentation](https://readthedocs.org/projects/pygtkspellcheck/badge/?version=latest&style=flat-square)](https://pygtkspellcheck.readthedocs.org/en/latest/)

Python GTK Spellcheck is a simple but quite powerful spellchecking library for GTK written in pure Python. It's spellchecking component is based on [Enchant](http://www.abisource.com/projects/enchant/) and it supports both GTK 3 and 4 via [PyGObject](https://live.gnome.org/PyGObject/).


## ✨ Features

- **spellchecking** based on [Enchant](http://www.abisource.com/projects/enchant/) for `GtkTextView`
- support for word, line, and multiple line **ignore regular expressions**
- support for both **GTK 3 and 4** via [PyGObject](https://live.gnome.org/PyGObject/) for Python 3
- localized names of the available languages based on [ISO-Codes](http://pkg-isocodes.alioth.debian.org/)
- support for custom ignore tags and hot swap of `GtkTextBuffer`
- support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries

<p align="center">
  <img src="https://raw.githubusercontent.com/koehlma/pygtkspellcheck/master/docs/screenshots/screenshot.png" alt="Screenshot" />
</p>


## 🚀 Getting Started

Python GTK Spellcheck is available from the [Python Package Index](https://pypi.python.org/pypi/pygtkspellcheck):
```sh
pip install pygtkspellcheck
```
Depending on your distribution, you may also find Python GTK Spellcheck in your package manager.
For instance, on Debian you may want to install [`python3-gtkspellcheck`](https://packages.debian.org/bullseye/python3-gtkspellcheck) package.


## 🥳 Showcase

Over time, several project have used Python GTK Spellcheck or are still using it. Among those are:

- [Nested Editor](http://nestededitor.sourceforge.net/about.html): “Specialized editor for structured documents.”
- [Cherry Tree](http://www.giuspen.com/cherrytree/): “A hierarchical note taking application, […].”
- [Zim](http://zim-wiki.org/): “Zim is a graphical text editor used to maintain a collection of wiki pages.”
- [REMARKABLE](http://remarkableapp.github.io/): “The best markdown editor for Linux and Windows.”
- [RedNotebook](http://rednotebook.sourceforge.net/): “RedNotebook is a modern journal.”
- [Reportbug](https://packages.debian.org/stretch/reportbug): “Reports bugs in the Debian distribution.”
- [UberWriter](http://uberwriter.wolfvollprecht.de/): “UberWriter is a writing application for markdown.”
- [Gourmet](https://github.com/thinkle/gourmet): “Gourmet Recipe Manager is a manager, editor, and organizer for recipes.“


## 🔖 Versions

Version numbers follow [Semantic Versioning](http://semver.org/). However, the version change from 3 to 4 pertains only API incompatible changes in `oxt_extract` and not the spellchecking component.


## 📚 Documentation

The documentation is available at [Read the Docs](http://pygtkspellcheck.readthedocs.org/).


## 🏗 Contributing

We welcome all kinds of contributions! ❤️

For minor changes and bug fixes feel free to simply open a pull request. For major changes impacting the overall design of Python GTK Spellcheck, please first [start a discussion](https://github.com/koehlma/pygtkspellcheck/discussions/new?category=ideas) outlining your idea.
