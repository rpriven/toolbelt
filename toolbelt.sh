#!/bin/bash

# Djedi Toolbox // Djedi Toolbelt
# Installs most useful tools

## To Do List
# implement requirements.txt
# xargs apt install < requirements.txt

# Need to add programs:
# dnmasscan
# interlace
# Static-Flow
# Sn1per
# TomNomNom tools..

figlet DjediToolbelt | lolcat && echo "v.0.1"
echo "[*] Installing Pentest & Bug Bounty Toolbox Suite..."

# if not sudo, exit
if ! [ $(id -u) = 0 ]; then
    echo "Please run as root"
    exit 1
fi

echo "[+] Installing / Updating nmap naabu nuclei burpsuite feroxbuster nikto masscan gobuster seclists sqlmap git docker docker.io..."
sudo apt install nmap naabu nuclei burpsuite feroxbuster nikto masscan gobuster seclists sqlmap git docker docker.io -y

cd /opt
if [ ! -d pimpmykali ]; then
    echo "[+] Installing pimpmykali..."
    sudo git clone https://github.com/Dewalt-arch/pimpmykali
    cd pimpmykali
    echo "[+] Installing Golang..."
    sudo ./pimpmykali.sh --go
    echo "[+] Installing Impacket..."
    sudo ./pimpmykali.sh --impacket
    cd /opt
fi
if [ ! -d /opt/knock ]; then
    echo "[+] Installing Knockpy..."
    sudo git clone https://github.com/guelfoweb/knock.git
    cd knock
    pip3 install -r requirements.txt && cd /opt
fi
if [ ! -d /opt/Sublist3r ]; then
    echo "[+] Installing Sublist3r..."
    sudo git clone https://github.com/aboul3la/Sublist3r.git
    cd Sublist3r
    pip install -r requirements.txt && cd /opt
fi
if [ ! -d /opt/Striker ]; then
    echo "[+] Installing Striker..."
    sudo git clone https://github.com/s0md3v/Striker.git
    cd Striker
    pip install -r requirements.txt && cd /opt
fi
if [ ! -d /opt/waymore ]; then
    echo "[+] Installing waymore..."
    git clone https://github.com/xnl-h4ck3r/waymore.git
    cd waymore
    sudo pip3 install -r requirements.txt
    sudo python setup.py install && cd /opt
fi

echo "[+] Installing wfuzz and scrapy..."
pip install wfuzz scrapy

# Go Tools
echo "[+] Installing nuclei..."
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
echo "[+] Installing amass..."
go install -v github.com/OWASP/Amass/v3/...@master
echo "[+] Installing assetfinder..."
go install github.com/tomnomnom/assetfinder@latest
echo "[+] Installing httprobe..."
go install github.com/tomnomnom/httprobe@latest
echo "[+] Installing gowitness..."
go install github.com/sensepost/gowitness@latest
# echo "[+] Installing waybackurl..."
# go install github.com/tomnomnom/waybackurls@latest
echo "[+] Installing subjack..."
go install github.com/haccer/subjack@latest
echo "[+] Installing hakrawler..."
go install github.com/hakluke/hakrawler@latest
echo "[+] Installing webanalyze..."
go install -v github.com/rverton/webanalyze/cmd/webanalyze@latest && webanalyze -update

# Docker Stuff
echo "[+] Installing RustScan..."
docker pull rustscan/rustscan:2.0.1
if [ "~/.zshrc" ]; then
    echo "[+] adding rustscan alias to .zshrc"
    echo "alias rustscan='docker run -it --rm --name rustscan rustscan/rustscan:2.0.1'" >> .zshrc
elif [ "~/.bashrc" ]; then
    echo "[+] adding rustscan alias to .bashrc"
    echo "alias rustscan='docker run -it --rm --name rustscan rustscan/rustscan:2.0.1'" >> .bashrc
fi

echo "[*] Installation Complete"
