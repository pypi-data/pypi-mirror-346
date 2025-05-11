"""
Tests for the gesture_detector module
"""

import unittest
from unittest.mock import MagicMock, patch

from vlc_gesture_control.gesture_detector import GestureDetector


class TestGestureDetector(unittest.TestCase):
    """Test cases for the GestureDetector class"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = GestureDetector()

    def test_detect_gesture_play_pause(self):
        """Test detection of play/pause gesture (all fingers up)"""
        finger_state = [1, 1, 1, 1, 1]  # All fingers up
        gesture = self.detector.detect_gesture(finger_state)
        self.assertEqual(gesture, "PLAY_PAUSE")

    def test_detect_gesture_volume_up(self):
        """Test detection of volume up gesture (index finger only)"""
        finger_state = [0, 1, 0, 0, 0]  # Index finger only
        gesture = self.detector.detect_gesture(finger_state)
        self.assertEqual(gesture, "VOLUME_UP")

    def test_detect_gesture_volume_down(self):
        """Test detection of volume down gesture (thumb + index finger)"""
        finger_state = [1, 1, 0, 0, 0]  # Thumb + index finger
        gesture = self.detector.detect_gesture(finger_state)
        self.assertEqual(gesture, "VOLUME_DOWN")

    def test_detect_gesture_forward(self):
        """Test detection of forward gesture (index + middle fingers)"""
        finger_state = [0, 1, 1, 0, 0]  # Index + middle fingers
        gesture = self.detector.detect_gesture(finger_state)
        self.assertEqual(gesture, "FORWARD")

    def test_detect_gesture_backward(self):
        """Test detection of backward gesture (thumb + index + middle fingers)"""
        finger_state = [1, 1, 1, 0, 0]  # Thumb + index + middle fingers
        gesture = self.detector.detect_gesture(finger_state)
        self.assertEqual(gesture, "BACKWARD")

    def test_detect_gesture_toggle_subtitle(self):
        """Test detection of toggle subtitle gesture (index + middle + ring fingers)"""
        finger_state = [0, 1, 1, 1, 0]  # Index + middle + ring fingers
        gesture = self.detector.detect_gesture(finger_state)
        self.assertEqual(gesture, "TOGGLE_SUBTITLE")

    def test_detect_gesture_change_audio(self):
        """Test detection of change audio track gesture (all fingers except thumb)"""
        finger_state = [0, 1, 1, 1, 1]  # All fingers except thumb
        gesture = self.detector.detect_gesture(finger_state)
        self.assertEqual(gesture, "CHANGE_AUDIO")

    def test_detect_gesture_next_video(self):
        """Test detection of next video gesture (left hand thumb only)"""
        finger_state = [1, 0, 0, 0, 0]  # Thumb only
        gesture = self.detector.detect_gesture(finger_state, hand_label="Left")
        self.assertEqual(gesture, "NEXT_VIDEO")

    def test_detect_gesture_previous_video(self):
        """Test detection of previous video gesture (right hand thumb only)"""
        finger_state = [1, 0, 0, 0, 0]  # Thumb only
        gesture = self.detector.detect_gesture(finger_state, hand_label="Right")
        self.assertEqual(gesture, "PREVIOUS_VIDEO")

    def test_detect_gesture_none(self):
        """Test detection of no recognized gesture"""
        finger_state = [0, 0, 1, 0, 1]  # Random unrecognized gesture
        gesture = self.detector.detect_gesture(finger_state)
        self.assertIsNone(gesture)


if __name__ == "__main__":
    unittest.main()
