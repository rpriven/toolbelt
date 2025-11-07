#!/usr/bin/env python3
"""
Djedi Toolbelt - Installation Functions
Handles installation of tools across all categories
"""

import os
import subprocess
import logging
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from utils import (
    run_command,
    ensure_directory,
    get_home_dir,
    check_command_exists,
    print_success,
    print_info,
    print_warning,
    print_error,
)
import config


# ============================================================================
# APT Tools Installation
# ============================================================================

def install_apt_tools(
    tools: Optional[List[str]] = None,
    distro_type: str = 'unknown',
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install tools via APT package manager

    Args:
        tools: List of package names (None for all)
        distro_type: Distro type for filtering
        logger: Logger instance

    Returns:
        True if successful
    """
    if tools is None:
        tools = config.get_apt_tools_for_distro(distro_type)

    if not tools:
        print_warning("No APT tools to install for this distribution")
        return True

    print_info(f"Installing {len(tools)} APT tools...")
    if logger:
        logger.info(f"Installing APT tools: {', '.join(tools)}")

    # Update apt cache
    try:
        print_info("Updating APT cache...")
        run_command(['apt', 'update'], use_sudo=True, logger=logger)
    except Exception as e:
        print_error(f"Failed to update APT cache: {e}")
        if logger:
            logger.error(f"APT update failed: {e}")
        return False

    # Check which tools are already installed
    tools_to_install = []
    for tool in tools:
        # Handle cases like docker.io where command name != package name
        check_name = tool.replace('.io', '').replace('-', '')
        if check_command_exists(check_name):
            print_success(f"{tool} already installed")
            if logger:
                logger.debug(f"{tool} already installed")
        else:
            tools_to_install.append(tool)

    if not tools_to_install:
        print_success("All APT tools already installed")
        return True

    # Install tools
    print_info(f"Installing {len(tools_to_install)} new tools...")
    try:
        cmd = ['apt', 'install', '-y'] + tools_to_install
        result = run_command(cmd, use_sudo=True, logger=logger)

        print_success(f"Installed {len(tools_to_install)} APT tools")
        if logger:
            logger.info(f"APT installation complete: {', '.join(tools_to_install)}")
        return True

    except Exception as e:
        print_error(f"Failed to install some APT tools: {e}")
        if logger:
            logger.error(f"APT installation failed: {e}")
        return False


# ============================================================================
# /opt Tools Installation
# ============================================================================

def install_opt_tool(
    tool_name: str,
    tool_config: Dict,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install a single /opt tool

    Args:
        tool_name: Name of the tool
        tool_config: Tool configuration dict
        logger: Logger instance

    Returns:
        True if successful
    """
    opt_path = f"/opt/{tool_name}"

    # Check if already installed
    if os.path.isdir(opt_path):
        print_success(f"{tool_name} already installed")
        if logger:
            logger.debug(f"{tool_name} already installed at {opt_path}")
        return True

    print_info(f"Installing {tool_name}...")
    if logger:
        logger.info(f"Installing /opt tool: {tool_name}")

    try:
        # Clone repository
        cmd = ['git', 'clone', tool_config['url'], opt_path]
        run_command(cmd, use_sudo=True, logger=logger)

        # Run post-install commands if specified
        if 'post_install' in tool_config:
            for post_cmd in tool_config['post_install']:
                run_command(post_cmd, use_sudo=True, shell=True, logger=logger)

        print_success(f"{tool_name} installed")
        if logger:
            logger.info(f"{tool_name} installation complete")
        return True

    except Exception as e:
        print_error(f"Failed to install {tool_name}: {e}")
        if logger:
            logger.error(f"Failed to install {tool_name}: {e}")
        return False


def install_opt_tools(
    tools: Optional[List[str]] = None,
    distro_type: str = 'unknown',
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install /opt tools

    Args:
        tools: List of tool names (None for all)
        distro_type: Distro type for filtering
        logger: Logger instance

    Returns:
        True if successful
    """
    all_tools = config.get_opt_tools_for_distro(distro_type)

    if tools is None:
        tools_to_install = all_tools
    else:
        tools_to_install = {k: v for k, v in all_tools.items() if k in tools}

    if not tools_to_install:
        print_warning("No /opt tools to install for this distribution")
        return True

    print_info(f"Installing {len(tools_to_install)} /opt tools...")

    # Ensure /opt exists
    ensure_directory("/opt", use_sudo=True)

    # Install each tool
    success_count = 0
    for tool_name, tool_config in tools_to_install.items():
        if install_opt_tool(tool_name, tool_config, logger):
            success_count += 1

    print_success(f"Installed {success_count}/{len(tools_to_install)} /opt tools")
    return success_count == len(tools_to_install)


# ============================================================================
# Python Tools Installation
# ============================================================================

def install_python_tools(
    tools: Optional[List[str]] = None,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install Python tools via pip3

    Args:
        tools: List of package names (None for all)
        logger: Logger instance

    Returns:
        True if successful
    """
    if tools is None:
        tools = config.PYTHON_TOOLS

    if not tools:
        print_warning("No Python tools to install")
        return True

    print_info(f"Installing {len(tools)} Python tools...")
    if logger:
        logger.info(f"Installing Python tools: {', '.join(tools)}")

    try:
        cmd = ['pip3', 'install', '--upgrade'] + tools
        run_command(cmd, logger=logger)

        print_success(f"Installed {len(tools)} Python tools")
        if logger:
            logger.info(f"Python tools installation complete")
        return True

    except Exception as e:
        print_error(f"Failed to install Python tools: {e}")
        if logger:
            logger.error(f"Python tools installation failed: {e}")
        return False


# ============================================================================
# Go Tools Installation
# ============================================================================

def install_go_tool(
    tool_name: str,
    tool_path: str,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install a single Go tool

    Args:
        tool_name: Name of the tool
        tool_path: Go module path
        logger: Logger instance

    Returns:
        True if successful
    """
    try:
        cmd = ['go', 'install', '-v', tool_path]
        run_command(cmd, logger=logger)
        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed to install {tool_name}: {e}")
        return False


def install_go_tools(
    tools: Optional[List[str]] = None,
    logger: Optional[logging.Logger] = None,
    parallel: bool = True
) -> bool:
    """
    Install Go tools

    Args:
        tools: List of tool names (None for all)
        logger: Logger instance
        parallel: Install in parallel if True

    Returns:
        True if successful
    """
    all_tools = config.GO_TOOLS

    if tools is None:
        tools_to_install = all_tools
    else:
        tools_to_install = {k: v for k, v in all_tools.items() if k in tools}

    if not tools_to_install:
        print_warning("No Go tools to install")
        return True

    print_info(f"Installing {len(tools_to_install)} Go tools...")
    if logger:
        logger.info(f"Installing Go tools: {', '.join(tools_to_install.keys())}")

    # Check if Go is installed
    if not check_command_exists('go'):
        print_error("Go is not installed! Install golang-go first.")
        return False

    success_count = 0

    if parallel:
        # Install in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(install_go_tool, name, path, logger): name
                for name, path in tools_to_install.items()
            }

            for future in as_completed(futures):
                tool_name = futures[future]
                try:
                    if future.result():
                        print_success(f"{tool_name} installed")
                        success_count += 1
                    else:
                        print_error(f"{tool_name} failed")
                except Exception as e:
                    print_error(f"{tool_name} failed: {e}")
    else:
        # Install sequentially
        for tool_name, tool_path in tools_to_install.items():
            if install_go_tool(tool_name, tool_path, logger):
                print_success(f"{tool_name} installed")
                success_count += 1
            else:
                print_error(f"{tool_name} failed")

    print_success(f"Installed {success_count}/{len(tools_to_install)} Go tools")
    return success_count == len(tools_to_install)


# ============================================================================
# Docker Tools Installation
# ============================================================================

def install_docker_tools(
    tools: Optional[List[str]] = None,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install Docker tools

    Args:
        tools: List of tool names (None for all)
        logger: Logger instance

    Returns:
        True if successful
    """
    all_tools = config.DOCKER_TOOLS

    if tools is None:
        tools_to_install = all_tools
    else:
        tools_to_install = {k: v for k, v in all_tools.items() if k in tools}

    if not tools_to_install:
        print_warning("No Docker tools to install")
        return True

    print_info(f"Installing {len(tools_to_install)} Docker tools...")
    if logger:
        logger.info(f"Installing Docker tools: {', '.join(tools_to_install.keys())}")

    # Check if Docker is installed
    if not check_command_exists('docker'):
        print_error("Docker is not installed! Install docker.io first.")
        return False

    success_count = 0

    for tool_name, tool_config in tools_to_install.items():
        try:
            # Pull Docker image
            cmd = ['docker', 'pull', tool_config['image']]
            run_command(cmd, logger=logger)

            # Add alias to shell config if specified
            if 'alias' in tool_config:
                home = get_home_dir()
                shell_configs = [
                    os.path.join(home, '.zshrc'),
                    os.path.join(home, '.bashrc')
                ]

                for config_file in shell_configs:
                    if os.path.exists(config_file):
                        with open(config_file, 'r') as f:
                            content = f.read()

                        if tool_name not in content:
                            with open(config_file, 'a') as f:
                                f.write(f"\n# {tool_name} alias (added by toolbelt)\n")
                                f.write(f"{tool_config['alias']}\n")
                            print_info(f"Added {tool_name} alias to {config_file}")

            print_success(f"{tool_name} installed")
            success_count += 1

        except Exception as e:
            print_error(f"Failed to install {tool_name}: {e}")
            if logger:
                logger.error(f"Failed to install {tool_name}: {e}")

    print_success(f"Installed {success_count}/{len(tools_to_install)} Docker tools")
    return success_count == len(tools_to_install)


# ============================================================================
# Useful Scripts Download
# ============================================================================

def download_useful_scripts(
    scripts: Optional[Dict[str, str]] = None,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Download useful scripts to ~/scripts

    Args:
        scripts: Dict of {filename: url} (None for all)
        logger: Logger instance

    Returns:
        True if successful
    """
    if scripts is None:
        scripts = config.USEFUL_SCRIPTS

    if not scripts:
        print_warning("No scripts to download")
        return True

    print_info(f"Downloading {len(scripts)} useful scripts...")
    if logger:
        logger.info(f"Downloading scripts: {', '.join(scripts.keys())}")

    # Create scripts/payloads directory in user's home (not /root!)
    home = get_home_dir()
    scripts_dir = os.path.join(home, 'scripts', 'payloads')
    ensure_directory(scripts_dir)

    success_count = 0

    for filename, url in scripts.items():
        try:
            output_path = os.path.join(scripts_dir, filename)

            # Skip if already exists
            if os.path.exists(output_path):
                print_success(f"{filename} already exists")
                success_count += 1
                continue

            # Download with wget
            cmd = ['wget', '-O', output_path, url]
            run_command(cmd, logger=logger)

            print_success(f"Downloaded {filename}")
            success_count += 1

        except Exception as e:
            print_error(f"Failed to download {filename}: {e}")
            if logger:
                logger.error(f"Failed to download {filename}: {e}")

    print_success(f"Downloaded {success_count}/{len(scripts)} scripts to {scripts_dir}")
    return success_count == len(scripts)
