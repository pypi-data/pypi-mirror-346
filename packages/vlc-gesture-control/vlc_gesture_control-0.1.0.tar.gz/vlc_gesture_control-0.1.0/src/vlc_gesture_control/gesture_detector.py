"""
Gesture detection module for VLC Gesture Control.
This module handles the detection and classification of hand gestures.
"""

import mediapipe as mp
import numpy as np
from .config import GESTURES, SPECIAL_GESTURES


class GestureDetector:
    def __init__(self, max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8, model_complexity=1):
        """
        Initialize the gesture detector with MediaPipe Hands.
        
        Args:
            max_num_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
            model_complexity: Model complexity (0, 1, or 2)
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=model_complexity
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.gesture_history = []
        self.gesture_history_size = 10
        self.required_consistency = 8
        
        # Hand motion tracking for swipe gestures
        self.prev_hand_center = None
        self.hand_positions = []  # Store recent hand positions
        self.max_positions = 10  # Number of positions to track
        self.swipe_threshold = 0.15  # Minimum x-distance to detect a swipe
        self.swipe_frames_threshold = 5  # Number of frames to complete a swipe
        self.swipe_cooldown = 0  # Cooldown timer to prevent multiple swipes
        self.swipe_ready = False  # Flag to indicate swipe gesture is prepared

    def process_frame(self, frame):
        """
        Process a frame and detect hands.
        
        Args:
            frame: RGB image frame
            
        Returns:
            MediaPipe hand processing results
        """
        return self.hands.process(frame)
    
    def draw_landmarks(self, frame, hand_landmarks):
        """
        Draw hand landmarks on the frame.
        
        Args:
            frame: BGR image frame
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            Frame with landmarks drawn
        """
        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame
    
    def fingers_up(self, hand_landmarks, hand_label):
        """
        Determine which fingers are up based on landmark positions and hand label.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            hand_label: 'Left' or 'Right'
            
        Returns:
            List of 5 binary values indicating thumb, index, middle, ring, pinky finger state (1=up, 0=down)
        """
        fingertips_ids = [
            self.mp_hands.HandLandmark.THUMB_TIP,
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_hands.HandLandmark.RING_FINGER_TIP,
            self.mp_hands.HandLandmark.PINKY_TIP
        ]

        finger_state = []
        landmarks = hand_landmarks.landmark

        # Different logic for thumb based on hand side
        if hand_label == 'Right':
            if landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x < landmarks[self.mp_hands.HandLandmark.THUMB_IP].x:
                finger_state.append(1)
            else:
                finger_state.append(0)
        else:
            if landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x > landmarks[self.mp_hands.HandLandmark.THUMB_IP].x:
                finger_state.append(1)
            else:
                finger_state.append(0)

        # For other fingers, check if fingertip is above finger pip
        for tip_id in fingertips_ids[1:]:
            pip_id = tip_id - 2  # Get pip joint for each fingertip
            if landmarks[tip_id].y < landmarks[pip_id].y:
                finger_state.append(1)
            else:
                finger_state.append(0)

        return finger_state
    
    def detect_gesture(self, finger_state, hand_label=None):
        """
        Recognize gesture based on finger positions and hand label.
        
        Args:
            finger_state: List of 5 binary values indicating finger states
            hand_label: 'Left' or 'Right' hand label (for direction-specific gestures)
            
        Returns:
            String representing the detected gesture or None if no gesture is detected
        """
        # Check thumb-only gestures for navigation (hand-specific)
        if finger_state == [1, 0, 0, 0, 0]:  # Thumb only
            if hand_label == 'Left':
                return "NEXT_VIDEO"  # Left hand thumb only (pointing right) = NEXT
            elif hand_label == 'Right':
                return "PREVIOUS_VIDEO"  # Right hand thumb only (pointing left) = PREVIOUS
        
        # Check for all five fingers up = PLAY/PAUSE
        if sum(finger_state) == 5:
            return "PLAY_PAUSE"
        
        # Check for specific finger patterns for other controls
        if finger_state == [0, 1, 0, 0, 0]:  # Index finger only
            return "VOLUME_UP"
        
        if finger_state == [1, 1, 0, 0, 0]:  # Thumb + index finger
            return "VOLUME_DOWN"
        
        if finger_state == [0, 1, 1, 0, 0]:  # Index + middle fingers
            return "FORWARD"
        
        if finger_state == [1, 1, 1, 0, 0]:  # Thumb + index + middle fingers
            return "BACKWARD"
        
        if finger_state == [0, 1, 1, 1, 0]:  # Index + middle + ring fingers
            return "TOGGLE_SUBTITLE"
        
        if finger_state == [0, 1, 1, 1, 1]:  # All fingers except thumb
            return "CHANGE_AUDIO"
        
        # No recognized gesture
        return None
    
    def is_swipe_gesture_ready(self, finger_state, hand_label):
        """
        Check if the hand is in the correct position to start tracking a swipe gesture.
        
        Note: This is kept for backward compatibility but is deprecated in the new control scheme
        which uses thumb-only gestures for navigation instead of swipes.
        
        Args:
            finger_state: List of 5 binary values indicating finger states
            hand_label: 'Left' or 'Right'
            
        Returns:
            Boolean indicating if the hand is in swipe-ready position
        """
        # Swipe gestures are no longer used in the new control scheme
        # but keeping this for backward compatibility
        return False
    
    def get_hand_center(self, hand_landmarks):
        """
        Calculate the center point of the hand.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            (x, y, z) coordinates of hand center
        """
        # Using the center of the palm as the hand center (average of wrist and middle_finger_mcp)
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        
        x = (wrist.x + middle_mcp.x) / 2
        y = (wrist.y + middle_mcp.y) / 2
        z = (wrist.z + middle_mcp.z) / 2
        
        return (x, y, z)
    
    def track_hand_movement(self, hand_landmarks, hand_label, finger_state):
        """
        Track hand movement for swipe gesture detection.
        
        Note: This is kept for backward compatibility but is deprecated in the new control scheme
        which uses thumb-only gestures for navigation instead of swipes.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            hand_label: 'Left' or 'Right'
            finger_state: List of 5 binary values indicating finger states
            
        Returns:
            None - swipe gestures are no longer used in the new control scheme
        """
        # Swipe gestures are deprecated in the new control scheme
        # returning None to prevent any swipe detection
        return None
    
    def is_palm_facing_camera(self, hand_landmarks, hand_label):
        """
        Determine if the palm is facing the camera using normal vector.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            hand_label: 'Left' or 'Right'
            
        Returns:
            Boolean indicating whether palm is facing the camera
        """
        landmarks = hand_landmarks.landmark

        # Get required landmark coordinates
        wrist = [landmarks[self.mp_hands.HandLandmark.WRIST].x,
                landmarks[self.mp_hands.HandLandmark.WRIST].y,
                landmarks[self.mp_hands.HandLandmark.WRIST].z]
        index_mcp = [landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
                    landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y,
                    landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].z]
        pinky_mcp = [landmarks[self.mp_hands.HandLandmark.PINKY_MCP].x,
                    landmarks[self.mp_hands.HandLandmark.PINKY_MCP].y,
                    landmarks[self.mp_hands.HandLandmark.PINKY_MCP].z]

        # Vectors from wrist to finger bases
        wrist_to_index = [index_mcp[i] - wrist[i] for i in range(3)]
        wrist_to_pinky = [pinky_mcp[i] - wrist[i] for i in range(3)]

        # Calculate palm normal vector via cross product
        palm_normal = [wrist_to_index[1]*wrist_to_pinky[2] - wrist_to_index[2]*wrist_to_pinky[1],
                    wrist_to_index[2]*wrist_to_pinky[0] - wrist_to_index[0]*wrist_to_pinky[2],
                    wrist_to_index[0]*wrist_to_pinky[1] - wrist_to_index[1]*wrist_to_pinky[0]]

        # Camera looks along negative z-axis
        camera_direction = [0, 0, -1]

        # Calculate dot product between palm normal and camera direction
        dot_product = sum(palm_normal[i] * camera_direction[i] for i in range(3))

        # Adjust for hand side
        if hand_label == 'Right':
            dot_product *= -1

        # Positive dot product means palm facing camera
        return dot_product > 0
    
    def is_palm_perpendicular(self, hand_landmarks, hand_label):
        """
        Determine if the palm is perpendicular to the camera (side view).
        This is used for distinguishing swipe gesture from play/pause.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            hand_label: 'Left' or 'Right'
            
        Returns:
            Boolean indicating whether palm is perpendicular to camera
        """
        # This is a simplified check - we can improve it with more accurate calculations
        landmarks = hand_landmarks.landmark
        
        # Get the thumb and pinky positions
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]
        
        # When palm is perpendicular, the thumb and pinky should be at similar z-depths
        z_difference = abs(thumb_tip.z - pinky_tip.z)
        
        # Threshold for considering palm perpendicular
        perpendicular_threshold = 0.05
        
        return z_difference < perpendicular_threshold
    
    def update_gesture_history(self, gesture):
        """
        Update gesture history with latest detection.
        
        Args:
            gesture: Detected gesture
            
        Returns:
            None
        """
        self.gesture_history.append(gesture)
        if len(self.gesture_history) > self.gesture_history_size:
            self.gesture_history.pop(0)
    
    def is_gesture_consistent(self, gesture):
        """
        Check if a gesture has been consistently detected.
        
        Args:
            gesture: Gesture to check
            
        Returns:
            Boolean indicating if gesture has been consistently detected
        """
        if gesture is None:
            return False
        return self.gesture_history.count(gesture) >= self.required_consistency
    
    def clear_history(self):
        """Clear the gesture history."""
        self.gesture_history.clear()
        self.hand_positions = []
        self.swipe_ready = False
    
    def set_parameters(self, history_size, required_consistency):
        """
        Set gesture detection parameters.
        
        Args:
            history_size: Size of the gesture history buffer
            required_consistency: Number of consistent detections required
        """
        self.gesture_history_size = history_size
        self.required_consistency = required_consistency
    
    def cleanup(self):
        """Release resources."""
        self.hands.close()


if __name__ == "__main__":
    # Simple test code
    import cv2
    
    detector = GestureDetector()
    cap = cv2.VideoCapture(0)
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Failed to capture frame")
                break
                
            frame = cv2.flip(frame, 1)  # Mirror
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = detector.process_frame(rgb_frame)
            
            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    hand_label = 'Right'
                    if results.multi_handedness:
                        hand_label = results.multi_handedness[idx].classification[0].label
                    
                    if not detector.is_palm_facing_camera(hand_landmarks, hand_label):
                        continue
                    
                    detector.draw_landmarks(frame, hand_landmarks)
                    finger_state = detector.fingers_up(hand_landmarks, hand_label)
                    
                    # Check for swipe gesture
                    swipe_gesture = detector.track_hand_movement(hand_landmarks, hand_label, finger_state)
                    if swipe_gesture:
                        cv2.putText(
                            frame,
                            f"Swipe: {swipe_gesture}",
                            (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            2
                        )
                    
                    # Check for regular gestures
                    gesture = detector.detect_gesture(finger_state, hand_label)
                    detector.update_gesture_history(gesture)
                    
                    if detector.is_gesture_consistent(gesture):
                        cv2.putText(
                            frame,
                            f"Gesture: {gesture}",
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2
                        )
            else:
                detector.clear_history()
            
            cv2.imshow('Gesture Detector Test', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()
        detector.cleanup() 