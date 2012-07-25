# -*- coding:utf-8 -*-
#
# Copyright (C) 2012, Carlos Jenkins <carlos@jenkins.co.cr>
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
Uncompress, read and install LibreOffice .oxt dictionaries extensions.

This module extracts the .dic and .aff (Hunspell) dictionaries from all the 
.oxt extensions found on some directory.

Extensions like the ones found here:

    http://extensions.services.openoffice.org/dictionary
"""

import os
import xml.dom.minidom
import shutil
import logging
import gettext
from zipfile import ZipFile, BadZipfile

# Expose
__all__ = ['deflate_oxt']

logger = logging.getLogger(__name__)
_ = gettext.translation('pygtkspellcheck', fallback=True).gettext

def deflate_oxt(oxt_path, extract_path, override=False, move_path=None):
    """
    Uncompress, read and install LibreOffice ``.oxt`` dictionaries extensions.

    :param oxt_path: path to a directory containing the ``.oxt`` extensions.
    :param extract_path: path to extract Hunspell dictionaries files.
    :param override: override files.
    :param move_path: Optional path to move the ``.oxt`` files after processing.
    :rtype: None

    This function extracts the Hunspell dictionaries (``.dic`` and ``.aff``
    files) from all the ``.oxt`` extensions found on ``oxt_path`` directory to
    the ``extract_path`` directory.

    Extensions like the ones found here:

        http://extensions.services.openoffice.org/dictionary

    In detail, this functions does the following:

        1. Find all the ``.oxt`` extension files within ``oxt_path``
        2. Open (unzip) each extension.
        3. Find the dictionary definition file within (*dictionaries.xcu*)
        4. Parse the dictionary definition file and locate the dictionaries files.
        5. Uncompress those files to ``extract_path``.

    By default file overriding is disabled, set ``override`` parameter to True
    if you want to enable it. As and additional option, each processed extension
    can be moved to ``move_path``.
    """

    # Get the real, absolute and normalized path
    oxt_path = os.path.normpath(os.path.abspath(os.path.realpath(oxt_path)))
    
    # Check that the input directory exists
    if not os.path.isdir(oxt_path):
        return
        
    # Create extract directory if not exists
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    # Check that the extract path is a directory
    if not os.path.isdir(extract_path):
        logger.error(_('Extract path is not a directory.'))
        return
    
    # Get all .oxt extension at given path
    oxt_files = [extension for extension in os.listdir(oxt_path) if extension.lower().endswith('.oxt')]
    
    for extension_name in oxt_files:
        
        extension_path = os.path.join(oxt_path, extension_name)
        
        try:
            with ZipFile(extension_path, 'r') as extension_file:
                
                # List of files within the extension file
                files_within = extension_file.namelist()
                
                # Find the dictionaries registry
                registry = 'dictionaries.xcu'
                if not registry in files_within:
                    for file_path in files_within:
                        if file_path.lower().endswith(registry):
                            registry = file_path
                
                if registry in files_within:
                    try:
                        # Find within the registry the entry for dictionaries
                        registry_content = extension_file.read(registry)
                        dom = xml.dom.minidom.parseString(registry_content)
                        dic_locations = _find_dictionaries_location(dom)
                        
                        if dic_locations:
                            for dic_location in dic_locations:
                                
                                # Get the list of files considered dictionaries for current entry
                                dic_location = dic_location.replace('%origin%', os.path.dirname(registry))
                                dic_files = []
                                for dic_file in dic_location.split(' '):
                                    if dic_file.startswith('/'):
                                        dic_file = dic_file[1:]
                                    dic_files.append(os.path.normpath(dic_file))
                                
                                # Extract files if they exists within the extension file
                                for dic_file in dic_files:
                                    if dic_file in files_within:
                                        target = os.path.join(extract_path, os.path.basename(dic_file))
                                        # Extract only if we are overriding or file doesn't exists
                                        if (override and os.path.isfile(target)) or (not os.path.exists(target)):
                                            # Extract a single file without caring about folder structure
                                            with extension_file.open(dic_file) as source:
                                                with file(target, 'wb') as destination:
                                                    shutil.copyfileobj(source, destination)
                                    else:
                                        logger.warning(_('\'{0}\' declared in registry but not found within the extension.').format(dic_file))
                                
                    except Exception as inst:
                        logger.exception(_('Error while processing extension {0}.').format(extension_name))
                        pass
                else:
                    logger.error(_('Extension \'{0}\' has no dictionary registry.').format(extension_name))
        except BadZipfile:
            logger.error(_('Extension \'{0}\' is not a valid zip file.').format(extension_name))
        
        
        # Move the extension after processing if user requires it
        if move_path is not None:
            # Create move path if it doesn't exists
            if not os.path.exists(move_path):
                os.makedirs(move_path)
            # Move to the given path only if it is a directory and target doesn't exists
            if os.path.isdir(move_path):
                if not os.path.exists(os.path.join(move_path, extension_name)) or override:
                    #print('Move from ', extension_path, ' to ', move_path)
                    shutil.move(extension_path, move_path)
                else:
                    logger.warning(_('Unable to move extension, file with same name exists within move_path.'))
            else:
                logger.warning(_('Unable to move extension, move_path is not a directory.'))


def _find_dictionaries_location(dom):
    """Find the location of the dictionaries files in the extension XML registry"""

    def _is_text_node(element):
        return element.firstChild.nodeType == xml.dom.Node.TEXT_NODE
    
    result = []
    
    root = dom.getElementsByTagName('oor:component-data')[0]
    
    for value in root.getElementsByTagName('value'):
        if _is_text_node(value) and value.firstChild.data == 'DICT_SPELL':
            dict_node = value.parentNode.parentNode
            for prop in dict_node.getElementsByTagName('prop'):
                if prop.hasAttribute('oor:name') and prop.getAttribute('oor:name') == 'Locations':
                    dict_value = prop.getElementsByTagName('value')[0]
                    # <value>%origin%/es_CR.aff %origin%/es_CR.dic</value>
                    if _is_text_node(dict_value):
                        result.append(dict_value.firstChild.data)
                    # <value><it>%origin%/es_CR.aff</it><it>%origin%/es_CR.dic</it></value>
                    else:
                        for item in dict_value.getElementsByTagName('it'):
                            result.append(item.firstChild.data)
                break
    return result

