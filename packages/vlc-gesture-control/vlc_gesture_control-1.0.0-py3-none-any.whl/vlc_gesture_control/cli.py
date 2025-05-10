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

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description="Control VLC media player using hand gestures detected through your webcam."
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"VLC Gesture Control {version('vlc-gesture-control')}"
    )
    
    parser.add_argument(
        "--mode", 
        choices=["cpu", "gpu"], 
        default="cpu",
        help="Processing mode: CPU (default) or GPU if supported"
    )
    
    parser.add_argument(
        "--camera", 
        type=int, 
        default=0,
        help="Camera index to use (default: 0)"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug mode with additional logging"
    )
    
    args = parser.parse_args()
    
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
            print("Error: GPU dependencies not installed. Install with 'pip install vlc-gesture-control[gpu]'")
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