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

ENCODING = 'UTF-8'

import sys
import argparse

# Python 2/3 unicode
import sys
if sys.version_info.major == 3:
    io_in = lambda x: x
    io_out = io_in
else:
    io_in = lambda x: x.decode(ENCODING)
    io_out = lambda x: x.encode(ENCODING)   

# Pipes Python enconding nightmare
if sys.stdout.encoding is None:
    import codecs
    sys.stdout = codecs.getwriter(ENCODING)(sys.stdout)

# Find metadata dict
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '../src/'))
from gtkspellcheck import __metadata__

# Parse command line
parser = argparse.ArgumentParser(description='Insert metadata into plain text files.')
parser.add_argument('infile', type=argparse.FileType('r'),
                     help='path to the template file or stdin pipe.')
parser.add_argument('-w', '--writeback', action='store_true',
                     help='write the output back to the input file.')
args = parser.parse_args()

# Read content
out_content = io_in(args.infile.read())
args.infile.close()

# Replace variables
# FIXME: Stop wasting memory like crazy!
for key, value in __metadata__.items():
    out_content = out_content.replace(key, value)

# Print/Write new content
if args.writeback:
    try:
        with open(args.infile.name, 'w') as out_handler:
            out_handler.write(io_out(out_content))
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(-1)
else:
    print(out_content)

sys.exit(0)
