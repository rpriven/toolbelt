#!/usr/bin/env python3
"""
Djedi Toolbelt v2.0 - Security Tool Installer
Interactive package manager for pentesting and security research tools
"""

import sys
import os
from typing import Optional, List, Dict

# Import local modules
from utils import (
    setup_logging,
    detect_distro,
    check_root_discourage,
    check_apt,
    check_sudo,
    check_command_exists,
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

    print(colorize("1)", 'green') + " Install All Tools in Category")
    print(colorize("2)", 'green') + " Select Specific Tools (Coming Soon)")
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
            print_warning("Individual tool selection coming in next update!")
            input("\nPress Enter to continue...")
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
