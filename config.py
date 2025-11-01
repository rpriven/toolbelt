#!/usr/bin/env python3
"""
Djedi Toolbelt - Configuration and Tool Definitions
Defines all tools, categories, and profiles
"""

from typing import Dict, List

# ============================================================================
# Tool Categories
# ============================================================================

# APT Tools - Available via package manager
APT_TOOLS_KALI = [
    "nmap",
    "masscan",
    "naabu",
    "nuclei",
    "burpsuite",
    "feroxbuster",
    "nikto",
    "gobuster",
    "seclists",
    "sqlmap",
    "git",
    "docker.io",
    "docker-compose",
    "golang-go",
    "wireshark",
]

APT_TOOLS_DEBIAN = [
    "nmap",
    "masscan",
    "nikto",
    "sqlmap",
    "git",
    "docker.io",
    "docker-compose",
    "golang-go",
    "wireshark",
    "burpsuite",  # Community edition available in some repos
]

# /opt Tools - Cloned to /opt directory
OPT_TOOLS = {
    "pimpmykali": {
        "url": "https://github.com/Dewalt-arch/pimpmykali",
        "post_install": [
            "cd /opt/pimpmykali && sudo ./pimpmykali.sh --go",
            "cd /opt/pimpmykali && sudo ./pimpmykali.sh --impacket",
            "cd /opt/pimpmykali && sudo ./pimpmykali.sh --upgrade"
        ],
        "kali_only": True
    },
    "xnLinkFinder": {
        "url": "https://github.com/xnl-h4ck3r/xnLinkFinder.git",
        "post_install": ["cd /opt/xnLinkFinder && sudo python setup.py install"],
        "kali_only": False
    },
    "knock": {
        "url": "https://github.com/guelfoweb/knock.git",
        "post_install": ["cd /opt/knock && pip3 install -r requirements.txt"],
        "kali_only": False
    },
    "Sublist3r": {
        "url": "https://github.com/aboul3la/Sublist3r.git",
        "post_install": ["cd /opt/Sublist3r && pip install -r requirements.txt"],
        "kali_only": False
    },
    "Striker": {
        "url": "https://github.com/s0md3v/Striker.git",
        "post_install": ["cd /opt/Striker && pip install -r requirements.txt"],
        "kali_only": False
    },
    "wafw00f": {
        "url": "https://github.com/EnableSecurity/wafw00f.git",
        "post_install": [
            "cd /opt/wafw00f && pip3 install -r requirements.txt",
            "cd /opt/wafw00f && sudo python setup.py install"
        ],
        "kali_only": False
    },
    "waymore": {
        "url": "https://github.com/xnl-h4ck3r/waymore.git",
        "post_install": [
            "cd /opt/waymore && pip3 install -r requirements.txt",
            "cd /opt/waymore && sudo python setup.py install"
        ],
        "kali_only": False
    },
    "XSStrike": {
        "url": "https://github.com/s0md3v/XSStrike.git",
        "post_install": ["cd /opt/XSStrike && pip3 install -r requirements.txt"],
        "kali_only": False
    },
}

# Python Tools - Installed via pip3
PYTHON_TOOLS = [
    "wfuzz",
    "arjun",
    "scrapy",
    "tld",
    "requests",
    "fuzzywuzzy",
]

# Go Tools - Installed via go install
GO_TOOLS = {
    "naabu": "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
    "nuclei": "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest",
    "katana": "github.com/projectdiscovery/katana/cmd/katana@latest",
    "httpx": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
    "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
    "amass": "github.com/OWASP/Amass/v3/...@master",
    "assetfinder": "github.com/tomnomnom/assetfinder@latest",
    "httprobe": "github.com/tomnomnom/httprobe@latest",
    "gowitness": "github.com/sensepost/gowitness@latest",
    "subjack": "github.com/haccer/subjack@latest",
    "hakrawler": "github.com/hakluke/hakrawler@latest",
    "webanalyze": "github.com/rverton/webanalyze/cmd/webanalyze@latest",
}

# Docker Tools
DOCKER_TOOLS = {
    "rustscan": {
        "image": "rustscan/rustscan:2.0.1",
        "alias": "alias rustscan='docker run -it --rm --name rustscan rustscan/rustscan:2.0.1'"
    },
}

# Useful Scripts - Downloaded to ~/scripts
USEFUL_SCRIPTS = {
    "linpeas.sh": "https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh",
    "jaws-enum.ps1": "https://github.com/411Hall/JAWS/raw/master/jaws-enum.ps1",
    "LinEnum.sh": "https://github.com/rebootuser/LinEnum/raw/master/LinEnum.sh",
    "winPEASany_ofs.exe": "https://github.com/carlospolop/PEASS-ng/releases/download/20230122/winPEASany_ofs.exe",
    "php-reverse-shell.php": "https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php",
    "linux-exploit-suggester.sh": "https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh",
    "PowerView.ps1": "https://github.com/PowerShellMafia/PowerSploit/raw/master/Recon/PowerView.ps1",
}

