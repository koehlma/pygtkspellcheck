#!/bin/bash

set -o errexit
set -o nounset

export DEBFULLNAME="Maximilian Köhl"
export DEBEMAIL="linuxmaxi@googlemail.com"

cd ../../

echo "create python source distribution"
python setup.py sdist
cd dist/

echo "create build folder"
mkdir -p ubuntu/build

echo "copying source distribution"
SDIST=`find . -maxdepth 1 -type f -name *.tar.gz`
DEBSDIST=`echo $SDIST | sed s/.tar.gz/.orig.tar.gz/ | sed s/-/_/`
cp $SDIST ubuntu/build/$DEBSDIST

echo "extracting source distribution"
cd ubuntu/build/
tar -zxvf $DEBSDIST
DEBSDISTUN=`find . -maxdepth 1 -type d -name pygtkspellcheck-*`
cp -R ../debian/ $DEBSDISTUN/

cd $DEBSDISTUN/

echo "build and sign source package"
debuild -S -sa

echo "uploading source to launchpad"
cd ../
dput ppa:koehlma/packages pygtkspellcheck_*_source.changes
