#!/bin/bash

python3 setup.py register
python3 setup.py build_sphinx
python2 setup.py upload_sphinx --upload-dir=build/sphinx/html/ 
