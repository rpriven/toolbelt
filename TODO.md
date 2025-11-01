# Toolbelt Enhancement TODO

## v2.1 Priority Features

### 1. Tool Update Detection ⭐⭐⭐
**Priority: HIGH**

Check which Go tools have updates available and provide interactive update menu.

```python
# Compare installed version vs @latest
# Show which tools need updates
# Bulk update option
```

**Implementation:**
- Query `go list -m` for installed versions
- Compare against `@latest` from go.dev
- Interactive menu to select which tools to update

---

### 2. Individual Tool Selection (Level 3) ⭐⭐⭐
**Priority: HIGH**

Replace "Coming Soon" with actual tool selection using gum.

**Using `gum choose --no-limit` for multi-select:**

```bash
# Install gum first
go install github.com/charmbracelet/gum@latest

# Then use in Python via subprocess
selected = subprocess.run(
    ['gum', 'choose', '--no-limit'] + tool_list,
    capture_output=True,
    text=True
).stdout.strip().split('\n')
```

**Implementation Plan:**
1. Add gum as optional dependency (install if not present)
2. In `tool_selection_menu()`, replace option 2 with gum multi-select
3. Pass selected tools to category installer
4. Fallback to sequential selection if gum not available

**Example:**
```python
def select_apt_tools(distro_type: str) -> List[str]:
    """Let user select specific APT tools with gum multi-select"""
    all_tools = config.get_apt_tools_for_distro(distro_type)

    if check_command_exists('gum'):
        # Multi-select with gum
        result = subprocess.run(
            ['gum', 'choose', '--no-limit', '--header', 'Select tools to install:'] + all_tools,
            capture_output=True,
            text=True
        )
        selected = [t for t in result.stdout.strip().split('\n') if t]
        return selected
    else:
        # Fallback: show list, let user pick
        print_warning("Install gum for multi-select: go install github.com/charmbracelet/gum@latest")
        # ... manual selection loop
```

---

### 3. Wordlist Management ⭐⭐
**Priority: MEDIUM**

Download and organize common wordlists for pentesting.

**Wordlists to Include:**
- SecLists (already in APT tools, but organize it)
- rockyou.txt
- Daniel Miessler's lists
- Custom wordlists for subdomains, directories, passwords

**Directory Structure:**
```
~/wordlists/
├── passwords/
│   ├── rockyou.txt
│   └── common-passwords.txt
├── subdomains/
│   ├── subdomains-top1mil.txt
│   └── dns-bruteforce.txt
├── directories/
│   ├── common.txt
│   └── raft-large-directories.txt
└── usernames/
    └── common-usernames.txt
```

**Implementation:**
- New category: "Wordlist Management"
- Download from GitHub releases
- Extract and organize
- Create symlinks to common locations

---

### 4. Resource Monitoring ⭐⭐
**Priority: MEDIUM**

Show disk space requirements before installation.

**Features:**
- Check available disk space
- Estimate download size per category
- Warn if insufficient space
- Show progress during large downloads

**Implementation:**
```python
def check_disk_space(required_gb: float) -> bool:
    """Check if enough disk space available"""
    stat = os.statvfs(os.path.expanduser('~'))
    available_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)

    if available_gb < required_gb:
        print_error(f"Insufficient disk space!")
        print_info(f"Required: {required_gb}GB, Available: {available_gb:.1f}GB")
        return False
    return True
```

---

### 5. Tool Usage Instructions (tldr) ⭐⭐
**Priority: MEDIUM**

Show basic usage examples after installing each tool.

**Using tldr pages:**
```bash
# Install tldr
pip3 install tldr

# Show usage
tldr nuclei
```

**Implementation:**
```python
def show_tool_usage(tool_name: str):
    """Display quick usage guide for tool"""
    if check_command_exists('tldr'):
        subprocess.run(['tldr', tool_name])
    else:
        # Fallback: show our own examples from config
        if tool_name in TOOL_EXAMPLES:
            print_info(f"\nQuick Start for {tool_name}:")
            print(TOOL_EXAMPLES[tool_name])
```

