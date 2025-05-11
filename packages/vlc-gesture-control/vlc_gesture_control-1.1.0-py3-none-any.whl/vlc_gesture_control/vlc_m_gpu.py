"""
VLC Gesture Control GPU Module.

This module contains the GPU-accelerated implementation of the VLC Gesture Controller.
It will gracefully handle the case when tensorflow is not available.
"""

# Standard imports that should always be available
import os
import sys
import time
import logging
from typing import Dict, List, Optional, Tuple, Union

# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define placeholder model whether tensorflow is available or not
class PlaceholderModel:
    """A placeholder model for when TensorFlow is not available."""

    def __init__(self):
        """Initialize an empty model."""
        logger.warning("Using placeholder model instead of TensorFlow model")

    def predict(self, *args, **kwargs):
        """Return a dummy prediction."""
        return [[0.9, 0.1, 0.0]]

# Try to import tensorflow, but continue if not available
try:
    import tensorflow as tf

    TENSORFLOW_AVAILABLE = True
    logger.info(f"TensorFlow {tf.__version__} loaded successfully")
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logger.warning("TensorFlow is not available, GPU controller will be limited")

# Import internal modules
from vlc_gesture_control.gesture_detector import GestureDetector
from vlc_gesture_control.media_controller import MediaController

import os
import time

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import torch
import win32api
import win32con
import win32gui


def get_device_choice():
    # Check if we're in a testing environment or automated environment
    if "PYTEST_CURRENT_TEST" in os.environ or "CI" in os.environ:
        # Default to CPU in test environments
        print("Test environment detected. Using CPU by default.")
        return "cpu"

    # Check if device choice is provided through environment variable
    if "VLC_GESTURE_DEVICE" in os.environ:
        choice = os.environ["VLC_GESTURE_DEVICE"].lower().strip()
        if choice in ["cpu", "gpu"]:
            return choice
        print(
            f"Invalid device choice in environment variable: {choice}. Falling back to"
            " CPU."
        )
        return "cpu"

    # Interactive mode - prompt user
    while True:
        try:
            choice = input("Choose processing device (cpu/gpu): ").lower().strip()
            if choice in ["cpu", "gpu"]:
                return choice
            print("Invalid choice. Please enter 'cpu' or 'gpu'")
        except EOFError:
            # Handle cases where input() is not available
            print("Cannot get interactive input. Defaulting to CPU.")
            return "cpu"


# Chnage device based on user choice
device_choice = get_device_choice()
if device_choice == "gpu" and torch.cuda.is_available():
    device = "cuda"
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
    cv2.setUseOptimized(True)
    mp_hands = mp.solutions.hands
    MEDIAPIPE_DEVICE = 0
else:
    if device_choice == "gpu":
        print("GPU requested but CUDA is not available. Falling back to CPU.")
    device = "cpu"
    print("Using CPU for processing.")
    cv2.ocl.setUseOpenCL(False)
    mp_hands = mp.solutions.hands
    MEDIAPIPE_DEVICE = -1  # cpu
    # change for multithreading
    # torch.set_num_threads(16)
    # torch.set_num_interop_threads(16)
    # print(f"PyTorch is set to use {torch.get_num_threads()} threads.")


def enum_windows_callback(hwnd, results):
    """Callback function to list all window titles."""
    results.append(win32gui.GetWindowText(hwnd))


def find_vlc_window():
    """Find the VLC Media Player window handle by searching for 'VLC media player' in the title."""
    all_windows = []
    win32gui.EnumWindows(enum_windows_callback, all_windows)
    for title in all_windows:
        if "VLC media player" in title:
            return win32gui.FindWindow(None, title)
    return None


