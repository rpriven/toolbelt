#!/usr/bin/env python3
"""
Djedi Toolbelt v2.0 - Security Tool Installer
Interactive package manager for pentesting and security research tools
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict

# Import local modules
from utils import (
    setup_logging,
    detect_distro,
    check_root_discourage,
    check_apt,
    check_sudo,
    check_command_exists,
    gum_multi_select,
    print_banner,
    print_section,
    print_success,
    print_info,
    print_warning,
    print_error,
    colorize,
)
import config
import installer


# ============================================================================
# Fresh Detection & Integration
# ============================================================================

def check_fresh_installed() -> bool:
    """Check if fresh CLI tools are installed"""
    fresh_tools = ['fzf', 'rg', 'bat']
    return all(check_command_exists(tool) for tool in fresh_tools)


def prompt_install_fresh():
    """Prompt user to install fresh if not detected"""
    if check_fresh_installed():
        return

    print()
    print_warning("Fresh CLI tools not detected")
    print_info("Fresh provides modern CLI productivity tools (fzf, ripgrep, bat, etc.)")
    print_info("Repository: https://github.com/rpriven/fresh")
    print()

    response = input(colorize("Would you like to install fresh first? [y/N]: ", 'yellow')).strip().lower()
    if response == 'y':
        print()
        print_info("To install fresh, run:")
        print()
        print("  git clone https://github.com/rpriven/fresh.git && cd fresh")
        print("  ./fresh.sh")
        print()
        print_info("Then come back and run toolbelt again!")
        sys.exit(0)


# ============================================================================
# Level 1: Main Menu
# ============================================================================

def show_main_menu(distro_name: str, distro_type: str):
    """Display the main menu"""
    print_banner()
    print(colorize(f"Detected: {distro_name}", 'cyan'))
    print()
    print(colorize("=" * 60, 'white'))
    print(colorize("  MAIN MENU", 'cyan'))
    print(colorize("=" * 60, 'white'))
    print()
    print(colorize("1)", 'green') + " Quick Install Profiles")
    print(colorize("2)", 'green') + " Browse & Select Categories")
    print(colorize("3)", 'green') + " Install Prerequisites (fresh)")
    print(colorize("4)", 'green') + " View Installed Tools")
    print(colorize("5)", 'green') + " Check for Tool Updates")
    print(colorize("6)", 'green') + " Manage Wordlists")
    print()
    print(colorize("0)", 'red') + " Exit")
    print()


def main_menu_loop(distro_name: str, distro_type: str, logger):
    """Main menu interaction loop"""
    while True:
        show_main_menu(distro_name, distro_type)
        choice = input(colorize("Select option: ", 'yellow')).strip()

        if choice == '1':
            profile_menu(distro_type, logger)
        elif choice == '2':
            category_menu(distro_type, logger)
        elif choice == '3':
            prompt_install_fresh()
        elif choice == '4':
            view_installed_tools()
        elif choice == '5':
            update_tools_menu(logger)
        elif choice == '6':
            wordlist_menu(logger)
        elif choice == '0':
            print()
            print_success("Thank you for using Djedi Toolbelt!")
            sys.exit(0)
        else:
            print_error("Invalid option. Please try again.")
            input("\nPress Enter to continue...")


# ============================================================================
# Level 2: Profile Menu
# ============================================================================

def show_profile_menu():
    """Display profile selection menu"""
    print_section("QUICK INSTALL PROFILES")

    profiles = config.PROFILES
    idx = 1
    profile_map = {}

    for profile_id, profile_info in profiles.items():
        print(f"{colorize(str(idx) + ')', 'green')} {colorize(profile_info['name'], 'white')}")
        print(f"   {profile_info['description']}")
        print()
        profile_map[str(idx)] = profile_id
        idx += 1

    print(colorize("0)", 'red') + " Back to Main Menu")
    print()

    return profile_map


def install_profile(profile_id: str, distro_type: str, logger):
    """Install tools from a profile"""
    profile = config.get_profile(profile_id)
    if not profile:
        print_error(f"Profile not found: {profile_id}")
        return

    print_section(f"Installing Profile: {profile['name']}")
    print_info(profile['description'])
    print()

    categories = profile['categories']

    # APT Tools
    if 'apt' in categories:
        if categories['apt'] == 'all':
            installer.install_apt_tools(distro_type=distro_type, logger=logger)
        elif isinstance(categories['apt'], list):
            installer.install_apt_tools(tools=categories['apt'], distro_type=distro_type, logger=logger)

    # Go Tools
    if 'go' in categories:
        if categories['go'] == 'all':
            installer.install_go_tools(logger=logger)
        elif isinstance(categories['go'], list):
            installer.install_go_tools(tools=categories['go'], logger=logger)

    # /opt Tools
    if 'opt' in categories:
        if categories['opt'] == 'all':
            installer.install_opt_tools(distro_type=distro_type, logger=logger)
        elif isinstance(categories['opt'], list):
            installer.install_opt_tools(tools=categories['opt'], distro_type=distro_type, logger=logger)

    # Python Tools
    if 'python' in categories:
        if categories['python'] == 'all':
            installer.install_python_tools(logger=logger)
        elif isinstance(categories['python'], list):
            installer.install_python_tools(tools=categories['python'], logger=logger)

    # Docker Tools
    if 'docker' in categories:
        if categories['docker'] == 'all':
            installer.install_docker_tools(logger=logger)
        elif isinstance(categories['docker'], list):
            installer.install_docker_tools(tools=categories['docker'], logger=logger)

    # Scripts
    if 'scripts' in categories and categories['scripts']:
        installer.download_useful_scripts(logger=logger)

    print()
    print_success(f"Profile '{profile['name']}' installation complete!")
    input("\nPress Enter to continue...")


def profile_menu(distro_type: str, logger):
    """Profile selection menu"""
    while True:
        profile_map = show_profile_menu()
        choice = input(colorize("Select profile: ", 'yellow')).strip()

        if choice == '0':
            return
        elif choice in profile_map:
            install_profile(profile_map[choice], distro_type, logger)
        else:
            print_error("Invalid option. Please try again.")
            input("\nPress Enter to continue...")


# ============================================================================
# Level 2: Category Menu
# ============================================================================

def show_category_menu():
    """Display category selection menu"""
    print_section("BROWSE & SELECT CATEGORIES")

    idx = 1
    category_map = {}

    for cat_id, cat_info in config.CATEGORIES.items():
        icon = cat_info.get('icon', '•')
        name = cat_info['name']
        desc = cat_info['description']

        print(f"{colorize(str(idx) + ')', 'green')} {icon} {colorize(name, 'white')}")
        print(f"   {desc}")
        print()

        category_map[str(idx)] = cat_id
        idx += 1

    print(colorize("0)", 'red') + " Back to Main Menu")
    print()

    return category_map


def category_menu(distro_type: str, logger):
    """Category selection menu"""
    while True:
        category_map = show_category_menu()
        choice = input(colorize("Select category: ", 'yellow')).strip()

        if choice == '0':
            return
        elif choice in category_map:
            category_id = category_map[choice]
            tool_selection_menu(category_id, distro_type, logger)
        else:
            print_error("Invalid option. Please try again.")
            input("\nPress Enter to continue...")


# ============================================================================
# Level 3: Tool Selection Menu
# ============================================================================

def show_tool_selection_menu(category_id: str, distro_type: str):
    """Display tool selection menu for a category"""
    cat_info = config.CATEGORIES[category_id]
    print_section(f"{cat_info['icon']} {cat_info['name']}")
    print_info(cat_info['description'])
    print()

    # Check if gum is available
    has_gum = check_command_exists('gum')

    print(colorize("1)", 'green') + " Install All Tools in Category")
    if has_gum:
        print(colorize("2)", 'green') + " Select Specific Tools (multi-select)")
    else:
        print(colorize("2)", 'green') + " Select Specific Tools (requires gum)")
        print_info("   Install gum: go install github.com/charmbracelet/gum@latest")
    print()
    print(colorize("0)", 'red') + " Back")
    print()


def tool_selection_menu(category_id: str, distro_type: str, logger):
    """Tool selection menu for a category"""
    while True:
        show_tool_selection_menu(category_id, distro_type)
        choice = input(colorize("Select option: ", 'yellow')).strip()

        if choice == '0':
            return
        elif choice == '1':
            install_category_all(category_id, distro_type, logger)
        elif choice == '2':
            install_category_selected(category_id, distro_type, logger)
        else:
            print_error("Invalid option. Please try again.")
            input("\nPress Enter to continue...")


def install_category_all(category_id: str, distro_type: str, logger):
    """Install all tools in a category"""
    cat_info = config.CATEGORIES[category_id]
    print_section(f"Installing All {cat_info['name']}")

    success = False

    if category_id == 'apt':
        success = installer.install_apt_tools(distro_type=distro_type, logger=logger)
    elif category_id == 'go':
        success = installer.install_go_tools(logger=logger)
    elif category_id == 'opt':
        success = installer.install_opt_tools(distro_type=distro_type, logger=logger)
    elif category_id == 'python':
        success = installer.install_python_tools(logger=logger)
    elif category_id == 'docker':
        success = installer.install_docker_tools(logger=logger)
    elif category_id == 'scripts':
        success = installer.download_useful_scripts(logger=logger)

    print()
    if success:
        print_success(f"{cat_info['name']} installation complete!")
    else:
        print_warning(f"{cat_info['name']} installation completed with some errors")

    input("\nPress Enter to continue...")


def install_category_selected(category_id: str, distro_type: str, logger):
    """Install selected tools from a category using gum multi-select"""
    cat_info = config.CATEGORIES[category_id]

    # Check if gum is available
    if not check_command_exists('gum'):
        print()
        print_error("gum is not installed!")
        print_info("gum is required for interactive multi-select")
        print()
        print_info("Install gum with:")
        print("  go install github.com/charmbracelet/gum@latest")
        print()
        print_info("Make sure $GOPATH/bin is in your PATH")
        print()
        input("Press Enter to continue...")
        return

    print_section(f"Select {cat_info['name']}")

    # Get tool list based on category
    tools_list: List[str] = []

    if category_id == 'apt':
        tools_list = config.get_apt_tools_for_distro(distro_type)
    elif category_id == 'go':
        tools_list = list(config.GO_TOOLS.keys())
    elif category_id == 'opt':
        tools_list = list(config.get_opt_tools_for_distro(distro_type).keys())
    elif category_id == 'python':
        tools_list = config.PYTHON_TOOLS  # Already a list, not a dict
    elif category_id == 'docker':
        tools_list = list(config.DOCKER_TOOLS.keys())
    elif category_id == 'scripts':
        print()
        print_info("Scripts category downloads all scripts as a set")
        print_info("Use option 1 to install all scripts")
        print()
        input("Press Enter to continue...")
        return

    if not tools_list:
        print_error(f"No tools available for {cat_info['name']}")
        input("\nPress Enter to continue...")
        return

    # Show count
    print_info(f"Available tools: {len(tools_list)}")
    print()
    print(colorize("TIP: Use SPACE to select, ENTER when done, Ctrl+C to cancel", 'yellow'))
    print()

    # Use gum for multi-select
    selected = gum_multi_select(
        tools_list,
        header=f"Select {cat_info['name']} to install:"
    )

    if not selected:
        print()
        print_warning("No tools selected")
        input("\nPress Enter to continue...")
        return

    # Show what was selected
    print()
    print_section(f"Installing {len(selected)} Selected Tools")
    for tool in selected:
        print(colorize(f"  • {tool}", 'cyan'))
    print()

    # Confirm installation
    response = input(colorize("Proceed with installation? [Y/n]: ", 'yellow')).strip().lower()
    if response == 'n':
        print_warning("Installation cancelled")
        input("\nPress Enter to continue...")
        return

    # Install selected tools
    success = False

    if category_id == 'apt':
        success = installer.install_apt_tools(tools=selected, distro_type=distro_type, logger=logger)
    elif category_id == 'go':
        success = installer.install_go_tools(tools=selected, logger=logger)
    elif category_id == 'opt':
        success = installer.install_opt_tools(tools=selected, distro_type=distro_type, logger=logger)
    elif category_id == 'python':
        success = installer.install_python_tools(tools=selected, logger=logger)
    elif category_id == 'docker':
        success = installer.install_docker_tools(tools=selected, logger=logger)

    print()
    if success:
        print_success(f"Selected {cat_info['name']} installation complete!")
    else:
        print_warning(f"Selected {cat_info['name']} installation completed with some errors")

    input("\nPress Enter to continue...")


# ============================================================================
# View Installed Tools
# ============================================================================

def view_installed_tools():
    """Display currently installed tools"""
    print_section("INSTALLED TOOLS")

    # Check APT tools
    print(colorize("📦 APT Tools:", 'cyan'))
    apt_tools = config.get_apt_tools_for_distro('kali')  # Use max list
    for tool in apt_tools:
        check_name = tool.replace('.io', '').replace('-', '')
        if check_command_exists(check_name):
            print(colorize(f"  ✓ {tool}", 'green'))

    print()

    # Check Go tools
    print(colorize("🔷 Go Tools:", 'cyan'))
    for tool_name in config.GO_TOOLS.keys():
        if check_command_exists(tool_name):
            print(colorize(f"  ✓ {tool_name}", 'green'))

    print()

    # Check Docker tools
    print(colorize("🐳 Docker Tools:", 'cyan'))
    for tool_name in config.DOCKER_TOOLS.keys():
        if check_command_exists(tool_name):
            print(colorize(f"  ✓ {tool_name}", 'green'))

    print()
    input("Press Enter to continue...")


# ============================================================================
# Tool Update Management
# ============================================================================

def update_tools_menu(logger):
    """Tool update management menu"""
    while True:
        print_section("🔄 TOOL UPDATE MANAGEMENT")

        print(colorize("1)", 'green') + " 📊 Check Versions Only")
        print("   Show which tools are outdated")
        print()
        print(colorize("2)", 'green') + " ⚡ Update All ProjectDiscovery Tools")
        print("   Fast bulk update using pdtm")
        print()
        print(colorize("3)", 'green') + " 🔧 Update All Go Tools")
        print("   Update all Go tools to @latest")
        print()
        print(colorize("4)", 'green') + " 🎯 Select Individual Tools to Update")
        print("   Choose specific tools with multi-select")
        print()
        print(colorize("0)", 'red') + " Back to Main Menu")
        print()

        choice = input(colorize("Select option: ", 'yellow')).strip()

        if choice == '0':
            return
        elif choice == '1':
            check_tool_versions(logger)
        elif choice == '2':
            update_pd_tools_bulk(logger)
        elif choice == '3':
            update_all_go_tools(logger)
        elif choice == '4':
            update_selected_tools(logger)
        else:
            print_error("Invalid option. Please try again.")
            input("\nPress Enter to continue...")


def check_tool_versions(logger):
    """Check and display tool versions vs latest"""
    print_section("📊 Checking Tool Versions")

    print_info("Checking installed Go tools...")
    print()

    outdated = []
    up_to_date = []
    not_installed = []

    for tool_name, module_path in config.GO_TOOLS.items():
        # Check if tool is installed
        if not check_command_exists(tool_name):
            not_installed.append(tool_name)
            continue

        # Get installed version
        try:
            result = subprocess.run(
                [tool_name, '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Try to extract just the version number, not the full banner
            version_output = result.stdout.strip() or result.stderr.strip()

            # Many tools print version on first line - extract it
            if version_output:
                first_line = version_output.split('\n')[0]
                # Look for version patterns like "v1.2.3" or "1.2.3"
                import re
                version_match = re.search(r'v?\d+\.\d+\.\d+', first_line)
                if version_match:
                    installed_version = version_match.group(0)
                else:
                    # Fallback to first line if no version pattern found
                    installed_version = first_line[:50]
            else:
                installed_version = "installed"

            up_to_date.append((tool_name, installed_version))

        except Exception as e:
            logger.debug(f"Could not get version for {tool_name}: {e}")
            up_to_date.append((tool_name, "installed"))

    # Display results
    if up_to_date:
        print(colorize("✓ Installed Tools:", 'green'))
        for tool, version in up_to_date:
            version_str = version[:50] + "..." if len(version) > 50 else version
            print(f"  • {tool}: {version_str}")
        print()

    if not_installed:
        print(colorize("○ Not Installed:", 'yellow'))
        for tool in not_installed:
            print(f"  • {tool}")
        print()

    print_info("💡 To update tools, use options 2-4 from the update menu")
    print()
    input("Press Enter to continue...")


def update_pd_tools_bulk(logger):
    """Update all ProjectDiscovery tools using pdtm"""
    print_section("⚡ Updating ProjectDiscovery Tools")

    # Check if pdtm is installed
    if not check_command_exists('pdtm'):
        print_warning("pdtm not found!")
        print_info("Installing pdtm...")
        try:
            subprocess.run(
                ['go', 'install', '-v', 'github.com/projectdiscovery/pdtm/cmd/pdtm@latest'],
                check=True
            )
            print_success("pdtm installed successfully")
        except Exception as e:
            print_error(f"Failed to install pdtm: {e}")
            logger.error(f"Failed to install pdtm: {e}")
            input("\nPress Enter to continue...")
            return

    print_info("Running: pdtm -ua (update all)")
    print()

    try:
        # Run pdtm with direct terminal access
        result = subprocess.run(
            ['pdtm', '-ua'],
            check=False  # Don't raise on non-zero exit
        )

        print()
        if result.returncode == 0:
            print_success("ProjectDiscovery tools updated successfully!")
        else:
            print_warning("Update completed with some issues")

        logger.info(f"pdtm update completed with exit code {result.returncode}")

    except Exception as e:
        print_error(f"Update failed: {e}")
        logger.error(f"pdtm update failed: {e}", exc_info=True)

    print()
    input("Press Enter to continue...")


def update_all_go_tools(logger):
    """Update all Go tools to @latest"""
    print_section("🔧 Updating All Go Tools")

    print_warning("This will update ALL Go tools to @latest")
    print_info(f"Total tools: {len(config.GO_TOOLS)}")
    print()

    # List all tools that will be updated
    print(colorize("Tools to update:", 'cyan'))
    for tool_name in config.GO_TOOLS.keys():
        # Check if installed
        if check_command_exists(tool_name):
            print(colorize(f"  ✓ {tool_name}", 'green'))
        else:
            print(colorize(f"  ○ {tool_name} (not installed, will skip)", 'yellow'))
    print()

    response = input(colorize("Continue? [y/N]: ", 'yellow')).strip().lower()
    if response != 'y':
        print_warning("Update cancelled")
        input("\nPress Enter to continue...")
        return

    print()
    success_count = 0
    fail_count = 0
    skipped_count = 0

    for tool_name, module_path in config.GO_TOOLS.items():
        # Skip if not installed
        if not check_command_exists(tool_name):
            skipped_count += 1
            continue

        print(f"Updating {tool_name}...", end=' ')
        try:
            result = subprocess.run(
                ['go', 'install', '-v', module_path],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print(colorize("✓", 'green'))
                success_count += 1
                logger.info(f"Updated {tool_name}")
            else:
                print(colorize("✗", 'red'))
                fail_count += 1
                logger.warning(f"Failed to update {tool_name}: {result.stderr}")

        except Exception as e:
            print(colorize("✗", 'red'))
            fail_count += 1
            logger.error(f"Error updating {tool_name}: {e}")

    print()
    print_info(f"Updated: {success_count} | Failed: {fail_count} | Skipped: {skipped_count}")
    print()
    input("Press Enter to continue...")


def update_selected_tools(logger):
    """Update selected Go tools using gum multi-select"""
    print_section("🎯 Select Tools to Update")

    # Check if gum is available
    if not check_command_exists('gum'):
        print()
        print_error("gum is not installed!")
        print_info("gum is required for interactive multi-select")
        print()
        print_info("Install gum with:")
        print("  go install github.com/charmbracelet/gum@latest")
        print()
        input("Press Enter to continue...")
        return

    tool_list = list(config.GO_TOOLS.keys())

    print_info(f"Available tools: {len(tool_list)}")
    print()
    print(colorize("TIP: Use SPACE to select, ENTER when done", 'yellow'))
    print()

    # Use gum for multi-select
    selected = gum_multi_select(
        tool_list,
        header="Select tools to update:"
    )

    if not selected:
        print()
        print_warning("No tools selected")
        input("\nPress Enter to continue...")
        return

    # Show selection
    print()
    print_section(f"Updating {len(selected)} Selected Tools")
    for tool in selected:
        print(colorize(f"  • {tool}", 'cyan'))
    print()

    # Confirm
    response = input(colorize("Proceed with update? [Y/n]: ", 'yellow')).strip().lower()
    if response == 'n':
        print_warning("Update cancelled")
        input("\nPress Enter to continue...")
        return

    print()
    success_count = 0
    fail_count = 0

    for tool_name in selected:
        module_path = config.GO_TOOLS[tool_name]
        print(f"Updating {tool_name}...", end=' ')

        try:
            result = subprocess.run(
                ['go', 'install', '-v', module_path],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print(colorize("✓", 'green'))
                success_count += 1
                logger.info(f"Updated {tool_name}")
            else:
                print(colorize("✗", 'red'))
                fail_count += 1
                logger.warning(f"Failed to update {tool_name}: {result.stderr}")

        except Exception as e:
            print(colorize("✗", 'red'))
            fail_count += 1
            logger.error(f"Error updating {tool_name}: {e}")

    print()
    print_info(f"Updated: {success_count} | Failed: {fail_count}")
    print()
    input("Press Enter to continue...")


# ============================================================================
# Wordlist Management
# ============================================================================

def wordlist_menu(logger):
    """Wordlist management menu"""
    while True:
        print_section("📚 WORDLIST MANAGEMENT")

        # Check if SecLists is installed
        seclists_path = os.path.expanduser("~/wordlists/SecLists")
        seclists_installed = os.path.isdir(seclists_path)

        print(colorize("1)", 'green') + " Install SecLists")
        if seclists_installed:
            print(colorize("   ✓ Already installed at ~/wordlists/SecLists", 'green'))
        else:
            print("   Comprehensive wordlist collection")
        print()

        print(colorize("2)", 'green') + " View Installed Wordlists")
        print("   Browse wordlist directory structure")
        print()

        print(colorize("3)", 'green') + " Update SecLists")
        if seclists_installed:
            print("   Pull latest updates from GitHub")
        else:
            print(colorize("   (Requires SecLists to be installed first)", 'yellow'))
        print()

        print(colorize("0)", 'red') + " Back to Main Menu")
        print()

        choice = input(colorize("Select option: ", 'yellow')).strip()

        if choice == '0':
            return
        elif choice == '1':
            install_seclists(logger)
        elif choice == '2':
            view_wordlists(logger)
        elif choice == '3':
            update_seclists(logger, seclists_installed)
        else:
            print_error("Invalid option. Please try again.")
            input("\nPress Enter to continue...")


def install_seclists(logger):
    """Install SecLists wordlist collection"""
    print_section("📥 Installing SecLists")

    wordlists_dir = os.path.expanduser("~/wordlists")
    seclists_path = os.path.join(wordlists_dir, "SecLists")

    # Check if already installed
    if os.path.isdir(seclists_path):
        print_warning("SecLists is already installed!")
        print_info(f"Location: {seclists_path}")
        print()
        response = input(colorize("Reinstall? This will delete and re-clone. [y/N]: ", 'yellow')).strip().lower()
        if response != 'y':
            print_warning("Installation cancelled")
            input("\nPress Enter to continue...")
            return

        # Remove existing
        print_info("Removing existing SecLists...")
        try:
            subprocess.run(['rm', '-rf', seclists_path], check=True)
        except Exception as e:
            print_error(f"Failed to remove existing SecLists: {e}")
            logger.error(f"Failed to remove SecLists: {e}")
            input("\nPress Enter to continue...")
            return

    # Create wordlists directory
    if not os.path.isdir(wordlists_dir):
        print_info(f"Creating {wordlists_dir}...")
        os.makedirs(wordlists_dir, exist_ok=True)

    # Clone SecLists
    print_info("Cloning SecLists from GitHub...")
    print_warning("This is a large repository (~500MB), it may take a few minutes...")
    print()

    try:
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', 'https://github.com/danielmiessler/SecLists.git', seclists_path],
            check=False
        )

        if result.returncode == 0:
            print()
            print_success("SecLists installed successfully!")
            print_info(f"Location: {seclists_path}")
            print()
            print_info("Popular wordlists:")
            print(f"  • Passwords: {seclists_path}/Passwords/")
            print(f"  • Usernames: {seclists_path}/Usernames/")
            print(f"  • Subdomains: {seclists_path}/Discovery/DNS/")
            print(f"  • Directories: {seclists_path}/Discovery/Web-Content/")
            print(f"  • Fuzzing: {seclists_path}/Fuzzing/")
            logger.info("SecLists installed successfully")
        else:
            print_error("Failed to clone SecLists repository")
            logger.error("SecLists installation failed")

    except Exception as e:
        print_error(f"Installation failed: {e}")
        logger.error(f"SecLists installation error: {e}", exc_info=True)

    print()
    input("Press Enter to continue...")


def view_wordlists(logger):
    """View installed wordlist directory structure"""
    print_section("📂 Installed Wordlists")

    wordlists_dir = os.path.expanduser("~/wordlists")

    if not os.path.isdir(wordlists_dir):
        print_warning("No wordlists directory found")
        print_info(f"Expected location: {wordlists_dir}")
        print()
        input("Press Enter to continue...")
        return

    seclists_path = os.path.join(wordlists_dir, "SecLists")

    if not os.path.isdir(seclists_path):
        print_warning("SecLists not found")
        print_info("Use option 1 to install SecLists")
        print()
        input("Press Enter to continue...")
        return

    # Show SecLists structure
    print(colorize(f"SecLists Location: {seclists_path}", 'cyan'))
    print()

    categories = [
        "Discovery",
        "Fuzzing",
        "IOCs",
        "Miscellaneous",
        "Passwords",
        "Pattern-Matching",
        "Payloads",
        "Usernames",
        "Web-Shells"
    ]

    for category in categories:
        category_path = os.path.join(seclists_path, category)
        if os.path.isdir(category_path):
            # Count files in category
            try:
                file_count = sum(1 for _ in Path(category_path).rglob('*') if _.is_file())
                print(colorize(f"  📁 {category}/", 'green') + f" ({file_count} files)")
            except Exception:
                print(colorize(f"  📁 {category}/", 'green'))

    print()
    print_info(f"Full path: {seclists_path}")
    print()
    input("Press Enter to continue...")


def update_seclists(logger, seclists_installed: bool):
    """Update SecLists from GitHub"""
    print_section("🔄 Updating SecLists")

    if not seclists_installed:
        print_warning("SecLists is not installed!")
        print_info("Use option 1 to install SecLists first")
        print()
        input("Press Enter to continue...")
        return

    seclists_path = os.path.expanduser("~/wordlists/SecLists")

    print_info("Pulling latest updates from GitHub...")
    print()

    try:
        # Run git pull
        result = subprocess.run(
            ['git', '-C', seclists_path, 'pull'],
            check=False
        )

        print()
        if result.returncode == 0:
            print_success("SecLists updated successfully!")
        else:
            print_warning("Update completed with issues")
            print_info("Try reinstalling if problems persist (option 1)")

        logger.info(f"SecLists update completed with exit code {result.returncode}")

    except Exception as e:
        print_error(f"Update failed: {e}")
        logger.error(f"SecLists update error: {e}", exc_info=True)

    print()
    input("Press Enter to continue...")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point"""
    # System checks
    check_root_discourage()

    if not check_apt():
        print_error("APT package manager not found!")
        print_error("This tool currently only supports Debian-based systems.")
        sys.exit(1)

    if not check_sudo():
        print_error("sudo not found! Please install sudo first.")
        sys.exit(1)

    # Setup logging
    logger = setup_logging()

    # Detect distribution
    distro_name, distro_type = detect_distro()
    logger.info(f"Detected distribution: {distro_name} (type: {distro_type})")

    # Check for fresh (optional)
    prompt_install_fresh()

    # Enter main menu loop
    try:
        main_menu_loop(distro_name, distro_type, logger)
    except KeyboardInterrupt:
        print()
        print()
        print_warning("Installation interrupted by user")
        logger.info("Installation interrupted by user (KeyboardInterrupt)")
        sys.exit(0)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
