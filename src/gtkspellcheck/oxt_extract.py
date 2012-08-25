# -*- coding:utf-8 -*-
#
# Copyright (C) 2012, Carlos Jenkins <carlos@jenkins.co.cr>
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

"""
This module extracts the .dic and .aff (Hunspell) dictionaries from any given 
.oxt extension.

Extensions like the ones found here:

    Extensions could be found at:
"""

import functools
import os
import xml.dom.minidom
import zipfile

# public objects
__all__ = ['extract_oxt']

def find_dictionaries(registry):
    def oor_name(name, element):
        return element.attributes['oor:name'].value.lower() == name
    
    def get_property(name, properties):
        property = list(filter(functools.partial(oor_name, name),
                               properties))
        if property:
            return property[0].getElementsByTagName('value')[0]
    
    result = []
    
    for dictionaries in filter(functools.partial(oor_name, 'dictionaries'),
                               registry.getElementsByTagName('node')):
        for dictionary in dictionaries.getElementsByTagName('node'):
            properties = dictionary.getElementsByTagName('prop')
            format = get_property('format', properties).firstChild.data.strip()
            if format and format == 'DICT_SPELL':
                locations = get_property('locations', properties)
                if locations.firstChild.nodeType == xml.dom.Node.TEXT_NODE:
                    locations = locations.firstChild.data
                    locations = locations.replace('%origin%/', '').strip()
                    result.append(locations.split())
                else:
                    locations = [item.firshChild.data.replace('%origin%/', '') \
                                 .strip() for item in
                                 locations.getElementsByTagName('it')]
                    result.append(locations)
    
    return result

def extract(filename, target):
    """
    Extract Hunspell dictionaries out of LibreOffice ``.oxt`` extensions.

    :param filename: path to the ``.oxt`` extension
    :param target: path to extract Hunspell dictionaries to
    :rtype: list of the extracted dictionaries

    This function extracts the Hunspell dictionaries (``.dic`` and ``.aff``
    files) from the given ``.oxt`` extension found to ``target``.

    Extensions could be found at:

        http://extensions.services.openoffice.org/dictionary
    """
    with zipfile.ZipFile(filename, 'r') as extension:
        files = extension.namelist()
        
        registry = 'dictionaries.xcu'
        if not registry in files:
            for filename in files:
                if filename.lower().endswith(registry):
                    registry = filename
                
        if registry in files:
            registry = xml.dom.minidom.parse(extension.open(registry))
            dictionaries = find_dictionaries(registry)
            extracted = []
            for dictionary in dictionaries:
                for filename in dictionary:
                    with open(os.path.join(target, os.path.basename(filename)),
                              'wb') as _target:
                        with extension.open(filename, 'r') as _source:
                            extracted.append(os.path.basename(filename))
                            _target.write(_source.read())
            return extracted