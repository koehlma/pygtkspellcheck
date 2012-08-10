#!/bin/bash

set -o errexit
set -o nounset

# Base packages needed to run this script:
#    sudo apt-get install devscripts quilt build-essential fakeroot dh-make wget pbuilder

export DEBFULLNAME="Carlos Miguel Jenkins Pérez"
export DEBEMAIL="carlos@jenkins.co.cr"

# Create Python sdist
echo "Entering to the distribution root..."
cd ../../
python setup.py sdist
echo "Entering to dist..."
cd dist/

# Create build folder
echo "Creating build folder..."
mkdir -p debian/build

# Copy source package
echo "Copying source package..."
SDIST=`find . -maxdepth 1 -type f -name *.tar.gz`
DEBSDIST=`echo $SDIST | sed s/.tar.gz/.orig.tar.gz/ | sed s/-/_/`
cp $SDIST debian/build/$DEBSDIST

# Build Debian source package
echo "Entering build folder..."
cd debian/build/
tar -zxvf $DEBSDIST
DEBSDISTUN=`find . -maxdepth 1 -type d -name pygtkspellcheck-*`
cp -R ../debian/ $DEBSDISTUN/

# Build Debian binary packages
echo "Entering $DEBSDISTUN..."
cd $DEBSDISTUN/
echo "Ready to build package. Press [Enter] to confirm structure and build using debuild or Ctrl+C to cancel. Type 'pbuilder' to build using pbuilder."
read builder
if [ "$builder" == "pbuilder" ]; then
  echo "Building using pbuilder..."
  pdebuild -us -uc
else
  echo "Building using debuild..."
  debuild -us -uc

  # Move Debian packages
  echo "Moving Debian packages..."
  cd ../
  mv *.deb ../
fi

# Clean
echo "Done. Perform cleaning? Press [Enter] to confirm cleaning and continue or Ctrl+C to cancel."
read
cd ../../../
rm -R dist/debian/build
rm -f dist/pygtkspellcheck-*
rm -f MANIFEST
python setup.py clean
