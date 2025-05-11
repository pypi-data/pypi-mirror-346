"""
Command-line interface for VLC Gesture Control
"""

import argparse
import sys
from importlib.metadata import version

# Import these at module level for easier mocking in tests
try:
    from .vlc_m_cpu import main as cpu_main
except ImportError:
    cpu_main = None

try:
    from .vlc_m_gpu import main as gpu_main
except ImportError:
    gpu_main = None


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

    args = parser.parse_args()

    # Handle special commands first
    if args.help_gestures:
        show_gesture_help()

    try:
        if args.mode == "cpu":
            if cpu_main is None:
                raise ImportError("CPU module not available")
            cpu_main(camera_index=args.camera, debug=args.debug)
        else:
            if gpu_main is None:
                raise ImportError("GPU dependencies not installed")
            gpu_main(camera_index=args.camera, debug=args.debug)
    except ImportError as e:
        if args.mode == "gpu":
            print(
                "Error: GPU dependencies not installed. Install with 'pip install"
                " vlc-gesture-control[gpu]'"
            )
        else:
            print(f"Error importing required modules: {e}")
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
