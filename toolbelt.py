#!/usr/bin/python3

######################
''' Djedi Toolbelt '''
''' Python3 Reboot '''
######################

'''
#########################################################################

WARNING: 

    This script is approximately 5 GB and will take a while to run.

    Please make sure you check this before installing.

    Menu will be coming in one of the next updates to help
    cater to your preferences and custom requirements.

#########################################################################         
'''

'''
TO DO:

    Finish - apt threading (sort of, with apt-fast)

    Add - Menu selection for the various categories:
            - apt tools only
            - opt tools only
            - python tools only
            - go tools only
            - docker tools only
            - scripts only

    Threading for /opt tools

    Find out where scripts are actually downloading

    Add C2 - Probably Havoc
    Add PowerView (if not already included)

    Double-check all tools

    Add section for Bug Bounty tools

    Add section for API tools

    Add option to download the recon.py automation script,
    which uses this toolbelt
    
'''

import subprocess, os, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from termcolor import colored
from tqdm import tqdm

threads = []

# Check if the user is running as root
if os.geteuid() != 0:
    print(colored("Please run as root", 'red'))
    exit(1)

'''
subprocess.run(["pip", "install", "progress"])

tools = ["tool1", "tool2", "tool3"]
bar = Bar('Installing', max=len(tools))
for tool in tools:
    # Code to install the tool
    bar.next()
bar.finish()
'''

# Figlet
os.system("figlet DjediToolbelt | lolcat")

# Version
print("v.0.3\n")

# Message
print(colored("[*] Installing Pentest & Bug Bounty Toolbox Suite", 'magenta'))

#########################
''' Aptitude Programs '''
#########################

def apt_tools():
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "apt-fast"])

    programs = ["nmap", "naabu", "nuclei", "burpsuite", "feroxbuster", "nikto", "masscan", "gobuster", "seclists", "sqlmap", "git"]

    for program in programs:
        if os.system(f"command -v {program}") == 0:
            print(colored(f"[*] {program} is already installed", 'blue'))
        else:
            print(colored(f"[+] Installing / updating {program}", 'green'))
            os.system(f"sudo apt-fast install {program} -y")
            if os.system(f"command -v {program}") != 0:
                print(colored(f"[*] Error: Failed to install the program: {program}", 'red'))
                exit(1)
        os.system(f"sudo apt-fast install docker docker.io golang-go -y")

##################
''' /opt Tools '''
##################

def opt_tools():  
    # Pimpmykali
    os.chdir("/opt")
    if not os.path.isdir("/opt/pimpmykali"):
        print(colored("[+] Installing pimpmykali...", 'green'))
        os.system("sudo git clone https://github.com/Dewalt-arch/pimpmykali")
        os.chdir("pimpmykali")
        print(colored("[+] Installing Golang...", 'green'))
        os.system("sudo ./pimpmykali.sh --go")
        print(colored("[+] Installing Impacket...", 'green'))
        os.system("sudo ./pimpmykali.sh --impacket")
        os.system("sudo ./pimpmykali.sh --upgrade")
        os.chdir("/opt")
    else:
        print(colored("[*] pimpmykali is already installed", 'blue'))

    # xnLinkFinder
    if not os.path.isdir("/opt/xnLinkFinder"):
        print(colored("[+] Installing xnLinkFinder...", 'green'))
        os.system("git clone https://github.com/xnl-h4ck3r/xnLinkFinder.git")
        os.chdir("xnLinkFinder")
        os.system("sudo python setup.py install")
        os.chdir("/opt")
    else:
        print(colored("[*] xnLinkFinder is already installed", 'blue'))

    # Knockpy
    if not os.path.isdir("/opt/knock"):
        print(colored("[+] Installing Knockpy...", 'green'))
        os.system("sudo git clone https://github.com/guelfoweb/knock.git")
        os.chdir("knock")
        os.system("pip3 install -r requirements.txt")
        os.chdir("/opt")
    else:
        print(colored("[*] Knockpy is already installed", 'blue'))

    # Sublist3r
    if not os.path.isdir("/opt/Sublist3r"):
        print(colored("[+] Installing Sublist3r...", 'green'))
        os.system("sudo git clone https://github.com/aboul3la/Sublist3r.git")
        os.chdir("Sublist3r")
        os.system("pip install -r requirements.txt")
        os.chdir("/opt")
    else:
        print(colored("[*] Sublist3r is already installed", 'blue'))

    # Striker
    if not os.path.isdir("/opt/Striker"):
        print(colored("[+] Installing Striker...", 'green'))
        os.system("sudo git clone https://github.com/s0md3v/Striker.git")
        os.chdir("Striker")
        os.system("pip install -r requirements.txt")
        os.chdir("/opt")
    else:
        print(colored("[*] Striker is already installed", 'blue'))

    # wafw00f
    if not os.path.isdir("/opt/wafw00f"):
        print(colored("[+] Installing wafw00f...", 'green'))
        os.system("git clone https://github.com/EnableSecurity/wafw00f.git")
        os.chdir("wafw00f")
        os.system("pip3 install -r requirements.txt")
        os.system("sudo python setup.py install")
        os.chdir("/opt")
    else:
        print(colored("[*] wafw00f is already installed", 'blue'))

    # Waymore
    if not os.path.isdir("/opt/waymore"):
        print(colored("[+] Installing waymore...", 'green'))
        os.system("git clone https://github.com/xnl-h4ck3r/waymore.git")
        os.chdir("waymore")
        os.system("pip3 install -r requirements.txt")
        os.system("sudo python setup.py install")
        os.chdir("/opt")
    else:
        print(colored("[*] waymore is already installed", 'blue'))

    # XSStrike
    if not os.path.isdir("/opt/XSStrike"):
        print(colored("[+] Installing XSStrike...", 'green'))
        os.system("git clone https://github.com/s0md3v/XSStrike.git")
        os.chdir("XSStrike")
        os.system("pip3 install -r requirements.txt")
        os.system("sudo python setup.py install")
        os.chdir("/opt")
    else:
        print(colored("[*] XSStrike is already installed", 'blue'))

