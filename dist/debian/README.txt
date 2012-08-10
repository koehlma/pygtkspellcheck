1. Install Debian required build packages:

    sudo apt-get install devscripts build-essential fakeroot dh-make wget pbuilder debootstrap debian-archive-keyring

2. Create a chroot environment:

    sudo pbuilder create --distribution unstable --mirror ftp://ftp.us.debian.org/debian/ --debootstrapopts "--keyring=/usr/share/keyrings/debian-archive-keyring.gpg"

3. Run make_release script:

    cd dist/debian
    ./make_release.sh

    Type 'pbuilder' when asked to use pbuilder for building.

