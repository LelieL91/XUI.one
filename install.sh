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

# Requirements
install_deps(){
  
  
  
}

DEBIAN_FRONTEND=noninteractive apt-get update >/dev/null 2>&1
DEBIAN_FRONTEND=noninteractive apt install software-properties-common ca-certificates lsb-release apt-transport-https >/dev/null 2>&1
[ -f "/usr/bin/python3" ] || { DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-dev python-is-python3 unzip >/dev/null 2>&1; }
[ -f "/usr/bin/python" ] || { DEBIAN_FRONTEND=noninteractive apt-get -y install python-is-python3 >/dev/null 2>&1; }
cd /root
wget https://github.com/amidevous/xui.one/releases/download/test/XUI_1.5.12.zip -O XUI_1.5.12.zip >/dev/null 2>&1
unzip XUI_1.5.12.zip >/dev/null 2>&1
wget https://raw.githubusercontent.com/amidevous/xui.one/master/install.python3 -O /root/install.python3 >/dev/null 2>&1
python3 /root/install.python3