####################
''' Python Tools '''
####################

def python_tools():
    print(colored("[+] Installing / Updating Python Tools...", 'green'))
    subprocess.run(["pip3", "install", "--upgrade", "wfuzz"])
    subprocess.run(["pip3", "install", "arjun"])
    subprocess.run(["pip3", "install", "scrapy"])
    subprocess.run(["pip3", "install", "tld"])
    subprocess.run(["pip3", "install", "requests"])
    subprocess.run(["pip3", "install", "fuzzywuzzy"])

################
''' Go Tools '''
################

def go_tools():
    print(colored("[+] Installing / Updating Go Tools...", 'green'))
    commands = [
        ["go", "install", "-v", "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"],
        ["go", "install", "-v", "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"],
        ["go", "install", "-v", "github.com/projectdiscovery/katana/cmd/katana@latest"],
        ["go", "install", "-v", "github.com/projectdiscovery/httpx/cmd/httpx@latest"],
        ["go", "install", "-v", "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"],
        ["go", "install", "-v", "github.com/OWASP/Amass/v3/...@master"],
        ["go", "install", "-v", "github.com/tomnomnom/assetfinder@latest"],
        ["go", "install", "-v", "github.com/tomnomnom/httprobe@latest"],
        ["go", "install", "-v", "github.com/sensepost/gowitness@latest"],
        ["go", "install", "-v", "github.com/haccer/subjack@latest"],
        ["go", "install", "-v", "github.com/hakluke/hakrawler@latest"],
        ["go", "install", "-v", "github.com/rverton/webanalyze/cmd/webanalyze@latest"],
    ]

    with ThreadPoolExecutor() as executor:
        results = [executor.submit(subprocess.run, cmd) for cmd in commands]
        for f in as_completed(results):
            print(colored(f.result(), 'green'))

####################
''' Docker Tools '''
####################

def docker_tools():
    # RustScan
    print(colored("[+] Installing / Updating RustScan...", 'green'))
    os.system("docker pull rustscan/rustscan:2.0.1")
    if os.path.isfile("~/.zshrc"):
        print(colored("[+] adding rustscan alias to ~/.zshrc", 'green'))
        with open("~/.zshrc", "a") as f:
            f.write("alias rustscan='docker run -it --rm --name rustscan rustscan/rustscan:2.0.1'")
    elif os.path.isfile("~/.bashrc"):
        print(colored("[+] adding rustscan alias to ~/.bashrc", 'green'))
        with open("~/.bashrc", "a") as f:
            f.write("alias rustscan='docker run -it --rm --name rustscan rustscan/rustscan:2.0.1'")

###############
''' Scripts '''
###############

def useful_scripts():
    def scripts_dir():
        if not os.path.isdir(os.path.expanduser("~/scripts")):
            # os.chdir(["cd", os.path.expanduser("~")])
            os.chdir(os.path.expanduser("~"))
            os.makedirs(os.path.expanduser("~/scripts"), exist_ok=True)
            os.chdir(os.path.expanduser("~/scripts"))
            subprocess.run(["echo", "created", "scripts", "and", "moved", "into", "it"])
        else:
            os.chdir(os.path.expanduser("~/scripts"))
            subprocess.run(["echo", "directory", "/scripts", "already", "exists,", "moving", "into", "it"])

    scripts_dir()

    scripts = ["https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh", "https://github.com/411Hall/JAWS/raw/master/jaws-enum.ps1", "https://github.com/rebootuser/LinEnum/raw/master/LinEnum.sh", "https://github.com/carlospolop/PEASS-ng/releases/download/20230122/winPEASany_ofs.exe", "https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php", "https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh", "https://github.com/PowerShellMafia/PowerSploit/raw/master/Recon/PowerView.ps1"]

    script_threads = []

    def download_script_thread(script):
        subprocess.run(f"wget {script}", shell=True)

    def download_script(scripts):
        for script in tqdm(scripts):
            print(colored(f"[+] Grabbing {script}", 'green'))
            t = threading.Thread(target=download_script_thread, args=(script,))
            script_threads.append(t)
            t.start()

        for t in script_threads:
            t.join()

        print(colored("[*] All scripts downloaded", 'green'))

    download_script(scripts)

try:
    apt_tools()
    opt_tools()
    go_tools()
    docker_tools()
    useful_scripts()
except KeyboardInterrupt:
    print(colored(f"[*] Exiting: KeyboardInterrupt", 'red'))

print(colored("[*] Installation Complete", 'magenta'))
print(colored("[*] Reboot Recommended", 'magenta'))
print(colored("[*] You are now Equipped!", 'green'))
