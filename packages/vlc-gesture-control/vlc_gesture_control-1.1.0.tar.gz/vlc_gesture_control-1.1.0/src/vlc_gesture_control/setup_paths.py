"""
Setup PATH for VLC Gesture Control

This script helps set up the PATH environment variable to include the Python Scripts
directory, making the VLC Gesture Control commands easily accessible from any command prompt.
"""

import os
import platform
import site
import sys
import subprocess
from pathlib import Path
from typing import Optional

def find_scripts_directory() -> Optional[str]:
    """Find the Python Scripts directory where executables are installed."""
    # Get the user site-packages directory
    user_site_packages = site.USER_SITE
    
    # If user_site_packages exists, use it to derive Scripts directory
    if user_site_packages:
        # Windows typically has Scripts, Unix-like systems typically have bin
        if platform.system() == "Windows":
            scripts_dir = Path(user_site_packages).parent / "Scripts"
        else:
            scripts_dir = Path(user_site_packages).parent / "bin"
        
        if scripts_dir.exists():
            return str(scripts_dir)
    
    # Fallback to standard paths
    if platform.system() == "Windows":
        # Check common Windows locations
        for path in [
            Path(sys.executable).parent / "Scripts",
            Path(sys.prefix) / "Scripts",
            # Check for Windows Store Python
            Path(os.environ.get("LOCALAPPDATA", "")) / "Packages" / "PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0" / "LocalCache" / "local-packages" / "Python312" / "Scripts",
        ]:
            if path.exists():
                return str(path)
    
    return None

def update_path_windows(scripts_dir: str) -> bool:
    """Update PATH on Windows using setx command."""
    try:
        # Check if the directory is already in PATH
        current_path = os.environ.get("PATH", "")
        if scripts_dir in current_path:
            print(f"\nDirectory already in PATH: {scripts_dir}")
            return True
        
        # Use setx to permanently add to PATH (user level)
        result = subprocess.run(
            ["setx", "PATH", f"{current_path};{scripts_dir}"],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print(f"\nSuccessfully added to PATH: {scripts_dir}")
            print("Please restart your command prompt for changes to take effect.")
            return True
        else:
            print(f"\nFailed to update PATH. Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"\nError updating PATH: {e}")
        return False

def create_batch_file(scripts_dir: str) -> bool:
    """Create a batch file that adds the directory to PATH temporarily."""
    bat_path = Path.cwd() / "add_to_path.bat"
    try:
        with open(bat_path, "w") as f:
            f.write(f"@echo off\n")
            f.write(f"echo Adding {scripts_dir} to PATH temporarily...\n")
            f.write(f"set PATH=%PATH%;{scripts_dir}\n")
            f.write(f"echo PATH updated! You can now use vlc-gesture-control commands.\n")
            f.write(f"cmd\n")
        
        print(f"\nCreated temporary PATH setup batch file: {bat_path}")
        print(f"Run this file to open a command prompt with updated PATH.")
        return True
    except Exception as e:
        print(f"\nError creating batch file: {e}")
        return False

def main() -> None:
    """Main function to set up PATH."""
    print("=== VLC Gesture Control - PATH Setup ===")
    
    # Find the Scripts directory
    scripts_dir = find_scripts_directory()
    
    if not scripts_dir:
        print("\nCould not find the Python Scripts directory.")
        print("Please ensure VLC Gesture Control is installed properly.")
        return
    
    print(f"\nFound Python Scripts directory: {scripts_dir}")
    print("This directory contains the VLC Gesture Control executables.")
    
    # Check if the commands are available
    executables = []
    for cmd in ["vlc-gesture-control", "vlc-gesture-control-cpu", "vlc-gesture-control-gpu"]:
        exe = cmd if platform.system() != "Windows" else f"{cmd}.exe"
        exe_path = Path(scripts_dir) / exe
        if exe_path.exists():
            executables.append(cmd)
    
    if not executables:
        print("\nCould not find VLC Gesture Control executables in the Scripts directory.")
        print("Please ensure VLC Gesture Control is installed properly.")
        return
    
    print(f"\nAvailable commands: {', '.join(executables)}")
    
    # Offer to set up PATH
    if platform.system() == "Windows":
        choice = input("\nWould you like to add this directory to your PATH? (y/n): ").strip().lower()
        if choice == 'y':
            success = update_path_windows(scripts_dir)
            if not success:
                print("\nCould not update PATH automatically.")
                create_batch_file(scripts_dir)
        else:
            create_batch_file(scripts_dir)
    else:
        print("\nOn Unix-like systems, add the following to your shell configuration file:")
        print(f"export PATH=\"$PATH:{scripts_dir}\"")
    
    print("\n=== Available Commands ===")
    print("vlc-gesture-control --help          Display general help")
    print("vlc-gesture-control --help-gestures Display gesture documentation")
    print("vlc-gesture-control --mode cpu      Run using CPU processing (default)")
    print("vlc-gesture-control --mode gpu      Run using GPU processing (if available)")
    print("vlc-gesture-control-cpu             Direct CPU mode shortcut")
    print("vlc-gesture-control-gpu             Direct GPU mode shortcut")
    
    print("\nIf commands are not found, use python -m vlc_gesture_control instead.")

if __name__ == "__main__":
    main() 