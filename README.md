# Djedi Toolbelt v2.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)

**Comprehensive security tool installer with interactive menus, pre-built profiles, and distro-specific support.**

---

![Djedi Toolbelt](images/toolbelt.jpeg)

## 🚀 What's New in v2.0

- ✅ **Interactive 3-Level Menu System** - Browse categories, select tools, install profiles
- ✅ **Pre-Built Profiles** - Bug Bounty, CTF, Web App, Network, Full Pentest
- ✅ **Distro Detection** - Kali, Debian, Ubuntu support with appropriate tool sets
- ✅ **No Root Requirement** - Runs as user, uses sudo only when needed
- ✅ **Comprehensive Logging** - Dual output (console + file)
- ✅ **Fresh Integration** - Detects and recommends modern CLI tools
- ✅ **Modular Architecture** - Clean, maintainable Python code

---

## 📋 Quick Start

```bash
# Clone the repository
git clone https://github.com/rpriven/toolbelt.git
cd toolbelt

# Run toolbelt (no sudo needed!)
python3 toolbelt.py
```

**Important:** Do NOT run as root/sudo. The script will use sudo for specific commands that require it.

---

## 🎯 Features

### Interactive Menu System

**Level 1 - Main Menu:**
- Quick Install Profiles
- Browse & Select Categories
- Install Prerequisites (fresh)
- View Installed Tools
- Check for Tool Updates
- Manage Wordlists

**Level 2 - Categories:**
- 📦 APT Tools - Package manager tools
- 🔷 Go Tools - Security tools written in Go
- 🔧 /opt Tools - Tools cloned to /opt
- 🐍 Python Tools - Tools via pip3
- 🐳 Docker Tools - Containerized tools
- 📜 Useful Scripts - PEAS, PowerView, etc.

**Level 3 - Tool Selection:**
- Install all tools in category
- Individual tool selection (gum multi-select)

**Tool Update Management:**
- Check versions of installed tools
- Update all ProjectDiscovery tools (pdtm)
- Update all Go tools to @latest
- Select individual tools to update (gum multi-select)

**Wordlist Management:**
- Install SecLists (comprehensive wordlist collection)
- View installed wordlists and directory structure
- Update SecLists from GitHub

### Pre-Built Profiles

**Bug Bounty Hunter** - Web app testing and reconnaissance
- nmap, masscan, nikto, sqlmap, burpsuite
- nuclei, httpx, subfinder, katana, amass
- Sublist3r, wafw00f, XSStrike
- wfuzz, arjun, scripts collection

**CTF Player** - Capture The Flag tools
- nmap, burpsuite, sqlmap, wireshark
- Python tools: wfuzz, scrapy, requests
- Scripts collection

**Web Application Testing** - Web security focus
- nmap, nikto, sqlmap, burpsuite
- nuclei, httpx, katana
- wafw00f, XSStrike, Striker
- wfuzz, arjun, scrapy

**Network Pentesting** - Network recon and scanning
- nmap, masscan, wireshark
- naabu, amass, assetfinder, httprobe
- RustScan (Docker)

**Full Pentesting Arsenal** - Everything (5GB+)
- All APT tools
- All Go tools
- All /opt tools
- All Python tools
- All Docker tools
- All scripts

---

## 🛠️ Tool Categories

### APT Tools (via package manager)

**Kali Linux:**
nmap, masscan, naabu, nuclei, burpsuite, feroxbuster, nikto, gobuster, seclists, sqlmap, git, docker.io, docker-compose, golang-go, wireshark

**Debian/Ubuntu:**
nmap, masscan, nikto, sqlmap, git, docker.io, docker-compose, golang-go, wireshark, burpsuite

### Go Tools (via go install)

naabu, nuclei, katana, httpx, subfinder, amass, assetfinder, httprobe, gowitness, subjack, hakrawler, webanalyze

*All ProjectDiscovery tools included*

### /opt Tools (cloned to /opt)

- **pimpmykali** (Kali only) - Golang + Impacket setup
- **xnLinkFinder** - Link finder for bug bounty
- **Knockpy** - Subdomain enumeration
- **Sublist3r** - Subdomain discovery
- **Striker** - Web application scanner
- **wafw00f** - WAF detection
- **waymore** - Web archive scraper
- **XSStrike** - XSS detection suite

### Python Tools (via pip3)

wfuzz, arjun, scrapy, tld, requests, fuzzywuzzy

### Docker Tools

**RustScan** - Fast port scanner
- Includes alias setup for shell

### Useful Scripts (downloaded to ~/scripts)

- **linpeas.sh** - Linux privilege escalation
- **jaws-enum.ps1** - Windows enumeration
- **LinEnum.sh** - Linux enumeration
- **winPEASany_ofs.exe** - Windows privilege escalation
- **php-reverse-shell.php** - PHP reverse shell
- **linux-exploit-suggester.sh** - Linux exploit suggester
- **PowerView.ps1** - PowerShell AD enumeration

