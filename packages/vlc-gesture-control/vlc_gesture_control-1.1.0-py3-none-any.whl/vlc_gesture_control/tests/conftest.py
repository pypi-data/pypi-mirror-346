"""
Shared test fixtures for VLC Gesture Control tests
"""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest


@pytest.fixture
def mock_video_frame():
    """Return a mock video frame for testing."""
    return np.zeros((480, 640, 3), dtype=np.uint8)


@pytest.fixture
def mock_hand_landmarks():
    """Return mock hand landmarks for testing."""
    # Create mock hand landmarks
    mock_landmarks = MagicMock()

    # Set up finger positions for all fingers up
    landmarks = []
    for i in range(21):  # MediaPipe uses 21 landmarks for a hand
        lm = MagicMock()
        # Set appropriate positions for each finger tip to be above its pip
        if i in [4, 8, 12, 16, 20]:  # Fingertips
            lm.y = 0.3
        else:
            lm.y = 0.5

        # Set x coordinates based on position
        lm.x = 0.5
        lm.z = 0.0

        landmarks.append(lm)

    # Set appropriate position for thumb
    landmarks[4].x = 0.3  # Thumb tip
    landmarks[3].x = 0.4  # Thumb IP

    mock_landmarks.landmark = landmarks
    return mock_landmarks


@pytest.fixture
def mock_vlc_window():
    """Return a mock VLC window handle and environment."""
    with (
        patch("win32gui.FindWindow", return_value=12345),
        patch("win32gui.IsWindow", return_value=True),
    ):
        yield 12345


@pytest.fixture
def mock_video_capture():
    """Return a mock video capture object."""
    with patch("cv2.VideoCapture") as mock_capture:
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_capture.return_value = mock_cap
        yield mock_cap


@pytest.fixture
def mock_mediapipe_hands():
    """Return a mock MediaPipe hands object."""
    with patch("mediapipe.solutions.hands.Hands") as mock_hands:
        mock_hands_instance = MagicMock()
        mock_hands.return_value = mock_hands_instance
        yield mock_hands_instance


@pytest.fixture(autouse=True)
def mock_pyautogui():
    """Mock pyautogui to prevent actual automation during tests."""
    with patch("pyautogui.keyDown") as mock_keydown, \
         patch("pyautogui.keyUp") as mock_keyup, \
         patch("pyautogui.press") as mock_press, \
         patch("pyautogui.typewrite") as mock_typewrite, \
         patch("pyautogui.screenshot") as mock_screenshot:
        
        mock_screenshot.return_value = np.zeros((1080, 1920, 3), dtype=np.uint8)
        
        yield {
            "keyDown": mock_keydown,
            "keyUp": mock_keyup,
            "press": mock_press,
            "typewrite": mock_typewrite,
            "screenshot": mock_screenshot
        }
