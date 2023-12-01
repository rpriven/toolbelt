# Djedi Toolbelt

This is intended for new Kali installs to install a large amount of useful tools not included with Kali in a short amount of time.

It is recommended if this is a new Kali VM to run PimpMyKali and run the 'N' option first.  Dewalt has done an excellent job on this and keeps getting better every time I use it.  You can check it out here:  https://github.com/Dewalt-arch/pimpmykali

## Updates

Python version got some important tweaks to speed things up and smooth out some issues.  It now takes only about 1 minute compared to 10 minutes or so using the bash version.  Still may have some tweaks to work through but it seems to be working well in the several tests I've done.  I will be putting this into a script shortly but here is instructions.

### toolbelt.py Installation

First we must install apt-fast
```bash
sudo apt install aria2 -y
/bin/bash -c "$(curl -sL https://git.io/vokNn)"
cp apt-fast /usr/local/sbin/
chmod +x /usr/local/sbin/apt-fast
cp apt-fast.conf /etc
```

Then we should be good to go:
```bash
curl https://raw.githubusercontent.com/rpriven/toolbelt/main/toolbelt.py | sudo python3
```

Still getting an error about 'jammy' not being signed and 'docker' package has no candidate.  Working on fixes.

*However, please note that there is an issue with the go tools and the useful scripts being downloaded in the /root directory instead of /home/kali because the script must be run as root.  Working on a fix for this*

## Overview

This script installs / updates some of the important key tools for Pentesters and Bug Bounty Hunters.  You probably
have most of these tools installed already (as it was designed for use with Kali/Debian/Ubuntu), but it is useful for 
me to have it all together in one script so I don't have to take the time to search for everything when I make a 
new VM or have to go through and install or update everything manually.

This is a rough version as it is my first attempt at building some sort of a recon framework (if you can call
it that) for Pentesting, CTFs as well as Bug Bounties.  There will be an accompanying automation script as well.

**This installs a good amount of tools, if you are looking for something light, you may want to remove what you do not want or need before running the script.**
*It is also a good idea to read through unfamiliar code before executing it anyway.*

## (Old) Installation

Simply download the script and run it:

```bash
wget https://raw.githubusercontent.com/rpriven/toolbelt/main/toolbelt.sh
chmod +x toolbelt.sh
sudo ./toolbelt.sh
```

Easier:

```bash
curl https://raw.githubusercontent.com/rpriven/toolbelt/main/toolbelt.sh | sudo sh
```

## What is on the Toolbelt:

- Nmap
- naabu
- Nuclei
- Burp Suite
- feroxbuster
- nikto
- masscan
- Gobuster
- SecLists
- SQLmap
- git
- docker
- docker.io
- pimpmykali
- Golang
- Impacket
- knockpy
- Sublist3r
- Striker
- waymore
- wfuzz
- scrapy
- amass
- assetfinder
- httprobe
- gowitness
- subjack
- hakrawler
- webanalyze
- RustScan

## To Do List

### Add basic syntax to tools

### Add checks for the Go programs if they are the @latest version so it doesn't re-download them every time
the script is run, only when it is either not found or not up to date

### Add to the toolbelt:

- dnmasscan
- interlace
- static-flow
- sn1per
- more...

### Add colors
