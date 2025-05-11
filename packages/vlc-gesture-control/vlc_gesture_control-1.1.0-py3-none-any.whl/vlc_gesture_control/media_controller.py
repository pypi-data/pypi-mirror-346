"""
Media Controller module for VLC Gesture Control.
This module handles the control of VLC media player through keyboard commands.
"""

import time

import win32api
import win32con
import win32gui

from .config import SUPPORTED_PLAYERS


def enum_windows_callback(hwnd, results):
    """Callback function to list all window titles."""
    if win32gui.IsWindowVisible(hwnd):
        results.append((hwnd, win32gui.GetWindowText(hwnd)))


class MediaController:
    def __init__(self, player_type="VLC"):
        """
        Initialize the media controller.

        Args:
            player_type: Type of media player to control (default: "VLC")
        """
        self.player_type = player_type
        self.player_config = SUPPORTED_PLAYERS.get(player_type)
        if not self.player_config:
            raise ValueError(f"Unsupported player type: {player_type}")

        self.player_window = None
        self.find_player_window()  # Attempt to find window but don't raise exception if not found
        self.last_action_time = 0
        self.action_interval = 1.0
        self.current_gesture = None
        self.gesture_repeat_count = 0

    def find_player_window(self):
        """Find the media player window handle."""
        try:
            all_windows = []
            win32gui.EnumWindows(enum_windows_callback, all_windows)

            window_title = self.player_config["window_title"]
            for hwnd, title in all_windows:
                if window_title in title:
                    self.player_window = hwnd
                    return True

            # Window was not found
            self.player_window = None
            return False
        except Exception as e:
            print(f"Error finding player window: {e}")
            self.player_window = None
            return False

    def is_player_running(self):
        """Check if the media player is running."""
        try:
            if not self.player_window or not win32gui.IsWindow(self.player_window):
                # If we don't have a valid window handle, try to find one
                # Only return True if find_player_window actually finds a window
                return self.find_player_window() and self.player_window is not None
            return True
        except Exception as e:
            print(f"Error checking if player is running: {e}")
            return False

    def send_key(self, key_code, modifier=None):
        """
        Send a key command to the media player.

        Args:
            key_code: Virtual key code to send
            modifier: Optional modifier key (e.g., Ctrl, Alt)

        Returns:
            Boolean indicating success
        """
        try:
            if not self.is_player_running():
                print(f"{self.player_type} window not found")
                return False

            # Press modifier key if provided
            if modifier:
                win32api.keybd_event(modifier, 0, 0, 0)
                time.sleep(0.05)

            # Send key to player window
            win32api.PostMessage(self.player_window, win32con.WM_KEYDOWN, key_code, 0)
            win32api.PostMessage(self.player_window, win32con.WM_KEYUP, key_code, 0)

            # Release modifier key if provided
            if modifier:
                time.sleep(0.05)
                win32api.keybd_event(modifier, 0, win32con.KEYEVENTF_KEYUP, 0)

            return True
        except Exception as e:
            print(f"Error sending key to {self.player_type}: {e}")
            return False

    def execute_command(self, command, is_repeating=False):
        """
        Execute a media player command.

        Args:
            command: Command to execute (e.g., "PLAY_PAUSE", "VOLUME_UP")
            is_repeating: Whether this is a repeated command

        Returns:
            String describing the action taken or None if no action
        """
        try:
            current_time = time.time()
            if current_time - self.last_action_time < self.action_interval:
                return None

            self.last_action_time = current_time

            # Update gesture repetition tracking
            if command == self.current_gesture:
                self.gesture_repeat_count += 1
            else:
                self.gesture_repeat_count = 1
                self.current_gesture = command

            # Check if VLC is running first
            if not self.is_player_running():
                return "VLC not found"

            # Execute the appropriate command
            if command == "PLAY_PAUSE":
                self.send_key(self.player_config["play_pause_key"])
                return "Play/Pause"

            elif command == "VOLUME_UP":
                self.send_key(self.player_config["volume_up_key"])
                return "Volume Up"

            elif command == "VOLUME_DOWN":
                self.send_key(self.player_config["volume_down_key"])
                return "Volume Down"

            elif command == "FORWARD":
                if self.gesture_repeat_count >= 4:
                    # Fast Forward with modifier key
                    self.send_key(
                        self.player_config["forward_key"],
                        self.player_config["modifier_key"],
                    )
                    return "Fast Forward"
                else:
                    self.send_key(self.player_config["forward_key"])
                    return "Forward 10 sec"

            elif command == "BACKWARD":
                if self.gesture_repeat_count >= 4:
                    self.send_key(
                        self.player_config["backward_key"],
                        self.player_config["modifier_key"],
                    )
                    return "Fast Backward"
                else:
                    self.send_key(self.player_config["backward_key"])
                    return "Backward 10 sec"

            elif command == "CHANGE_AUDIO":
                self.send_key(self.player_config["audio_track_key"])
                return "Change Audio Track"

            elif command == "TOGGLE_SUBTITLE":
                self.send_key(self.player_config["subtitle_key"])
                return "Toggle Subtitle"

            elif command == "NEXT_VIDEO":
                self.send_key(self.player_config["next_video_key"])
                return "Next Video"

            elif command == "PREVIOUS_VIDEO":
                self.send_key(self.player_config["prev_video_key"])
                return "Previous Video"

            else:
                return None
        except Exception as e:
            print(f"Error executing command {command}: {e}")
            return None

    def next_video(self):
        """Go to the next video in the playlist (N key in VLC)."""
        if self.is_player_running():
            self.send_key(self.player_config["next_video_key"])
            return "Next Video"
        return None

    def previous_video(self):
        """Go to the previous video in the playlist (P key in VLC)."""
        if self.is_player_running():
            self.send_key(self.player_config["prev_video_key"])
            return "Previous Video"
        return None

    def screenshot(self):
        """Take a screenshot in VLC (Shift+S)."""
        if self.is_player_running():
            win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
            time.sleep(0.05)
            win32api.PostMessage(self.player_window, win32con.WM_KEYDOWN, ord("S"), 0)
            win32api.PostMessage(self.player_window, win32con.WM_KEYUP, ord("S"), 0)
            time.sleep(0.05)
            win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "Screenshot Taken"
        return None

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.is_player_running():
            self.send_key(ord("F"))
            return "Fullscreen Toggled"
        return None

    def list_active_windows(self):
        """List all active windows for debugging."""
        try:
            all_windows = []
            win32gui.EnumWindows(enum_windows_callback, all_windows)
            return [title for _, title in all_windows]
        except Exception as e:
            print(f"Error listing active windows: {e}")
            return []


