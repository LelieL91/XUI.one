#!/bin/bash

# Ensure the script is running as root
[ "$EUID" -eq 0 ] || { echo -e "\nPlease run as root. Exiting..."; exit 1; }

echo -e "\nChecking that minimal requirements are ok"

# Ensure the OS is compatible with the launcher (Debian Only)
if [ -f /etc/os-release ]; then
  OS=$(grep -w ID /etc/os-release | sed 's/^.*=//')
  VER=$(grep -w VERSION_ID /etc/os-release | sed 's/^.*=//' | tr -d '"')
  ARCH=$(uname -m)
else
  echo 'Sorry, this OS is not supported by this XtreamUI.one installer.'
  exit 1
fi

echo "Detected : $OS  $VER  $ARCH"
[[ ( "$OS" = 'debian' || "$OS" = 'ubuntu' ) && ( "$VER" = '11' || "$VER" = '12' || "$VER" = '24.04' ) && "$ARCH" == 'x86_64' ]] || { echo 'Sorry, this OS is not supported by this XtreamUI.one installer.'; exit 1; }

# Define Build functions
DEBIAN_DEPS(){
  # Download and extract 
  mkdir -p '/root/XUI-Deps'
  wget --no-check-certificate --content-disposition 'https://github.com/LelieL91/XUI.one/releases/latest/download/xui_deb_fix.tar.gz' -O '/root/XUI-Deps/xui.tar.gz' -q --show-progress
  tar -xf '/root/XUI-Deps/xui_nginx_update.tar.gz' -C '/root/XUI-Deps'
  # Install Debian packages
  dpkg -i '/root/XUI-Deps/libjpeg8_8d-1+deb7u1_amd64.deb' >/dev/null 2>&1
  dpkg -i '/root/XUI-Deps/multiarch-support_2.28-10+deb10u4_amd64.deb' >/dev/null 2>&1
  dpkg -i '/root/XUI-Deps/libssl1.1_1.1.1w-0+deb11u1_amd64.deb' >/dev/null 2>&1
  rm -rf '/root/XUI-Deps'
}

INSTALL_XUI(){
  echo -e "Installing Installer OS dependancies"
  apt update >/dev/null 2>&1 && apt -y install software-properties-common ca-certificates apt-transport-https >/dev/null 2>&1
  [ -f '/usr/bin/python3' ] || { echo -e 'Missing Python3! Installing...'; apt -y install python3 python3-dev >/dev/null 2>&1; }
  [ -f '/usr/bin/python' ] || { echo -e 'Missing Python3 requirement! Installing...'; apt -y install python-is-python3 >/dev/null 2>&1; }
  [ -f '/usr/bin/sudo' ] || { echo -e 'Missing sudo! Installing...'; apt -y install sudo >/dev/null 2>&1; }
  [[ "$OS" == 'debian' && "$VER" == '12' ]] && { echo -e 'Debian 12 detected! Installing libraries...'; DEBIAN_DEPS; }
  echo -e 'Downloading Latest XUI.one release'
  mkdir -p '/root/XUI-Installer'
  wget --no-check-certificate --content-disposition 'https://github.com/LelieL91/XUI.one/releases/latest/download/xui.tar.gz' -O '/root/XUI-Installer/xui.tar.gz' -q --show-progress
  wget --no-check-certificate --content-disposition 'https://raw.githubusercontent.com/LelieL91/XUI.one/master/xui-remote-sql.py' -O '/root/XUI-Installer/xui-remote-sql.py' -q --show-progress
  echo -e 'Running XUI.one Installer'
  python3 '/root/XUI-Installer/xui-remote-sql.py'
  rm -rf '/root/XUI-Installer'
}

UPDATE_XUI(){
  echo -e 'Update XUI Function Triggered!! EMPTY'
}

UPDATE_NGINX(){
  echo -e 'Starting Nginx Updating process!!'
  # Stop XUI.one and backup old binaries (only 1st time)
  systemctl stop xuione && sleep 5
  cp -n '/home/xui/bin/nginx/sbin/nginx' '/home/xui/bin/nginx/sbin/nginx_old'
  cp -n '/home/xui/bin/nginx_rtmp/sbin/nginx_rtmp' '/home/xui/bin/nginx_rtmp/sbin/nginx_rtmp_old'
  # Download and extract 
  mkdir -p '/root/XUI-Updater'
  wget --no-check-certificate --content-disposition 'https://github.com/LelieL91/XUI.one/releases/latest/download/xui_nginx_update.tar.gz' -O '/root/XUI-Updater/xui_nginx_update.tar.gz' -q --show-progress
  tar -xf '/root/XUI-Updater/xui_nginx_update.tar.gz' -C '/root/XUI-Updater'
  # Copy binaries into XUI.one directories and remove updater folder
  cp '/root/XUI-Updater/nginx' '/home/xui/bin/nginx/sbin'
  cp '/root/XUI-Updater/nginx_rtmp' '/home/xui/bin/nginx_rtmp/sbin'
  rm -rf '/root/XUI-Updater'
  # Fix binaries owner and permissions
  chown xui:xui '/home/xui/bin/nginx/sbin/nginx' '/home/xui/bin/nginx_rtmp/sbin/nginx_rtmp'
  chmod 550 '/home/xui/bin/nginx/sbin/nginx' '/home/xui/bin/nginx_rtmp/sbin/nginx_rtmp'
  # Remove old pid files and start XUI.one
  [[ -f '/home/xui/bin/nginx/logs/nginx.pid' ]] && rm '/home/xui/bin/nginx/logs/nginx.pid'
  [[ -f '/home/xui/bin/nginx_rtmp/logs/nginx.pid' ]] && rm '/home/xui/bin/nginx_rtmp/logs/nginx.pid'
  systemctl start xuione && sleep 5
  echo -e 'Nginx has been successfully updated!!'
}

# Requirements
INSTALL_MENU(){
echo -ne "
Welcome to XUI.one Installer by LelieL91
1) Install latest XUI.one version (Fresh Install)
2) Update to latest XUI.one version
3) Update 'Nginx component' to latest version
0) Exit
Choose an option: "
  read a
  case $a in
    1) INSTALL_XUI ; INSTALL_MENU ;;
    2) UPDATE_XUI ; INSTALL_MENU ;;
    3) UPDATE_NGINX ; INSTALL_MENU ;;
    0) exit 0 ;;
    *) echo -e "Wrong option." ; INSTALL_MENU ;;
  esac
}

INSTALL_MENU