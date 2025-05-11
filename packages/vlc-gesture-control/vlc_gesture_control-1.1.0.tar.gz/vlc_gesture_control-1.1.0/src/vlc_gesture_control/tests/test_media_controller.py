"""
Tests for the media_controller module
"""

import unittest
from unittest.mock import MagicMock, patch

from vlc_gesture_control.media_controller import MediaController


class TestMediaController(unittest.TestCase):
    """Test cases for the MediaController class"""

    @patch("vlc_gesture_control.media_controller.win32gui")
    def setUp(self, mock_win32gui):
        """Set up test fixtures"""
        # Mock window finding to ensure tests run without a real VLC instance
        mock_win32gui.FindWindow.return_value = 12345  # Fake window handle
        mock_win32gui.IsWindow.return_value = True
        mock_win32gui.EnumWindows.return_value = None

        # Create a controller with a mocked VLC window
        self.controller = MediaController()
        self.controller.player_window = 12345

    def test_is_player_running_when_window_exists(self):
        """Test is_player_running returns True when window exists"""
        with patch(
            "vlc_gesture_control.media_controller.win32gui.IsWindow", return_value=True
        ):
            self.assertTrue(self.controller.is_player_running())

    def test_is_player_running_when_window_not_exists(self):
        """Test is_player_running returns False when window doesn't exist"""
        # Clear player_window to ensure is_player_running has to call FindWindow
        self.controller.player_window = None

        # Create a mock for find_player_window that returns False
        with patch.object(self.controller, "find_player_window", return_value=False):
            # When both IsWindow and FindWindow fail, is_player_running should return False
            with patch(
                "vlc_gesture_control.media_controller.win32gui.IsWindow",
                return_value=False,
            ):
                self.assertFalse(self.controller.is_player_running())

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_play_pause(self, mock_post_message):
        """Test execute_command for play/pause correctly sends the space key"""
        result = self.controller.execute_command("PLAY_PAUSE")
        self.assertEqual(result, "Play/Pause")
        # Check that PostMessage was called twice (key down and key up)
        self.assertEqual(mock_post_message.call_count, 2)

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_volume_up(self, mock_post_message):
        """Test execute_command for volume up correctly sends the up arrow key"""
        result = self.controller.execute_command("VOLUME_UP")
        self.assertEqual(result, "Volume Up")
        self.assertEqual(mock_post_message.call_count, 2)

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_volume_down(self, mock_post_message):
        """Test execute_command for volume down correctly sends the down arrow key"""
        result = self.controller.execute_command("VOLUME_DOWN")
        self.assertEqual(result, "Volume Down")
        self.assertEqual(mock_post_message.call_count, 2)

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_forward(self, mock_post_message):
        """Test execute_command for forward correctly sends the right arrow key"""
        result = self.controller.execute_command("FORWARD")
        self.assertEqual(result, "Forward 10 sec")
        self.assertEqual(mock_post_message.call_count, 2)

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_backward(self, mock_post_message):
        """Test execute_command for backward correctly sends the left arrow key"""
        result = self.controller.execute_command("BACKWARD")
        self.assertEqual(result, "Backward 10 sec")
        self.assertEqual(mock_post_message.call_count, 2)

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_toggle_subtitle(self, mock_post_message):
        """Test execute_command for toggle subtitle correctly sends the V key"""
        result = self.controller.execute_command("TOGGLE_SUBTITLE")
        self.assertEqual(result, "Toggle Subtitle")
        self.assertEqual(mock_post_message.call_count, 2)

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_change_audio(self, mock_post_message):
        """Test execute_command for change audio track correctly sends the B key"""
        result = self.controller.execute_command("CHANGE_AUDIO")
        self.assertEqual(result, "Change Audio Track")
        self.assertEqual(mock_post_message.call_count, 2)

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_next_video(self, mock_post_message):
        """Test execute_command for next video correctly sends the N key"""
        result = self.controller.execute_command("NEXT_VIDEO")
        self.assertEqual(result, "Next Video")
        self.assertEqual(mock_post_message.call_count, 2)

    @patch("vlc_gesture_control.media_controller.win32api.PostMessage")
    def test_execute_command_previous_video(self, mock_post_message):
        """Test execute_command for previous video correctly sends the P key"""
        result = self.controller.execute_command("PREVIOUS_VIDEO")
        self.assertEqual(result, "Previous Video")
        self.assertEqual(mock_post_message.call_count, 2)

    def test_execute_command_vlc_not_running(self):
        """Test execute_command when VLC is not running"""
        with patch.object(self.controller, "is_player_running", return_value=False):
            result = self.controller.execute_command("PLAY_PAUSE")
            self.assertEqual(result, "VLC not found")


if __name__ == "__main__":
    unittest.main()
