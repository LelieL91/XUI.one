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
  echo "Sorry, this OS is not supported by this XtreamUI.one installer."
  exit 1
fi

echo "Detected : $OS  $VER  $ARCH"
[[ "$OS" = "debian" && ( "$VER" = "11" || "$VER" = "12" ) && "$ARCH" == "x86_64" ]] || { echo "Sorry, this OS is not supported by this XtreamUI.one installer."; exit 1; }

# Define Build functions
INSTALL_XUI(){
  echo -e "Installing Installer OS dependancies"
  apt -y update >/dev/null 2>&1 && apt -y install software-properties-common ca-certificates lsb-release apt-transport-https >/dev/null 2>&1
  [ -f "/usr/bin/python3" ] || { echo -e "Missing Python3! Installing..."; apt -y install python3 python3-dev unzip >/dev/null 2>&1; }
  [ -f "/usr/bin/python" ] || { echo -e "Missing Python3 requirement! Installing..."; apt -y install python-is-python3 >/dev/null 2>&1; }
  [ -f "/usr/bin/sudo" ] || { echo -e "Missing sudo! Installing..."; apt -y install sudo >/dev/null 2>&1; }
  echo -e "Downloading Latest XUI.one release"
  wget --no-check-certificate --content-disposition 'https://github.com/LelieL91/XUI.one/releases/download/1.5.13/xui.tar.gz' -O '/root/xui.tar.gz' -q --show-progress
  wget --no-check-certificate --content-disposition 'https://raw.githubusercontent.com/LelieL91/XUI.one/master/install-xui.py' -O '/root/install-xui.py' -q --show-progress
  echo -e "Running XUI.one Installer"
  python3 '/root/install-xui.py'
}

UPDATE_XUI(){
  echo "Update XUI Function Triggered!! EMPTY"
}

UPDATE_NGINX(){
  echo "Starting Nginx Updating process!!"
  # Stop XUI.one and backup old binaries (only 1st time)
  systemctl stop xuione && sleep 5
  cp -n '/home/xui/bin/nginx/sbin/nginx' '/home/xui/bin/nginx/sbin/nginx_old'
  cp -n '/home/xui/bin/nginx_rtmp/sbin/nginx_rtmp' '/home/xui/bin/nginx_rtmp/sbin/nginx_rtmp_old'
  # Download and extract 
  mkdir -p "/root/XUI-updater"
  wget --no-check-certificate --content-disposition 'https://github.com/LelieL91/XUI.one/releases/download/1.5.13/xui_nginx_update.tar.gz' -O '/root/XUI-updater/xui_nginx_update.tar.gz' -q --show-progress
  tar -xf '/root/XUI-updater/xui_nginx_update.tar.gz' -C '/root/XUI-updater'
  # Copy binaries into XUI.one directories and remove updater folder
  cp '/root/XUI-updater/nginx' '/home/xui/bin/nginx/sbin'
  cp '/root/XUI-updater/nginx_rtmp' '/home/xui/bin/nginx_rtmp/sbin'
  rm -rf '/root/XUI-updater'
  # Fix binaries owner and permissions
  chown xui:xui '/home/xui/bin/nginx/sbin/nginx' '/home/xui/bin/nginx_rtmp/sbin/nginx_rtmp'
  chmod 550 '/home/xui/bin/nginx/sbin/nginx' '/home/xui/bin/nginx_rtmp/sbin/nginx_rtmp'
  # Remove old pid files and start XUI.one
  [[ -f '/home/xui/bin/nginx/logs/nginx.pid' ]] && rm '/home/xui/bin/nginx/logs/nginx.pid'
  [[ -f '/home/xui/bin/nginx_rtmp/logs/nginx.pid' ]] && rm '/home/xui/bin/nginx_rtmp/logs/nginx.pid'
  systemctl start xuione && sleep 5
  echo 'Nginx has been successfully updated!!'
}

UPDATE_PHP(){
  echo "Update PHP Function Triggered!! EMPTY"
#  Check if folder exist /home/xui/bin/php
#  Make backup: cp -R '/home/xui/bin/php' '/home/xui/bin/php.bak'
#  tar -xf "/root/xuione_php_latest.tar.gz" -C "/home/xui/bin"
# sudo cp -r xui.so /home/xui/bin/php/lib/php/extensions/no-debug-non-zts-20190902/xui.so >/dev/null 2>&1
}

# Requirements
INSTALL_MENU(){
echo -ne "
Welcome to XUI.one Debian Installer by LelieL91
1) Install latest XUI.one version (Fresh Install)
2) Update to latest XUI.one version
3) Update 'Nginx component' to latest version
4) Update 'PHP component' to latest version
0) Exit
Choose an option: "
  read a
  case $a in
    1) INSTALL_XUI ; INSTALL_MENU ;;
    2) UPDATE_XUI ; INSTALL_MENU ;;
    3) UPDATE_NGINX ; INSTALL_MENU ;;
    4) UPDATE_PHP ; INSTALL_MENU ;;
    0) exit 0 ;;
    *) echo -e "Wrong option." ; INSTALL_MENU ;;
  esac
}

INSTALL_MENU