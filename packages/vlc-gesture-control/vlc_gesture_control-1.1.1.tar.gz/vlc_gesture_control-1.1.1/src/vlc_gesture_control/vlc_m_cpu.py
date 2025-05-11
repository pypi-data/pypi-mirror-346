# works with both hands and all 5 control, changed controls to vlc only,has fps, fine tuned
# detect back of the hand and ignores it so you can safely adjust your hair and pick your nose without those gestures being detected.
# fast forward and backward implemented when the gesture is detected 4 times in a row
# kuods multitaskign is supported, is the movie is on one screen , and you are typing on whatsapp on another screen
# the gestures will only be detected on the screen where the movie is playing
# fast forward and backword  working [after multi tasking is implemented]
# thumb-only gestures for next/previous video navigation
# crashes when no vlc is fixed.

import sys
import logging
import time
from typing import List, Optional, Tuple, Dict, Any

# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Try to import required external libraries
try:
    import cv2
    import numpy as np
    import pyautogui
    import win32api
    import win32con
    import win32gui
    import mediapipe as mp
    
    REQUIRED_LIBS_AVAILABLE = True
except ImportError as e:
    REQUIRED_LIBS_AVAILABLE = False
    logger.error(f"Required library missing: {e}")
    missing_lib = str(e).split("'")[1] if "'" in str(e) else str(e)
    if "mediapipe" in missing_lib:
        logger.error(
            "Mediapipe is not available. This package requires Python 3.9-3.12. "
            "Python 3.13 is not yet supported by mediapipe."
        )
        print(f"ERROR: Python {sys.version.split()[0]} detected. This package requires Python 3.9-3.12.")
        print("Mediapipe does not yet support Python 3.13.")
        print("Please install a compatible Python version and try again.")
    
    print(f"Error: Required dependency '{missing_lib}' is missing.")
    print(f"Please install it with: pip install {missing_lib}")
    
    # Define placeholder for missing libraries to prevent immediate crashes
    if "mediapipe" in missing_lib:
        class MockMediapipe:
            """Mock for mediapipe when it's not available."""
            class Solutions:
                """Mock solutions module."""
                class Hands:
                    """Mock Hands class."""
                    def __init__(self, *args, **kwargs):
                        pass
                    def process(self, *args, **kwargs):
                        return None
                    def close(self):
                        pass
                    
                    class HandLandmark:
                        """Mock HandLandmark constants."""
                        WRIST = 0
                        THUMB_CMC = 1
                        THUMB_MCP = 2
                        THUMB_IP = 3
                        THUMB_TIP = 4
                        INDEX_FINGER_MCP = 5
                        INDEX_FINGER_PIP = 6
                        INDEX_FINGER_DIP = 7
                        INDEX_FINGER_TIP = 8
                        MIDDLE_FINGER_MCP = 9
                        MIDDLE_FINGER_PIP = 10
                        MIDDLE_FINGER_DIP = 11
                        MIDDLE_FINGER_TIP = 12
                        RING_FINGER_MCP = 13
                        RING_FINGER_PIP = 14
                        RING_FINGER_DIP = 15
                        RING_FINGER_TIP = 16
                        PINKY_MCP = 17
                        PINKY_PIP = 18
                        PINKY_DIP = 19
                        PINKY_TIP = 20
                    
                hands = Hands
                
                class DrawingUtils:
                    """Mock DrawingUtils class."""
                    def draw_landmarks(self, *args, **kwargs):
                        pass
                drawing_utils = DrawingUtils()
                
                HAND_CONNECTIONS = []
            solutions = Solutions()
        mp = MockMediapipe()


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
    def __init__(self, camera_index=0):
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
        self.frame_timestamps = []
        self.fps_display_interval = 2.0
        self.current_gesture = None
        self.gesture_repeat_count = 0
        self.camera_index = camera_index

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
                    # press control key globally
                    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                    time.sleep(0.05)  # small delay
                    # sends Right arrow to VLC
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

        # to get requird landmark coordinates
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

        # camera looks along the negative z-axis
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
        print("Gesture Control Running... Press 'q' to quit.\n")
        print("Gestures:")
        print("- Play/Pause: All fingers up (5 fingers)")
        print("- Volume Up: Index finger only")
        print("- Volume Down: Thumb + Index finger")
        print("- Forward: Index + Middle fingers")
        print("- Backward: Thumb + Index + Middle fingers")
        print("- Toggle Subtitle: Index + Middle + Ring fingers")
        print("- Change Audio Track: All fingers except thumb")
        print("- Next Video: Left hand thumb only (pointing right)")
        print("- Previous Video: Right hand thumb only (pointing left)\n")

        try:
            # Initialize MediaPipe hands
            self.hands = self.mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.8,
                min_tracking_confidence=0.8,
            )

            # Initialize camera
            self.initialize_camera()

            # Find VLC window
            self.vlc_window = find_vlc_window()

            # Failed camera read counter
            failed_reads = 0
            max_failed_reads = (
                10  # Maximum consecutive failed reads before reinitializing camera
            )

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
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)

                current_time = time.time()
                self.frame_timestamps.append(current_time)
                while (
                    self.frame_timestamps
                    and self.frame_timestamps[0]
                    < current_time - self.fps_display_interval
                ):
                    self.frame_timestamps.pop(0)
                average_fps = len(self.frame_timestamps) / self.fps_display_interval

                cv2.putText(
                    frame,
                    f"FPS: {average_fps:.2f}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

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
                        hand_label = None
                        if results.multi_handedness:
                            hand_label = (
                                results.multi_handedness[idx].classification[0].label
                            )
                        else:
                            hand_label = "Right"  # use right by defalt if not available

                        if not self.is_palm_facing_camera(hand_landmarks, hand_label):
                            continue  # to skip if back of hand is facing the camera

                        # draws hand landmarks on the frame
                        self.mp_draw.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                        )
                        finger_state = self.fingers_up(hand_landmarks, hand_label)

                        # Detect gesture considering the hand label
                        gesture = self.detect_gesture(finger_state, hand_label)

                        self.gesture_history.append(gesture)
                        if len(self.gesture_history) > self.gesture_history_size:
                            self.gesture_history.pop(0)
                        # to check for consistent gesture
                        if (
                            self.gesture_history.count(gesture)
                            >= self.required_gesture_consistency
                        ):
                            self.execute_gesture(gesture)
                else:
                    self.gesture_history.clear()

                cv2.imshow("Gesture Control", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Release resources and close windows."""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        if self.hands is not None:
            self.hands.close()
        print("Cleanup completed successfully.")


def main(camera_index=0, debug=False):
    """Entry point for the CPU version of VLC Gesture Control."""
    controller = GestureController(camera_index=camera_index)
    controller.run()


if __name__ == "__main__":
    main()
