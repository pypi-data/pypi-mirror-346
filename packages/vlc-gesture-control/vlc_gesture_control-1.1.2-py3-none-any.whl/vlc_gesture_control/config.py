"""
Configuration settings for VLC Gesture Control application.
This file centralizes all configurable parameters to make the app more maintainable.
"""

# Hand detection settings
HAND_DETECTION = {
    "max_num_hands": 1,
    "min_detection_confidence": 0.8,
    "min_tracking_confidence": 0.8,
    "model_complexity": 1,
}

# Gesture recognition settings
GESTURE_RECOGNITION = {
    "gesture_history_size": 10,
    "required_gesture_consistency": 8,
    "action_interval": 1.0,
    "status_display_time": 2.0,
}

# Performance settings
PERFORMANCE = {
    "fps_display_interval": 2.0,
    "frame_skip_threshold": 10,  # Skip frames if FPS drops below this
    "camera_resolution": (640, 480),  # Width, Height
}

# Gesture mappings - UPDATED to new control scheme
GESTURES = {
    "PLAY_PAUSE": 5,  # All five fingers up
    "VOLUME_UP": [0, 1, 0, 0, 0],  # Index finger only
    "VOLUME_DOWN": [1, 1, 0, 0, 0],  # Thumb + index finger
    "FORWARD": [0, 1, 1, 0, 0],  # Index + middle fingers
    "BACKWARD": [1, 1, 1, 0, 0],  # Thumb + index + middle fingers
    "TOGGLE_SUBTITLE": [0, 1, 1, 1, 0],  # Index + middle + ring fingers
    "CHANGE_AUDIO": [0, 1, 1, 1, 1],  # All fingers except thumb
}

# Special finger combinations for thumb-only directional gestures
SPECIAL_GESTURES = {
    "NEXT_VIDEO_LEFT_HAND": [1, 0, 0, 0, 0],  # Left hand thumb only
    "PREVIOUS_VIDEO_RIGHT_HAND": [1, 0, 0, 0, 0],  # Right hand thumb only
}

# Swipe gesture settings - keeping for backward compatibility but no longer used
SWIPE_SETTINGS = {
    "threshold": 0.15,  # Min x-distance to detect a swipe
    "frames_threshold": 5,  # Frames to complete a swipe
    "cooldown": 10,  # Frames to wait after a swipe
    "movement_min": 0.05,  # Minimum movement to track
    "debug_visualization": True,  # Show debug visualization for swipes
}

# Fast-forward/rewind settings
FAST_CONTROL = {
    "required_repeat_count": 4  # Number of consecutive detections needed for fast forward/rewind
}

# VLC window settings
VLC_WINDOW = {"title_contains": "VLC media player"}

# Display settings
DISPLAY = {
    "window_name": "Gesture Control",
    "fps_position": (10, 60),
    "status_position": (10, 30),
    "text_color": (0, 255, 0),  # Green in BGR
    "text_thickness": 2,
    "font_scale": 0.7,
}

# For future extension to support other media players
SUPPORTED_PLAYERS = {
    "VLC": {
        "window_title": "VLC media player",
        "play_pause_key": 0x20,  # VK_SPACE
        "volume_up_key": 0x26,  # VK_UP
        "volume_down_key": 0x28,  # VK_DOWN
        "forward_key": 0x27,  # VK_RIGHT
        "backward_key": 0x25,  # VK_LEFT
        "modifier_key": 0x11,  # VK_CONTROL
        "audio_track_key": ord("B"),  # B key for audio track selection
        "subtitle_key": ord("V"),  # V key for subtitle toggling
        "next_video_key": ord("N"),  # N key for next video in playlist
        "prev_video_key": ord("P"),  # P key for previous video in playlist
    }
}
