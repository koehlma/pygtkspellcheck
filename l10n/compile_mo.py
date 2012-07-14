#!/usr/bin/env python

import os
import sys
import shutil

where_am_i = os.path.normpath(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
os.chdir(where_am_i)

if sys.version_info.major == 3:
    import msgfmt3 as msgfmt
else:
    import msgfmt2 as msgfmt

def build_mo_files():
    """Compile available localization files"""
    
    APP = 'pygtkspellcheck'
    locale_dir = 'mo'
    po_dir = 'pygtkspellcheck'

    if os.path.exists(locale_dir):
        shutil.rmtree(locale_dir)
    os.mkdir(locale_dir)

    available_langs = [f[:-3] for f in os.listdir(po_dir) if f.endswith('.po')]

    print('Languages: {langs}'.format(langs=str(available_langs)))

    for lang in available_langs:
        po_file = os.path.join(po_dir, lang + '.po')
        lang_dir = os.path.join(locale_dir, lang)
        mo_dir = os.path.join(lang_dir, 'LC_MESSAGES')
        mo_file = os.path.join(mo_dir, APP + '.mo')
        
        if not os.path.exists(mo_dir):
            os.makedirs(mo_dir)
        
        print('Compiling {0} to {1}'.format(po_file, mo_file))
        msgfmt.make(po_file, mo_file)

if __name__ == '__main__':
    build_mo_files()