---

## 🔧 Requirements

- **OS:** Kali Linux, Debian, or Ubuntu
- **Python:** 3.6+
- **Package Manager:** apt
- **Privileges:** sudo access (script runs as user, not root)
- **Optional:** gum (for interactive multi-select) - `go install github.com/charmbracelet/gum@latest`

---

## 📖 Usage Examples

### Install a Profile

```bash
python3 toolbelt.py
# Select: 1) Quick Install Profiles
# Choose: Bug Bounty Hunter
```

### Browse Categories

```bash
python3 toolbelt.py
# Select: 2) Browse & Select Categories
# Choose category (e.g., Go Tools)
# Option 1: Install all tools
# Option 2: Select specific tools (interactive multi-select with gum)
```

### Interactive Tool Selection (gum)

With gum installed, you get beautiful interactive multi-select:

```bash
python3 toolbelt.py
# Select: 2) Browse & Select Categories
# Choose: Go Tools
# Select: 2) Select Specific Tools
# Use SPACE to toggle, ENTER when done
# Confirm selection and install
```

**Without gum:** The script will prompt you to install it or fall back to "Install All" option.

### Check Installed Tools

```bash
python3 toolbelt.py
# Select: 4) View Installed Tools
```

### Update Tools

```bash
python3 toolbelt.py
# Select: 5) Check for Tool Updates

# Option 1: Check versions only (see what's outdated)
# Option 2: Update all ProjectDiscovery tools (pdtm -ua)
# Option 3: Update all Go tools to @latest
# Option 4: Select specific tools to update (gum multi-select)
```

**Update strategies:**
- **Fast PD Update:** Option 2 uses `pdtm` for lightning-fast ProjectDiscovery tool updates
- **Comprehensive Update:** Option 3 updates ALL Go tools (PD + non-PD)
- **Selective Update:** Option 4 lets you cherry-pick which tools to update

### Manage Wordlists

```bash
python3 toolbelt.py
# Select: 6) Manage Wordlists

# Option 1: Install SecLists (~500MB)
# Option 2: View installed wordlists and structure
# Option 3: Update SecLists from GitHub
```

**SecLists includes:**
- **Passwords**: rockyou, common passwords, leaked databases
- **Usernames**: Common usernames and names
- **Subdomains**: DNS enumeration wordlists
- **Directories**: Web content discovery lists
- **Fuzzing**: XSS, SQLi, and other injection payloads

**Installation location:** `~/wordlists/SecLists/`

---

## 🔗 Integration with Fresh

Toolbelt integrates with [fresh](https://github.com/rpriven/fresh) for modern CLI productivity tools.

**Recommended Setup:**

1. **Install fresh first** - Modern CLI foundation (fzf, ripgrep, bat, etc.)
2. **Install toolbelt** - Security tools
3. **Install tmux-recon** (optional) - Pentesting automation

Fresh provides essential CLI tools that enhance the security workflow. Toolbelt will detect if fresh is installed and prompt you to install it if missing.

---

## 📂 Architecture

```
toolbelt/
├── toolbelt.py      # Main entry point with interactive menus
├── utils.py         # Distro detection, logging, helpers
├── config.py        # Tool definitions, profiles, categories
├── installer.py     # Installation logic for each category
├── toolbelt_old.py  # Original v1.0 (reference)
└── toolbelt.sh.old  # Legacy bash version (archived)
```

**Modular Design:**
- `utils.py` - System checks, logging setup, helper functions
- `config.py` - Tool lists, profile definitions, category metadata
- `installer.py` - Installation functions for each tool category
- `toolbelt.py` - Interactive menu system and main flow

---

## 🔐 Security Notes

- **No Root Execution**: Script runs as regular user, uses sudo only for specific commands
- **Logging**: All operations logged to `~/toolbelt-install.log`
- **Smart Detection**: Skips already-installed tools
- **Error Handling**: Comprehensive error checking and reporting

---

## 🐛 Known Issues

- Individual tool selection menu (Level 3) coming in next update
- Custom profile saving/loading planned for future release

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests or open issues for:
- Additional tool suggestions
- New profiles
- Platform support improvements
- Bug fixes

---

## 📝 Version History

**v2.0.0** (2025-10-31)
- Complete rewrite with interactive menu system
- Pre-built profile support
- Distro detection (Kali, Debian, Ubuntu)
- Removed root requirement
- Added comprehensive logging
- Fresh integration
- Modular architecture

**v1.0** (2023)
- Original automated installer
- Bash and Python versions
- Root required
- No menu system

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built for the pentesting and bug bounty community
- Integrates tools from ProjectDiscovery, OWASP, and many open source developers
- Inspired by the need for quick, consistent tool setup across environments
- Part of the Djedi security tooling ecosystem

---

**Djedi Toolbelt** - Because every pentester deserves a well-equipped toolbelt. 🔧
