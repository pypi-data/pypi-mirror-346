"""
Command-line interface for VLC Gesture Control
"""

import argparse
import sys
import platform
import os
from importlib.metadata import version

# Check Python version compatibility first
PYTHON_VERSION = tuple(map(int, platform.python_version_tuple()))
if PYTHON_VERSION >= (3, 13, 0):
    print(f"WARNING: VLC Gesture Control may not work correctly on Python {platform.python_version()}")
    print("This package is designed for Python 3.9-3.12 due to mediapipe compatibility.")
    print("If you encounter errors, please install Python 3.12 or earlier.\n")

# Setting this environment variable prevents the GPU module from asking for input
# when launched from the CLI with a specified mode
os.environ["VLC_GESTURE_DEVICE"] = "cpu"  # Default to CPU

# Define lazy importers for modules
cpu_main = None
gpu_main = None

def lazy_import_cpu():
    """Lazily import CPU module only when needed to avoid dependency errors"""
    global cpu_main
    if cpu_main is None:
        try:
            from .vlc_m_cpu import main as cpu_main_import
            cpu_main = cpu_main_import
        except ImportError as e:
            print(f"Error: CPU module import failed: {e}")
            return None
    return cpu_main

def lazy_import_gpu():
    """Lazily import GPU module only when needed to avoid dependency errors"""
    global gpu_main
    if gpu_main is None:
        try:
            from .vlc_m_gpu import main as gpu_main_import
            gpu_main = gpu_main_import
        except ImportError as e:
            print(f"Error: GPU module import failed: {e}")
            if "torch" in str(e):
                print("GPU acceleration requires additional dependencies.")
                print("Install them with: pip install vlc-gesture-control[gpu]")
            return None
    return gpu_main


def show_gesture_help():
    """Display detailed information about supported gestures"""
    print("\n=== VLC Gesture Control - Supported Gestures ===\n")
    print("| Gesture                       | Action                          |")
    print("|-------------------------------|----------------------------------|")
    print("| All five fingers up           | Play/Pause                       |")
    print("| Index finger only             | Volume Up                        |")
    print("| Thumb + Index finger          | Volume Down                      |")
    print("| Index + Middle fingers        | Forward 10s (Fast-forward when   |")
    print("|                               | repeated)                        |")
    print("| Thumb + Index + Middle        | Backward 10s (Fast-rewind when   |")
    print("|                               | repeated)                        |")
    print("| Index + Middle + Ring fingers | Toggle Subtitles                 |")
    print("| All fingers except thumb      | Change Audio Track               |")
    print("| Left hand thumb only          | Next Video                       |")
    print("| Right hand thumb only         | Previous Video                   |")
    print("\nNote: Make sure your palm is facing the camera for gestures to be recognized.")
    print("Press 'q' to quit the application while it's running.\n")
    sys.exit(0)


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description=(
            "Control VLC media player using hand gestures detected through your webcam."
        )
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"VLC Gesture Control {version('vlc-gesture-control')}",
    )

    parser.add_argument(
        "--help-gestures",
        action="store_true",
        help="Show detailed information about supported gestures",
    )

    parser.add_argument(
        "--mode",
        choices=["cpu", "gpu"],
        default="cpu",
        help="Processing mode: CPU (default) or GPU if supported",
    )

    parser.add_argument(
        "--camera", type=int, default=0, help="Camera index to use (default: 0)"
    )

    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode with additional logging"
    )
    
    parser.add_argument(
        "--setup-path",
        action="store_true",
        help="Launch the PATH setup utility to help find and add commands to PATH",
    )

    args = parser.parse_args()

    # Set the mode in environment variables to prevent interactive prompt
    if args.mode:
        os.environ["VLC_GESTURE_DEVICE"] = args.mode

    # Handle special commands first
    if args.help_gestures:
        show_gesture_help()
    
    if args.setup_path:
        try:
            from .setup_paths import main as setup_paths_main
            setup_paths_main()
            return
        except ImportError as e:
            print(f"Error: Setup paths utility not available: {e}")
            sys.exit(1)

    try:
        if args.mode == "cpu":
            # Lazy import CPU module only when needed
            cpu_runner = lazy_import_cpu()
            if cpu_runner is None:
                raise ImportError("CPU module not available")
            cpu_runner(camera_index=args.camera, debug=args.debug)
        else:  # GPU mode
            # Lazy import GPU module only when needed
            gpu_runner = lazy_import_gpu()
            if gpu_runner is None:
                print("Falling back to CPU mode due to missing GPU dependencies")
                cpu_runner = lazy_import_cpu()
                if cpu_runner is None:
                    raise ImportError("CPU module not available as fallback")
                cpu_runner(camera_index=args.camera, debug=args.debug)
            else:
                gpu_runner(camera_index=args.camera, debug=args.debug)
    except ImportError as e:
        if args.mode == "gpu":
            print(
                "Error: GPU dependencies not installed. Install with 'pip install"
                " vlc-gesture-control[gpu]'"
            )
        else:
            print(f"Error importing required modules: {e}")
            
        # Special handling for mediapipe on Python 3.13+
        if 'mediapipe' in str(e) and PYTHON_VERSION >= (3, 13, 0):
            print("\nERROR: Mediapipe is not compatible with Python 3.13+")
            print("This package requires Python 3.9-3.12.")
            print("Please install a compatible Python version to use this package.")
        
        # Show instructions for setting up PATH
        print("\nTIP: If commands are not found in your PATH, try:")
        print("python -m vlc_gesture_control.setup_paths")
        
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting VLC Gesture Control...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
