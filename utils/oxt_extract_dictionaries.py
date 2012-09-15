#!/usr/bin/env python
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

import sys
import argparse

sys.modules['gtk'] = None
import gtkspellcheck.oxt_extract

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('extension', nargs='+',
                        help='extension to extract')
    parser.add_argument('target',
                        help='target directory')
    
    arguments = parser.parse_args()
    for extension in arguments.extension:
        try:
            gtkspellcheck.oxt_extract.extract(extension, arguments.target)
        except gtkspellcheck.oxt_extract.BadXml:
            print(gtkspellcheck.oxt_extract._('extension "{}" has no valid XML '
                                              'dictionary registry'
                                              ).format(extension))
        except gtkspellcheck.oxt_extract.BadExtensionFile:
            print(gtkspellcheck.oxt_extract._('extension "{}" is not a valid '
                                              'ZIP file'
                                              ).format(extension))