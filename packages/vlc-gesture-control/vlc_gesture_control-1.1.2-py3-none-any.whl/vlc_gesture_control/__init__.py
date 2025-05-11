"""VLC Gesture Control - Control VLC media player using hand gestures."""

try:
    from importlib.metadata import version

    __version__ = version("vlc-gesture-control")
except ImportError:
    __version__ = "1.1.2"  # Fallback version


__author__ = "VLC Gesture Control Contributors"
__license__ = "MIT"
