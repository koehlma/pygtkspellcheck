# -*- coding:utf-8 -*-
#
# Copyright (C) 2012, Maximilian Köhl <linuxmaxi@googlemail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import re

__path__ = os.path.dirname(__file__)

names = {'full': 'Python GTK Spellchecker',
         'short': 'PyGtkSpellcheck',
         'url': 'pygtkspellcheck'}

features = ['localized names of the available languages',
            'supports word, line and multiple line ignore regular expressions',
            'supports ignore custom tags on GtkTextBuffer',
            'enable and disable of spellchecking with preferences memory',
            'supports hotswap of GtkTextBuffers',
            'PyGObject and PyGtk compatible with automatic detection',
            'Python 2 and 3 support'
            'as Enchant, support for Hunspell (LibreOffice) and Aspell (GNU) dictionaries',
            'extract dictionaries out of LibreOffice extension files',
            'legacy API for Python GtkSpell']

description = {'short': 'a simple but quite powerful Python spell checking library for GtkTextViews based on Enchant',
               'long': ('A simple but quite powerful spellchecking library written '
                        'in pure Python for Gtk based on Enchant. It supports PyGObject '
                        'as well as PyGtk for Python 2 and 3 with automatic switching '
                        'and binding detection. For automatic translation of the user '
                        'interface it can use Gedit’s translation files.')}

screenshot = os.path.join(__path__, 'screenshot.png')

development = 'https://github.com/koehlma/pygtkspellcheck'

documentation = 'http://pygtkspellcheck.readthedocs.org/'

homepage = 'http://koehlma.github.com/projects/pygtkspellcheck.html'

links = {'Enchant': 'http://www.abisource.com/projects/enchant/',
         'PyGObject': 'https://live.gnome.org/PyGObject/',
         'PyGtk': 'http://www.pygtk.org/'}

with open(os.path.join(__path__, 'readme.md'), 'rb') as _readme:
    readme = _readme.read().decode('utf-8')
    
with open(os.path.join(__path__, 'pypi.rst'), 'rb') as _pypi:
    pypi = _pypi.read().decode('utf-8')
    
with open(os.path.join(__path__, 'documentation.rst'), 'rb') as _documentation:
    docs = _documentation.read().decode('utf-8')

with open(os.path.join(__path__, 'website.md'), 'rb') as _website:
    website = _website.read().decode('utf-8')

replace = re.compile('\{%\s*(.+?)\s*%\}')

def linkify(text, format):
    if format == 'markdown':
        for name, url in links.items():
            text = text.replace(name, '[{}]({})'.format(name, url))
    elif format == 'rst':
        for name in links:
            text = text.replace(name, '`{}`_'.format(name))
        text += '\n'
        for name, url in links.items():
            if text.find(name) > -1:
                text += '\n.. _{}: {}'.format(name, url)            
    return text

def template(match):
    code = match.group(1)
    return str(eval(code))    

if __name__ == '__main__':
    print('creating readme')
    with open(os.path.join(__path__, '..', '..', 'README.md'), 'wb') as _readme:
        _readme.write(replace.sub(template, readme).encode('utf-8'))
    print('creating pypi')
    with open(os.path.join(__path__, '..', 'pypi', 'page.rst'), 'wb') as _pypi:
        _pypi.write(replace.sub(template, pypi).encode('utf-8'))
    print('creating documentation')
    with open(os.path.join(__path__, '..', 'source', 'index.rst'), 'wb') as _documentation:
        _documentation.write(replace.sub(template, docs).encode('utf-8'))
    koehlma_github = os.path.join(__path__, '..', '..', '..', 'koehlma.github.com')
    if os.path.exists(koehlma_github):
        print('creating website')
        with open(os.path.join(koehlma_github, 'projects', 'pygtkspellcheck.md'), 'wb') as _website:
            _website.write(replace.sub(template, website).encode('utf-8'))