# ============================================================================
# Installation Profiles
# ============================================================================

PROFILES = {
    "bug-bounty": {
        "name": "Bug Bounty Hunter",
        "description": "Tools for bug bounty hunting and web application testing",
        "categories": {
            "apt": ["nmap", "masscan", "nikto", "sqlmap", "burpsuite", "git"],
            "go": ["nuclei", "httpx", "subfinder", "katana", "amass", "assetfinder", "httprobe"],
            "opt": ["Sublist3r", "wafw00f", "XSStrike"],
            "python": ["wfuzz", "arjun", "requests"],
            "scripts": True,  # Install all scripts
        }
    },
    "ctf": {
        "name": "CTF Player",
        "description": "Tools for Capture The Flag competitions",
        "categories": {
            "apt": ["nmap", "burpsuite", "sqlmap", "git", "wireshark"],
            "python": ["wfuzz", "scrapy", "requests"],
            "scripts": True,
        }
    },
    "web-app": {
        "name": "Web Application Testing",
        "description": "Focused on web application security testing",
        "categories": {
            "apt": ["nmap", "nikto", "sqlmap", "burpsuite"],
            "go": ["nuclei", "httpx", "katana"],
            "opt": ["wafw00f", "XSStrike", "Striker"],
            "python": ["wfuzz", "arjun", "scrapy"],
        }
    },
    "network": {
        "name": "Network Pentesting",
        "description": "Network reconnaissance and scanning tools",
        "categories": {
            "apt": ["nmap", "masscan", "wireshark"],
            "go": ["naabu", "amass", "assetfinder", "httprobe"],
            "docker": ["rustscan"],
        }
    },
    "full-pentest": {
        "name": "Full Pentesting Arsenal",
        "description": "Complete toolset for comprehensive penetration testing",
        "categories": {
            "apt": "all",
            "go": "all",
            "opt": "all",
            "python": "all",
            "docker": "all",
            "scripts": True,
        }
    },
}

# ============================================================================
# Category Metadata
# ============================================================================

CATEGORIES = {
    "apt": {
        "name": "APT Tools",
        "description": "Tools installed via apt package manager",
        "icon": "📦",
        "requires_sudo": True,
    },
    "go": {
        "name": "Go Tools",
        "description": "Security tools written in Go",
        "icon": "🔷",
        "requires_sudo": False,
    },
    "opt": {
        "name": "/opt Tools",
        "description": "Tools cloned to /opt directory",
        "icon": "🔧",
        "requires_sudo": True,
    },
    "python": {
        "name": "Python Tools",
        "description": "Tools installed via pip3",
        "icon": "🐍",
        "requires_sudo": False,
    },
    "docker": {
        "name": "Docker Tools",
        "description": "Containerized security tools",
        "icon": "🐳",
        "requires_sudo": False,
    },
    "scripts": {
        "name": "Useful Scripts",
        "description": "PEAS, PowerView, and other scripts",
        "icon": "📜",
        "requires_sudo": False,
    },
}

# ============================================================================
# Helper Functions
# ============================================================================

def get_apt_tools_for_distro(distro_type: str) -> List[str]:
    """
    Get appropriate APT tools list for distro

    Args:
        distro_type: One of 'kali', 'debian', 'ubuntu', 'unknown'

    Returns:
        List of APT package names
    """
    if distro_type == 'kali':
        return APT_TOOLS_KALI
    elif distro_type in ['debian', 'ubuntu']:
        return APT_TOOLS_DEBIAN
    else:
        # Conservative list for unknown distros
        return [
            "nmap",
            "nikto",
            "sqlmap",
            "git",
            "docker.io",
        ]


def get_opt_tools_for_distro(distro_type: str) -> Dict:
    """
    Get appropriate /opt tools for distro

    Args:
        distro_type: One of 'kali', 'debian', 'ubuntu', 'unknown'

    Returns:
        Dictionary of /opt tools
    """
    if distro_type == 'kali':
        return OPT_TOOLS

    # Filter out Kali-only tools for other distros
    return {
        name: config
        for name, config in OPT_TOOLS.items()
        if not config.get('kali_only', False)
    }


def get_profile(profile_name: str) -> Dict:
    """
    Get profile configuration by name

    Args:
        profile_name: Profile identifier

    Returns:
        Profile configuration dictionary or None
    """
    return PROFILES.get(profile_name)


def list_profiles() -> List[str]:
    """
    Get list of available profile names

    Returns:
        List of profile names
    """
    return list(PROFILES.keys())