class GestureController:
    """
    GestureController class for the VLC Gesture Control project.
    GPU-accelerated version for better performance on supported hardware.
    """

    def __init__(self, camera_index=0):
        """Initialize the GestureController."""
        self.media_controller = MediaController()
        self.gesture_detector = GestureDetector()

        # Load the TensorFlow model if available
        if TENSORFLOW_AVAILABLE:
            self.model_path = os.path.join(
                os.path.dirname(__file__), "models", "palm_model"
            )
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                logger.info("TensorFlow model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading TensorFlow model: {e}")
                self.model = PlaceholderModel()
        else:
            # Use placeholder model if TensorFlow is not available
            self.model = PlaceholderModel()

        self.mp_hands = mp.solutions.hands
        self.hands = None
        self.mp_draw = mp.solutions.drawing_utils
        self.last_action_time = 0
        self.action_interval = 1.0  # time interval between gesture recognitions
        self.status_message = ""
        self.status_display_time = 2.0  # duration to display the status message
        self.status_time = 0
        self.gesture_history = []
        #  gesture detection thresholds here [dont modify these unless you know what you are doing]
        #  i have fine tuned these values to work with the current setup
        self.gesture_history_size = 10  # size of the gesture history buffer
        self.required_gesture_consistency = 8  # required consistent detections
        self.cap = None
        self.frame_timestamps = []  # for FPS calculation
        self.fps_display_interval = 2.0
        self.current_gesture = None
        self.gesture_repeat_count = 0
        self.camera_index = camera_index

        # Hand movement tracking for swipe gestures
        self.hand_positions = []
        self.max_positions = 10
        self.swipe_threshold = 0.15  # minimum x-distance to detect a swipe
        self.swipe_frames_threshold = 5  # number of frames to complete a swipe
        self.swipe_cooldown = 0  # cooldown timer to prevent multiple swipes
        self.swipe_ready = False  # flag to indicate swipe gesture is prepared

        # vlc_window will be initialized in run()
        self.vlc_window = None

    def initialize_camera(self):
        """Initialize the webcam for capturing video frames."""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                raise RuntimeError(
                    f"Camera at index {self.camera_index} not available."
                )
        except Exception as e:
            print(f"Error initializing camera: {e}")
            raise

    def fingers_up(self, hand_landmarks, hand_label):
        """Determine which fingers are up based on landmark positions and hand label."""
        fingertips_ids = [
            self.mp_hands.HandLandmark.THUMB_TIP,
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_hands.HandLandmark.RING_FINGER_TIP,
            self.mp_hands.HandLandmark.PINKY_TIP,
        ]

        finger_state = []
        landmarks = hand_landmarks.landmark

        # different logic for left and right hand
        if hand_label == "Right":
            if (
                landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x
                < landmarks[self.mp_hands.HandLandmark.THUMB_IP].x
            ):
                finger_state.append(1)
            else:
                finger_state.append(0)
        else:
            if (
                landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x
                > landmarks[self.mp_hands.HandLandmark.THUMB_IP].x
            ):
                finger_state.append(1)
            else:
                finger_state.append(0)

        for tip_id in fingertips_ids[1:]:
            pip_id = tip_id - 2
            if landmarks[tip_id].y < landmarks[pip_id].y:
                finger_state.append(1)
            else:
                finger_state.append(0)

        return finger_state

    def detect_gesture(self, finger_state, hand_label):
        """Recognize gesture based on the number of fingers up and hand label."""
        # PLAY/PAUSE remains the same - all fingers up
        if sum(finger_state) == 5:
            return "PLAY_PAUSE"

        # --- NEXT/PREVIOUS VIDEO with thumb only ---
        # Left hand thumb only (pointing right) = NEXT
        if hand_label == "Left" and finger_state == [1, 0, 0, 0, 0]:
            return "NEXT_VIDEO"
        # Right hand thumb only (pointing left) = PREVIOUS
        if hand_label == "Right" and finger_state == [1, 0, 0, 0, 0]:
            return "PREVIOUS_VIDEO"

        # --- VOLUME CONTROLS ---
        # Index finger only = VOLUME UP
        if finger_state == [0, 1, 0, 0, 0]:
            return "VOLUME_UP"
        # Thumb and index finger = VOLUME DOWN
        if finger_state == [1, 1, 0, 0, 0]:
            return "VOLUME_DOWN"

        # --- FORWARD/BACKWARD ---
        # Index and middle fingers = FORWARD
        if finger_state == [0, 1, 1, 0, 0]:
            return "FORWARD"
        # Thumb, index, and middle fingers = BACKWARD
        if finger_state == [1, 1, 1, 0, 0]:
            return "BACKWARD"

        # --- SUBTITLE/AUDIO CONTROLS ---
        # Three fingers (index, middle, ring) = TOGGLE SUBTITLE
        if finger_state == [0, 1, 1, 1, 0]:
            return "TOGGLE_SUBTITLE"
        # Four fingers (all except thumb) = CHANGE AUDIO
        if finger_state == [0, 1, 1, 1, 1]:
            return "CHANGE_AUDIO"

        # No recognized gesture
        return None

    def is_swipe_gesture_ready(self, finger_state):
        """Check if the hand is in the correct position to start tracking a swipe gesture."""
        # We define a swipe-ready position as all fingers up (5)
        return sum(finger_state) == 5

    def get_hand_center(self, hand_landmarks):
        """Calculate the center point of the hand."""
        # Using the center of the palm as the hand center (average of wrist and middle_finger_mcp)
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        middle_mcp = hand_landmarks.landmark[
            self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP
        ]

        x = (wrist.x + middle_mcp.x) / 2
        y = (wrist.y + middle_mcp.y) / 2
        z = (wrist.z + middle_mcp.z) / 2

        return (x, y, z)

    def track_hand_movement(self, hand_landmarks, hand_label, finger_state):
        """Track hand movement for swipe gesture detection."""
        # Decrement cooldown timer if active
        if self.swipe_cooldown > 0:
            self.swipe_cooldown -= 1
            return None

        # Get current hand center
        hand_center = self.get_hand_center(hand_landmarks)

        # Check if we're in swipe-ready position
        is_ready = self.is_swipe_gesture_ready(finger_state)

        # If position changed, reset tracking
        if self.swipe_ready != is_ready:
            self.hand_positions = []
            self.swipe_ready = is_ready

        # If not in swipe position, no need to track
        if not self.swipe_ready:
            return None

        # Track hand position
        self.hand_positions.append((hand_center, hand_label))
        if len(self.hand_positions) > self.max_positions:
            self.hand_positions.pop(0)

        # Need at least a few frames to detect a swipe
        if len(self.hand_positions) < self.swipe_frames_threshold:
            return None

        # Calculate movement
        start_pos, start_label = self.hand_positions[0]
        end_pos, end_label = self.hand_positions[-1]

        # Check if hand label is consistent
        if start_label != end_label:
            self.hand_positions = []
            return None

        # Calculate horizontal movement (x-axis)
        x_movement = end_pos[0] - start_pos[0]

        # Detect swipe based on direction and hand
        if abs(x_movement) >= self.swipe_threshold:
            self.hand_positions = []  # Reset after detecting a swipe
            self.swipe_cooldown = 10  # Set cooldown to prevent multiple detections

            if hand_label == "Left":
                return "NEXT_VIDEO" if x_movement < 0 else "PREVIOUS_VIDEO"
            else:  # Right hand
                return "PREVIOUS_VIDEO" if x_movement < 0 else "NEXT_VIDEO"

        return None

    def execute_gesture(self, gesture):
        """Execute the action corresponding to the detected gesture."""
        current_time = time.time()
        if current_time - self.last_action_time >= self.action_interval:
            self.last_action_time = current_time

            # Check if VLC window is still valid
            if not self.vlc_window or not win32gui.IsWindow(self.vlc_window):
                # Try to find VLC window again
                self.vlc_window = find_vlc_window()
                if not self.vlc_window:
                    self.status_message = "VLC not found"
                    self.status_time = time.time()
                    return

            if gesture == self.current_gesture:
                self.gesture_repeat_count += 1
            else:
                self.gesture_repeat_count = 1
                self.current_gesture = gesture

            if gesture == "PLAY_PAUSE":
                win32api.PostMessage(
                    self.vlc_window, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0
                )
                win32api.PostMessage(
                    self.vlc_window, win32con.WM_KEYUP, win32con.VK_SPACE, 0
                )
                self.status_message = "Play/Pause"

            elif gesture == "VOLUME_UP":
                win32api.PostMessage(
                    self.vlc_window, win32con.WM_KEYDOWN, win32con.VK_UP, 0
                )
                win32api.PostMessage(
                    self.vlc_window, win32con.WM_KEYUP, win32con.VK_UP, 0
                )
                self.status_message = "Volume Up"

            elif gesture == "VOLUME_DOWN":
                win32api.PostMessage(
                    self.vlc_window, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0
                )
                win32api.PostMessage(
                    self.vlc_window, win32con.WM_KEYUP, win32con.VK_DOWN, 0
                )
                self.status_message = "Volume Down"

            elif gesture == "FORWARD":
                if self.gesture_repeat_count >= 4:
                    # press Control key globally
                    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                    time.sleep(0.05)  # small delay
                    # send Right arrow to VLC
                    win32api.PostMessage(
                        self.vlc_window, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0
                    )
                    win32api.PostMessage(
                        self.vlc_window, win32con.WM_KEYUP, win32con.VK_RIGHT, 0
                    )
                    time.sleep(0.05)
                    # release Control key
                    win32api.keybd_event(
                        win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0
                    )
                    self.status_message = "Fast Forward"
                else:
                    win32api.PostMessage(
                        self.vlc_window, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0
                    )
                    win32api.PostMessage(
                        self.vlc_window, win32con.WM_KEYUP, win32con.VK_RIGHT, 0
                    )
                    self.status_message = "Forward 10 sec"

            elif gesture == "BACKWARD":
                if self.gesture_repeat_count >= 4:
                    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                    time.sleep(0.05)
                    win32api.PostMessage(
                        self.vlc_window, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0
                    )
                    win32api.PostMessage(
                        self.vlc_window, win32con.WM_KEYUP, win32con.VK_LEFT, 0
                    )
                    time.sleep(0.05)
                    win32api.keybd_event(
                        win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0
                    )
                    self.status_message = "Fast Backward"
                else:
                    win32api.PostMessage(
                        self.vlc_window, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0
                    )
                    win32api.PostMessage(
                        self.vlc_window, win32con.WM_KEYUP, win32con.VK_LEFT, 0
                    )
                    self.status_message = "Backward 10 sec"

            elif gesture == "CHANGE_AUDIO":
                # Send 'B' key for cycling through audio tracks
                win32api.PostMessage(self.vlc_window, win32con.WM_KEYDOWN, ord("B"), 0)
                win32api.PostMessage(self.vlc_window, win32con.WM_KEYUP, ord("B"), 0)
                self.status_message = "Change Audio Track"

            elif gesture == "TOGGLE_SUBTITLE":
                # Send 'V' key for toggling subtitles
                win32api.PostMessage(self.vlc_window, win32con.WM_KEYDOWN, ord("V"), 0)
                win32api.PostMessage(self.vlc_window, win32con.WM_KEYUP, ord("V"), 0)
                self.status_message = "Toggle Subtitle"

            elif gesture == "NEXT_VIDEO":
                # Send 'N' key for next video in playlist
                win32api.PostMessage(self.vlc_window, win32con.WM_KEYDOWN, ord("N"), 0)
                win32api.PostMessage(self.vlc_window, win32con.WM_KEYUP, ord("N"), 0)
                self.status_message = "Next Video"

            elif gesture == "PREVIOUS_VIDEO":
                # Send 'P' key for previous video in playlist
                win32api.PostMessage(self.vlc_window, win32con.WM_KEYDOWN, ord("P"), 0)
                win32api.PostMessage(self.vlc_window, win32con.WM_KEYUP, ord("P"), 0)
                self.status_message = "Previous Video"

            else:
                self.gesture_repeat_count = 0
                self.current_gesture = None
                return

            self.status_time = time.time()

    def is_palm_facing_camera(self, hand_landmarks, hand_label):
        """Determine if the palm is facing the camera using the palm normal vector."""
        landmarks = hand_landmarks.landmark

        # to get required landmark coordinates
        wrist = [
            landmarks[self.mp_hands.HandLandmark.WRIST].x,
            landmarks[self.mp_hands.HandLandmark.WRIST].y,
            landmarks[self.mp_hands.HandLandmark.WRIST].z,
        ]
        index_mcp = [
            landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
            landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y,
            landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].z,
        ]
        pinky_mcp = [
            landmarks[self.mp_hands.HandLandmark.PINKY_MCP].x,
            landmarks[self.mp_hands.HandLandmark.PINKY_MCP].y,
            landmarks[self.mp_hands.HandLandmark.PINKY_MCP].z,
        ]

        wrist_to_index = [index_mcp[i] - wrist[i] for i in range(3)]
        wrist_to_pinky = [pinky_mcp[i] - wrist[i] for i in range(3)]

        # to calculate palm normal vector via cross product
        palm_normal = [
            wrist_to_index[1] * wrist_to_pinky[2]
            - wrist_to_index[2] * wrist_to_pinky[1],
            wrist_to_index[2] * wrist_to_pinky[0]
            - wrist_to_index[0] * wrist_to_pinky[2],
            wrist_to_index[0] * wrist_to_pinky[1]
            - wrist_to_index[1] * wrist_to_pinky[0],
        ]

        #  camera looks along the negative z-axis
        camera_direction = [0, 0, -1]

        # calculate dot product between palm normal and camera direction
        dot_product = sum(palm_normal[i] * camera_direction[i] for i in range(3))

        if hand_label == "Right":
            dot_product *= -1

        if dot_product > 0:
            return True  # front side is facing the camera
        else:
            return False  # back side of the hand is facing the camera

    def run(self):
        """Start the gesture control loop."""
        print(f"Gesture Control Running on {device.upper()}... Press 'q' to quit.\n")
        print("Gestures:")
        print("- Play/Pause: All five fingers up")
        print("- Volume Up: Index finger only")
        print("- Volume Down: Thumb + index finger")
        print("- Forward: Index + middle fingers")
        print("- Backward: Thumb + index + middle fingers")
        print("- Toggle Subtitle: Index + middle + ring fingers")
        print("- Change Audio Track: All fingers except thumb")
        print("- Next Video: Left hand thumb only (pointing right)")
        print("- Previous Video: Right hand thumb only (pointing left)\n")

        try:
            # Initialize MediaPipe hands
            self.hands = self.mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.8,
                min_tracking_confidence=0.8,
                model_complexity=1,
                static_image_mode=False,
            )

            # Initialize camera
            self.initialize_camera()

            # Find VLC window
            self.vlc_window = find_vlc_window()
            if not self.vlc_window:
                all_windows = []
                win32gui.EnumWindows(enum_windows_callback, all_windows)
                print("Available windows:")
                for title in all_windows:
                    print(f"- {title}")
                print(
                    "VLC media player not found. Will continue and wait for VLC to"
                    " open."
                )

            # Failed camera read counter
            failed_reads = 0
            max_failed_reads = (
                10  # Maximum consecutive failed reads before reinitializing camera
            )

            # to create window before the loop
            cv2.namedWindow("Gesture Control", cv2.WINDOW_NORMAL)

            while True:
                success, frame = self.cap.read()
                if not success:
                    failed_reads += 1
                    print(
                        f"Failed to capture frame ({failed_reads}/{max_failed_reads})"
                    )

                    if failed_reads >= max_failed_reads:
                        print("Camera disconnected. Attempting to reinitialize...")
                        self.cap.release()
                        time.sleep(1)  # Wait a bit before retrying
                        self.initialize_camera()
                        failed_reads = 0

                    time.sleep(0.1)  # Prevent tight loop on failure
                    continue
                else:
                    failed_reads = 0  # Reset counter on successful read

                frame = cv2.flip(frame, 1)  # mirror the frame

                if device == "cuda":
                    try:
                        # Convert to RGB and process on GPU
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        with torch.cuda.amp.autocast():
                            # Move data to GPU, process, and move back to CPU
                            rgb_tensor = torch.from_numpy(rgb_frame).float().cuda()
                            rgb_tensor = rgb_tensor / 255.0
                            # Move back to CPU and convert to correct format for MediaPipe
                            rgb_frame = (rgb_tensor.cpu().numpy() * 255).astype(
                                np.uint8
                            )
                    except Exception as e:
                        print(f"GPU processing error, falling back to CPU: {e}")
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                else:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process with MediaPipe
                results = self.hands.process(rgb_frame)

                current_time = time.time()
                self.frame_timestamps.append(current_time)
                # Remove timestamps older than fps_display_interval
                while (
                    self.frame_timestamps
                    and self.frame_timestamps[0]
                    < current_time - self.fps_display_interval
                ):
                    self.frame_timestamps.pop(0)
                average_fps = len(self.frame_timestamps) / self.fps_display_interval
                # Display FPS on the video feed
                cv2.putText(
                    frame,
                    f"FPS: {average_fps:.2f}",
                    (10, 60),  # Position on the frame (adjust as needed)
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,  # Font scale
                    (0, 255, 0),  # Color (B, G, R)
                    2,  # Thickness
                )

                #  message status
                if time.time() - self.status_time < self.status_display_time:
                    cv2.putText(
                        frame,
                        self.status_message,
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )

                if results.multi_hand_landmarks:
                    for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        # Get hand label
                        hand_label = None
                        if results.multi_handedness:
                            hand_label = (
                                results.multi_handedness[idx].classification[0].label
                            )
                        else:
                            hand_label = "Right"  # Default to right if not available

                        if not self.is_palm_facing_camera(hand_landmarks, hand_label):
                            continue  # Skip if back of hand is facing the camera

                        # Draw hand landmarks on the frame
                        self.mp_draw.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                        )
                        finger_state = self.fingers_up(hand_landmarks, hand_label)

                        # Check for standard gestures
                        gesture = self.detect_gesture(finger_state, hand_label)
                        self.gesture_history.append(gesture)
                        if len(self.gesture_history) > self.gesture_history_size:
                            self.gesture_history.pop(0)
                        # Check for consistent gesture
                        if (
                            self.gesture_history.count(gesture)
                            >= self.required_gesture_consistency
                        ):
                            self.execute_gesture(gesture)
                else:
                    self.gesture_history.clear()
                    self.hand_positions = []  # Clear hand tracking

                try:
                    cv2.imshow("Gesture Control", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        break
                except cv2.error as e:
                    print(f"Display error: {e}")
                    print("Continuing without display...")
                    # Check for quit without display
                    if win32api.GetAsyncKeyState(ord("Q")) & 0x8000:
                        break

        except Exception as e:
            print(f"Runtime error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Release resources and close windows."""
        try:
            if self.cap is not None:
                self.cap.release()
        except Exception as e:
            print(f"Error releasing camera: {e}")

        try:
            cv2.destroyAllWindows()
        except cv2.error as e:
            print(f"Error closing windows: {e}")

        try:
            if self.hands is not None:
                self.hands.close()
        except Exception as e:
            print(f"Error closing MediaPipe: {e}")

        print("Cleanup completed.")


if __name__ == "__main__":
    GestureController().run()


def main(camera_index=0, debug=False):
    """Entry point for the GPU version of VLC Gesture Control."""
    controller = GestureController(camera_index=camera_index)
    controller.run()


if __name__ == "__main__":
    main()
