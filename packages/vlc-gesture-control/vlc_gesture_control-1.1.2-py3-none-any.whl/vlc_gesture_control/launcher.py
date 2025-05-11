"""
Launcher script for VLC Gesture Control

This script helps create shortcuts that automatically handle environment
activation and launching the application.
"""

import os
import sys
import subprocess
import platform
import argparse
import site
import shutil
from pathlib import Path


def create_windows_shortcut(target_dir=None, mode="cpu"):
    """Create a Windows batch file shortcut for launching VLC Gesture Control."""
    if target_dir is None:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        target_dir = desktop
    
    target_dir = Path(target_dir)
    
    # Create the batch file
    batch_path = target_dir / "VLC Gesture Control.bat"
    
    # Get the Python executable path
    python_exe = sys.executable
    python_dir = os.path.dirname(python_exe)
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    # Get the script path
    scripts_dir = os.path.join(sys.prefix, "Scripts") if platform.system() == "Windows" else os.path.join(sys.prefix, "bin")
    vlc_script = os.path.join(scripts_dir, "vlc-gesture-control.exe" if platform.system() == "Windows" else "vlc-gesture-control")
    
    # If the script doesn't exist in the expected location, try to find it
    if not os.path.exists(vlc_script):
        # Try site-packages
        user_scripts = os.path.join(site.USER_BASE, "Scripts" if platform.system() == "Windows" else "bin")
        vlc_script = os.path.join(user_scripts, "vlc-gesture-control.exe" if platform.system() == "Windows" else "vlc-gesture-control")
    
    # Create content based on whether we're in a venv
    if in_venv:
        # If in venv, activate it first
        activate_script = os.path.join(python_dir, "activate.bat" if platform.system() == "Windows" else "activate")
        content = f"""@echo off
echo Starting VLC Gesture Control...
call "{activate_script}"
"{vlc_script}" --mode {mode}
"""
    else:
        # If not in venv, just run the script directly
        content = f"""@echo off
echo Starting VLC Gesture Control...
"{vlc_script}" --mode {mode}
"""
    
    # Write the batch file
    with open(batch_path, "w") as f:
        f.write(content)
    
    print(f"Created shortcut at: {batch_path}")
    return batch_path


def create_linux_shortcut(target_dir=None, mode="cpu"):
    """Create a Linux desktop entry for launching VLC Gesture Control."""
    if target_dir is None:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        target_dir = desktop
    
    target_dir = Path(target_dir)
    
    # Get the Python executable path
    python_exe = sys.executable
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    # Create a shell script that will launch the app
    script_path = target_dir / "vlc-gesture-control.sh"
    
    if in_venv:
        # If in venv, activate it first
        activate_script = os.path.join(os.path.dirname(python_exe), "activate")
        content = f"""#!/bin/bash
source "{activate_script}"
vlc-gesture-control --mode {mode}
"""
    else:
        # If not in venv, just run the script directly
        content = f"""#!/bin/bash
"{python_exe}" -m vlc_gesture_control --mode {mode}
"""
    
    # Write the shell script
    with open(script_path, "w") as f:
        f.write(content)
    
    # Make it executable
    os.chmod(script_path, 0o755)
    
    # Create desktop entry
    desktop_entry_path = target_dir / "VLC Gesture Control.desktop"
    icon_path = "/usr/share/icons/hicolor/scalable/apps/vlc.svg"  # Default VLC icon
    
    desktop_content = f"""[Desktop Entry]
Name=VLC Gesture Control
Comment=Control VLC with hand gestures
Exec={script_path}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Video;AudioVideo;Player;
"""
    
    with open(desktop_entry_path, "w") as f:
        f.write(desktop_content)
    
    print(f"Created shortcut at: {desktop_entry_path}")
    print(f"Created launcher script at: {script_path}")
    return desktop_entry_path


def create_macos_shortcut(target_dir=None, mode="cpu"):
    """Create a macOS application for launching VLC Gesture Control."""
    if target_dir is None:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        target_dir = desktop
    
    target_dir = Path(target_dir)
    
    # Get the Python executable path
    python_exe = sys.executable
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    # Create a shell script that will launch the app
    script_path = target_dir / "vlc-gesture-control.sh"
    
    if in_venv:
        # If in venv, activate it first
        activate_script = os.path.join(os.path.dirname(python_exe), "activate")
        content = f"""#!/bin/bash
source "{activate_script}"
vlc-gesture-control --mode {mode}
"""
    else:
        # If not in venv, just run the script directly
        content = f"""#!/bin/bash
"{python_exe}" -m vlc_gesture_control --mode {mode}
"""
    
    # Write the shell script
    with open(script_path, "w") as f:
        f.write(content)
    
    # Make it executable
    os.chmod(script_path, 0o755)
    
    print(f"Created launcher script at: {script_path}")
    print("To use this script, you can create an Automator application that runs this shell script.")
    return script_path


def main():
    """Main entry point for creating shortcuts."""
    parser = argparse.ArgumentParser(
        description="Create shortcuts for VLC Gesture Control"
    )
    
    parser.add_argument(
        "--target-dir",
        help="Directory to create shortcuts in (default: Desktop)",
        default=None,
    )
    
    parser.add_argument(
        "--mode",
        choices=["cpu", "gpu"],
        default="cpu",
        help="Processing mode to use (default: cpu)",
    )
    
    args = parser.parse_args()
    
    # Detect OS and create appropriate shortcut
    if platform.system() == "Windows":
        shortcut_path = create_windows_shortcut(args.target_dir, args.mode)
    elif platform.system() == "Linux":
        shortcut_path = create_linux_shortcut(args.target_dir, args.mode)
    elif platform.system() == "Darwin":  # macOS
        shortcut_path = create_macos_shortcut(args.target_dir, args.mode)
    else:
        print(f"Unsupported operating system: {platform.system()}")
        sys.exit(1)
    
    print("\nShortcut created successfully!")
    print(f"You can now launch VLC Gesture Control by running: {shortcut_path}")
    

if __name__ == "__main__":
    main() 