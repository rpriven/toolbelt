#!/usr/bin/env python3
"""
Djedi Toolbelt - Utility Functions
Provides distro detection, logging, and helper functions
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple


# ============================================================================
# Distro Detection
# ============================================================================

def detect_distro() -> Tuple[str, str]:
    """
    Detect the Linux distribution

    Returns:
        Tuple of (distro_name, distro_type)
        distro_type is one of: 'kali', 'debian', 'ubuntu', 'unknown'
    """
    distro_name = "Unknown"
    distro_type = "unknown"

    if not os.path.exists('/etc/os-release'):
        return (distro_name, distro_type)

    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read()

            # Extract PRETTY_NAME
            for line in content.split('\n'):
                if line.startswith('PRETTY_NAME='):
                    distro_name = line.split('=')[1].strip('"')
                    break

            # Determine distro type
            content_lower = content.lower()
            if 'kali' in content_lower:
                distro_type = 'kali'
            elif 'debian' in content_lower:
                distro_type = 'debian'
            elif 'ubuntu' in content_lower:
                distro_type = 'ubuntu'

    except Exception as e:
        logging.error(f"Error detecting distro: {e}")

    return (distro_name, distro_type)


def is_kali() -> bool:
    """Check if running on Kali Linux"""
    _, distro_type = detect_distro()
    return distro_type == 'kali'


def is_debian_based() -> bool:
    """Check if running on Debian-based system (Debian, Ubuntu, Kali)"""
    _, distro_type = detect_distro()
    return distro_type in ['kali', 'debian', 'ubuntu']


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup logging with both file and console output

    Args:
        log_file: Optional path to log file. Defaults to ~/toolbelt-install.log

    Returns:
        Configured logger instance
    """
    if log_file is None:
        log_file = os.path.expanduser("~/toolbelt-install.log")

    # Create logger
    logger = logging.getLogger('toolbelt')
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    logger.handlers.clear()

    # File handler (DEBUG level)
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler (INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log session start
    logger.info("=" * 60)
    logger.info(f"Toolbelt session started: {datetime.now()}")
    logger.info("=" * 60)

    return logger


# ============================================================================
# System Checks
# ============================================================================

def is_root() -> bool:
    """Check if running as root"""
    return os.geteuid() == 0


def check_root_discourage():
    """Warn user if running as root (we don't want root!)"""
    if is_root():
        print("\033[91m")  # Red
        print("=" * 60)
        print("WARNING: Running as root is NOT recommended!")
        print("=" * 60)
        print("\033[0m")  # Reset
        print()
        print("This script will use sudo for specific commands that need it.")
        print("Running the entire script as root can cause issues:")
        print("  • Scripts download to /root instead of your home directory")
        print("  • Files owned by root instead of your user")
        print("  • Potential security issues")
        print()
        response = input("Continue anyway? [y/N]: ").strip().lower()
        if response != 'y':
            print("Exiting. Please run without sudo/root.")
            sys.exit(0)


def check_command_exists(command: str) -> bool:
    """
    Check if a command exists in PATH

    Args:
        command: Command name to check

    Returns:
        True if command exists, False otherwise
    """
    try:
        result = subprocess.run(
            ['which', command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except Exception:
        return False


def check_apt() -> bool:
    """Check if apt package manager is available"""
    return check_command_exists('apt')


def check_sudo() -> bool:
    """Check if sudo is available"""
    return check_command_exists('sudo')


# ============================================================================
# Helper Functions
# ============================================================================

def run_command(
    cmd: List[str],
    use_sudo: bool = False,
    shell: bool = False,
    check: bool = True,
    logger: Optional[logging.Logger] = None
) -> subprocess.CompletedProcess:
    """
    Run a command with optional sudo

    Args:
        cmd: Command and arguments as list
        use_sudo: Prepend sudo if True
        shell: Run as shell command if True
        check: Raise exception on non-zero exit if True
        logger: Optional logger instance

    Returns:
        CompletedProcess instance
    """
    if use_sudo and not is_root():
        if isinstance(cmd, list):
            cmd = ['sudo'] + cmd
        else:
            cmd = f"sudo {cmd}"

    if logger:
        cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
        logger.debug(f"Running: {cmd_str}")

    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if logger:
            logger.error(f"Command failed: {e.cmd}")
            logger.error(f"Exit code: {e.returncode}")
            if e.stdout:
                logger.error(f"Stdout: {e.stdout}")
            if e.stderr:
                logger.error(f"Stderr: {e.stderr}")
        raise


def ensure_directory(path: str, use_sudo: bool = False) -> bool:
    """
    Ensure directory exists, create if necessary

    Args:
        path: Directory path
        use_sudo: Use sudo to create if True

    Returns:
        True if directory exists or was created successfully
    """
    expanded_path = os.path.expanduser(path)

    if os.path.isdir(expanded_path):
        return True

    try:
        if use_sudo:
            subprocess.run(['sudo', 'mkdir', '-p', expanded_path], check=True)
        else:
            os.makedirs(expanded_path, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {expanded_path}: {e}")
        return False


def get_home_dir() -> str:
    """
    Get the actual user's home directory (not /root even if running as root)

    Returns:
        Path to user's home directory
    """
    # If running as root, try to get the original user's home
    if is_root():
        sudo_user = os.environ.get('SUDO_USER')
        if sudo_user:
            return os.path.expanduser(f"~{sudo_user}")

    # Otherwise return normal home
    return os.path.expanduser("~")


def colorize(text: str, color: str) -> str:
    """
    Colorize text for terminal output

    Args:
        text: Text to colorize
        color: Color name (red, green, yellow, blue, magenta, cyan)

    Returns:
        Colorized text string
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }

    color_code = colors.get(color.lower(), colors['reset'])
    return f"{color_code}{text}{colors['reset']}"


# ============================================================================
# Display Functions
# ============================================================================

def print_banner():
    """Print the toolbelt banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🔧  DJEDI TOOLBELT  🔧                      ║
║                                                          ║
║         Comprehensive Security Tool Installer            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(colorize(banner, 'cyan'))
    print(colorize("                    v2.0.0", 'magenta'))
    print()


def print_section(title: str):
    """Print a section header"""
    print()
    print(colorize("=" * 60, 'cyan'))
    print(colorize(f"  {title}", 'white'))
    print(colorize("=" * 60, 'cyan'))
    print()


def print_success(message: str):
    """Print success message"""
    print(colorize(f"✓ {message}", 'green'))


def print_info(message: str):
    """Print info message"""
    print(colorize(f"• {message}", 'blue'))


def print_warning(message: str):
    """Print warning message"""
    print(colorize(f"⚠ {message}", 'yellow'))


def print_error(message: str):
    """Print error message"""
    print(colorize(f"✗ {message}", 'red'))
