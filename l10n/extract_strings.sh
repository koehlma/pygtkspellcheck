#!/bin/bash
xgettext --keyword=translatable --sort-output -o pygtkspellcheck/en.po \
../src/gtkspellcheck/spellcheck.py ../src/gtkspellcheck/oxt_import.py
echo "Done!"
