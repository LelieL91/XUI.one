#!/bin/bash
echo -e "\nChecking that minimal requirements are ok"

read -p -1 "Do you want patch your build? [Y/n]" USER_REPLY

# Define directories
THIS_PATH=`dirname "$(readlink -f "$0")"`
BUILD_DIR="$thisPath/phpbuild"

# Ensure the OS is compatible with the launcher
if [ -f /etc/os-release ]; then
    OS=$(grep -w ID /etc/os-release | sed 's/^.*=//')
    VER=$(grep -w VERSION_ID /etc/os-release | sed 's/^.*=//' | tr -d '"')
    ARCH=$(uname -m)
else
    echo "Sorry, this OS is not supported by this XtreamUI.one installer."
    exit 1
fi

echo "Detected : $OS  $VER  $ARCH"
[[ "$OS" = "debian" && ( "$VER" = "11" || "$VER" = "12" ) && "$ARCH" == "x86_64" ]] || { echo "Sorry, this OS is not supported by this XtreamUI.one installer."; exit 1; }

read -p -1 "Enter PHP version to compile [7.4.33]: " PHP_VER

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
wget --no-check-certificate https://www.php.net/distributions/php-$PHP_VER.tar.gz -O "$BUILD_DIR/php-$PHP_VER.tar.gz"
rm -rf "$BUILD_DIR/php-$PHP_VER"
tar -xvf "$BUILD_DIR/php-$PHP_VER.tar.gz"

read -p -1 "Do you want patch your build? [Y/n]" USER_REPLY
if [[ "$VER" = "18.04" || "$VER" = "20.04" || "$VER" = "22.04" || "$VER" = "24.04" || "$VER" = "11" || "$VER" = "12" || "$VER" = "37" || "$VER" = "38" ]]; then
wget --no-check-certificate "https://launchpad.net/~ondrej/+archive/ubuntu/php/+sourcefiles/php7.3/7.3.33-2+ubuntu22.04.1+deb.sury.org+1/php7.3_7.3.33-2+ubuntu22.04.1+deb.sury.org+1.debian.tar.xz" -O "$BUILD_DIR/debian.tar.xz"
tar -xf "$BUILD_DIR/debian.tar.xz"
rm -f "$BUILD_DIR/debian.tar.xz"
cd "$BUILD_DIR/php-$PHP_VER"
patch -p1 < ../debian/patches/0060-Add-minimal-OpenSSL-3.0-patch.patch
else
cd "$BUILD_DIR/php-$PHP_VER"
fi
'./configure' '--prefix=/home/xui/bin/php' '--with-fpm-user=xui' '--with-fpm-group=xui' '--enable-gd' '--with-jpeg' '--with-freetype' '--enable-static' '--disable-shared' '--enable-opcache' '--enable-fpm' '--without-sqlite3' '--without-pdo-sqlite' '--enable-mysqlnd' '--with-mysqli' '--with-curl' '--disable-cgi' '--with-zlib' '--enable-sockets' '--with-openssl' '--enable-shmop' '--enable-sysvsem' '--enable-sysvshm' '--enable-sysvmsg' '--enable-calendar' '--disable-rpath' '--enable-inline-optimization' '--enable-pcntl' '--enable-mbregex' '--enable-exif' '--enable-bcmath' '--with-mhash' '--with-gettext' '--with-xmlrpc' '--with-xsl' '--with-libxml' '--with-pdo-mysql' '--disable-mbregex'
#'./configure'  '--prefix=/home/xui/bin/php' '--with-zlib-dir' '--with-freetype-dir' '--enable-mbstring' '--enable-calendar' '--with-curl' '--with-gd' '--disable-rpath' '--enable-inline-optimization' '--with-bz2' '--with-zlib' '--enable-sockets' '--enable-sysvsem' '--enable-sysvshm' '--enable-pcntl' '--enable-mbregex' '--enable-exif' '--enable-bcmath' '--with-mhash' '--enable-zip' '--with-pcre-regex' '--with-pdo-mysql=mysqlnd' '--with-mysqli=mysqlnd' '--with-openssl' '--with-fpm-user=xtreamcodes' '--with-fpm-group=xtreamcodes' '--with-libdir=/lib/x86_64-linux-gnu' '--with-gettext' '--with-xmlrpc' '--with-xsl' '--enable-opcache' '--enable-fpm' '--enable-libxml' '--enable-static' '--disable-shared' '--with-jpeg-dir' '--enable-gd-jis-conv' '--with-webp-dir' '--with-xpm-dir'
make -j$(nproc --all)
killall php
killall php-fpm
killall php
killall php-fpm
killall php
killall php-fpm
make install
cd /root
rm -rf "$BUILD_DIR"
chattr +i /home/xui/bin/php/sbin/php-fpm
chattr +i /home/xui/bin/php/bin/php