if __name__ == "__main__":
    # Simple test code
    controller = MediaController()

    print("Media Controller Test")
    print("--------------------")
    print("1. Play/Pause")
    print("2. Volume Up")
    print("3. Volume Down")
    print("4. Forward")
    print("5. Backward")
    print("6. Change Audio Track")
    print("7. Toggle Subtitle")
    print("8. Screenshot")
    print("9. Toggle Fullscreen")
    print("n. Next Video")
    print("p. Previous Video")
    print("0. Exit")

    while True:
        choice = input("\nEnter choice (0-9, n, p): ")

        if choice == "1":
            result = controller.execute_command("PLAY_PAUSE")
            print(f"Result: {result}")
        elif choice == "2":
            result = controller.execute_command("VOLUME_UP")
            print(f"Result: {result}")
        elif choice == "3":
            result = controller.execute_command("VOLUME_DOWN")
            print(f"Result: {result}")
        elif choice == "4":
            result = controller.execute_command("FORWARD")
            print(f"Result: {result}")
        elif choice == "5":
            result = controller.execute_command("BACKWARD")
            print(f"Result: {result}")
        elif choice == "6":
            result = controller.execute_command("CHANGE_AUDIO")
            print(f"Result: {result}")
        elif choice == "7":
            result = controller.execute_command("TOGGLE_SUBTITLE")
            print(f"Result: {result}")
        elif choice == "8":
            result = controller.screenshot()
            print(f"Result: {result}")
        elif choice == "9":
            result = controller.toggle_fullscreen()
            print(f"Result: {result}")
        elif choice.lower() == "n":
            result = controller.next_video()
            print(f"Result: {result}")
        elif choice.lower() == "p":
            result = controller.previous_video()
            print(f"Result: {result}")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")
