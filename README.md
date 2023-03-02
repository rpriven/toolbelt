# Djedi Toolbelt

## Update: Check out the new python version

This is still being updated but I think it is much more efficient and has so much more than the previous versions.

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

## Installation

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
