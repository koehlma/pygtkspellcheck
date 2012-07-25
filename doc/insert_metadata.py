#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2012, Maximilian Köhl <linuxmaxi@googlemail.com>
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

import sys
from os.path import exists, isfile

try:
    from gtkspellcheck import __metadata__
except ImportError: # Load if running from source
    import sys
    from os.path import join, dirname
    sys.path.append(join(dirname(__file__), '../src/'))
    from gtkspellcheck import __metadata__

# Python 2/3 compat
if sys.version_info.major == 3:
    u = lambda x: x
else:
    u = lambda x: x.decode('UTF-8')

usage = \
"""
USAGE:
    ./insert_metadata.py [INPUT_FILE] [OUTPUT_FILE]
"""

if len(sys.argv) != 3:
    print(usage)
    sys.exit(-1)

in_file = sys.argv[1]
out_file = sys.argv[2]

if not isfile(in_file):
    print('Unable find input file: {i}'.format(i=in_file))
    sys.exit(-2)

if exists(out_file):
    print('Output file {o} already exists. Stopping.'.format(i=out_file))
    sys.exit(-3)

with open(in_file, 'r') as in_handler:
    out_content = u(in_handler.read())

for key in __metadata__.keys():
    out_content = out_content.replace(key, __metadata__[key])

if out_file == '-':
    print(out_content)
else:
    with open(filename, 'w') as out_handler:
        out_handler.write(out_content)

sys.exit(0)