**Add to config.py:**
```python
TOOL_EXAMPLES = {
    "nuclei": "nuclei -t /path/to/templates -u https://target.com",
    "httpx": "cat domains.txt | httpx -status-code -title",
    "subfinder": "subfinder -d target.com -o subdomains.txt",
    # ... etc
}
```

---

### 6. Export/Import Configuration ⭐
**Priority: LOW**

Save and restore custom tool selections.

**Format:**
```json
{
  "name": "my-custom-setup",
  "created": "2025-10-31",
  "distro": "kali",
  "tools": {
    "apt": ["nmap", "masscan", "burpsuite"],
    "go": ["nuclei", "httpx", "subfinder"],
    "scripts": true
  }
}
```

**Implementation:**
- Save to `~/.config/toolbelt/configs/`
- Load previous configs
- Share between systems

---

### 7. Workspace Setup ⭐
**Priority: LOW**

Create standard pentesting directory structure.

**Directory Tree:**
```
~/pentesting/
├── targets/
│   └── example.com/
│       ├── recon/
│       ├── scans/
│       └── loot/
├── wordlists/  (symlink to ~/wordlists)
├── tools/      (symlink to /opt)
└── reports/
```

**Implementation:**
- New menu option: "Setup Workspace"
- Creates directories
- Adds .gitignore templates
- Initializes git repos where appropriate

---

### 8. Tmux Integration (via tmux-recon) ⭐⭐⭐
**Priority: HIGH** (After tmux-recon.py is done)

**Menu Option:**
```
7) 🚀 Launch Pentesting Environment (tmux-recon)
   Advanced shell environment with tmux automation
```

**Action:**
- Check if tmux-recon is installed
- If not, prompt to clone and install
- If yes, launch tmux-recon automation

**Implementation:**
```python
def launch_tmux_environment():
    """Launch tmux-recon pentesting environment"""
    if not os.path.exists('/opt/tmux-recon'):
        print_warning("tmux-recon not installed")
        response = input("Clone and install tmux-recon? [y/N]: ")
        if response.lower() == 'y':
            # Clone and run tmux-recon
            pass
    else:
        # Launch tmux-recon
        subprocess.run(['/opt/tmux-recon/tmux-recon.py', '--auto'])
```

---

### 9. Health Check / Verify Installation ⭐
**Priority: LOW**

Verify all installed tools are working correctly.

**Checks:**
- Run `--version` or `--help` on each tool
- Verify can execute
- Check for broken symlinks
- Report missing dependencies

**Implementation:**
```python
def health_check():
    """Verify all installed tools work"""
    broken_tools = []

    for tool in installed_tools:
        try:
            subprocess.run([tool, '--version'],
                         capture_output=True,
                         timeout=5)
        except Exception:
            broken_tools.append(tool)

    if broken_tools:
        print_error(f"Broken tools: {', '.join(broken_tools)}")
```

---

### 10. Progress Bars for Large Downloads ⭐
**Priority: LOW**

Better visual feedback during installation.

**Using tqdm:**
```python
from tqdm import tqdm

def download_with_progress(url: str, output: str):
    """Download with progress bar"""
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))

    with open(output, 'wb') as f, tqdm(
        total=total,
        unit='B',
        unit_scale=True,
        desc=output
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))
```

---

## Implementation Priority

**v2.1 (Next Release):**
1. Individual Tool Selection (gum multi-select) ✅ **COMPLETED**
2. Tool Update Detection ✅ **COMPLETED**
3. Wordlist Management 🔜

**v2.2:**
4. Resource Monitoring
5. Usage Instructions (tldr)
6. Tmux-recon Integration

**v2.3:**
7. Export/Import Configs
8. Workspace Setup
9. Health Check
10. Progress Bars

---

## Notes

- All features should maintain modular architecture
- Add comprehensive logging for new features
- Update README with each release
- Keep Python type hints for all new code
