"""
Professional Real-Time Finger Counting Application
with Voice Feedback and Advanced Gesture Recognition

Features:
- Real-time hand detection and finger counting (0-5)
- Text-to-speech voice announcements
- Visual statistics dashboard
- Gesture recognition (peace sign, fist, open palm, etc.)
- Support for both hands with proper orientation detection
"""

import cv2
import mediapipe as mp
import pyttsx3
import time
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict
import threading


class FingerCounter:
    """Main application class for finger counting with voice feedback"""
    
    # Hand landmarks indices (MediaPipe)
    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_MCP = 5
    INDEX_PIP = 6
    INDEX_DIP = 7
    INDEX_TIP = 8
    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12
    RING_MCP = 13
    RING_PIP = 14
    RING_DIP = 15
    RING_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20
    
    def __init__(self, camera_id: int = 0):
        """Initialize the finger counter application
        
        Args:
            camera_id: Webcam device ID (default: 0)
        """
        self.camera_id = camera_id
        self.cap = None
        self.running = False
        
        # MediaPipe initialization
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Text-to-speech initialization
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        
        # Statistics tracking
        self.start_time = None
        self.gesture_counts = defaultdict(int)
        self.total_gestures = 0
        self.current_finger_count = None
        self.last_announcement_time = 0
        self.last_announced_count = None  # Track last announced count to prevent repetition
        self.announcement_cooldown = 1.5  # seconds between announcements
        
        # Threading for TTS (non-blocking)
        self.tts_thread = None
        self.tts_lock = threading.Lock()
        
    def _configure_tts(self):
        """Configure text-to-speech engine settings"""
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Find and set an English voice (prefer US or UK English)
                english_voice = None
                for voice in voices:
                    # Check if voice name or ID contains English indicators
                    voice_info = f"{voice.name} {voice.id}".lower()
                    if any(lang in voice_info for lang in ['en', 'english', 'us', 'uk', 'american', 'british']):
                        english_voice = voice.id
                        break
                
                # If no explicit English voice found, try common indices
                if english_voice is None:
                    # On macOS, index 0 is usually English, index 1 might be different language
                    if len(voices) > 0:
                        english_voice = voices[0].id
                    else:
                        english_voice = voices[0].id if voices else None
                
                if english_voice:
                    self.tts_engine.setProperty('voice', english_voice)
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        except Exception as e:
            print(f"Warning: Could not configure TTS voice settings: {e}")
    
    def _is_finger_up(self, landmarks: List, finger_tip: int, finger_pip: int, 
                     finger_mcp: int, is_right_hand: bool) -> bool:
        """Check if a finger is extended/up
        
        Args:
            landmarks: Hand landmarks from MediaPipe
            finger_tip: Index of finger tip landmark
            finger_pip: Index of finger PIP joint
            finger_mcp: Index of finger MCP joint
            is_right_hand: Whether this is a right hand
            
        Returns:
            True if finger is up, False otherwise
        """
        # Get landmark positions
        tip = landmarks[finger_tip]
        pip = landmarks[finger_pip]
        mcp = landmarks[finger_mcp]
        
        # For thumb, use x-coordinate comparison with MCP (more accurate)
        if finger_tip == self.THUMB_TIP:
            if is_right_hand:
                # For right hand, thumb is up if tip.x > mcp.x
                return tip.x > mcp.x
            else:
                # For left hand, thumb is up if tip.x < mcp.x
                return tip.x < mcp.x
        else:
            # For other fingers, compare y-coordinates
            # In MediaPipe, y=0 is top, so tip.y < pip.y means finger is up
            # Use PIP as reference point for better accuracy
            return tip.y < pip.y
    
    def count_fingers(self, landmarks: List, handedness: str) -> int:
        """Count the number of extended fingers
        
        Args:
            landmarks: Hand landmarks from MediaPipe
            handedness: 'Left' or 'Right'
            
        Returns:
            Number of extended fingers (0-5)
        """
        is_right_hand = (handedness == 'Right')
        
        # Check each finger
        thumb_up = self._is_finger_up(
            landmarks, self.THUMB_TIP, self.THUMB_IP, self.THUMB_MCP, is_right_hand
        )
        index_up = self._is_finger_up(
            landmarks, self.INDEX_TIP, self.INDEX_PIP, self.INDEX_MCP, is_right_hand
        )
        middle_up = self._is_finger_up(
            landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP, self.MIDDLE_MCP, is_right_hand
        )
        ring_up = self._is_finger_up(
            landmarks, self.RING_TIP, self.RING_PIP, self.RING_MCP, is_right_hand
        )
        pinky_up = self._is_finger_up(
            landmarks, self.PINKY_TIP, self.PINKY_PIP, self.PINKY_MCP, is_right_hand
        )
        
        # Count extended fingers
        finger_count = sum([thumb_up, index_up, middle_up, ring_up, pinky_up])
        return finger_count
    
    def recognize_gesture(self, landmarks: List, handedness: str) -> str:
        """Recognize specific gestures based on finger positions
        
        Args:
            landmarks: Hand landmarks from MediaPipe
            handedness: 'Left' or 'Right'
            
        Returns:
            Gesture name (e.g., 'Fist', 'Open Palm', 'Peace Sign', etc.)
        """
        is_right_hand = (handedness == 'Right')
        
        thumb_up = self._is_finger_up(
            landmarks, self.THUMB_TIP, self.THUMB_IP, self.THUMB_MCP, is_right_hand
        )
        index_up = self._is_finger_up(
            landmarks, self.INDEX_TIP, self.INDEX_PIP, self.INDEX_MCP, is_right_hand
        )
        middle_up = self._is_finger_up(
            landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP, self.MIDDLE_MCP, is_right_hand
        )
        ring_up = self._is_finger_up(
            landmarks, self.RING_TIP, self.RING_PIP, self.RING_MCP, is_right_hand
        )
        pinky_up = self._is_finger_up(
            landmarks, self.PINKY_TIP, self.PINKY_PIP, self.PINKY_MCP, is_right_hand
        )
        
        fingers = [thumb_up, index_up, middle_up, ring_up, pinky_up]
        count = sum(fingers)
        
        # Gesture recognition logic
        if count == 0:
            return "Fist"
        elif count == 5:
            return "Open Palm"
        elif count == 2 and index_up and middle_up and not thumb_up and not ring_up and not pinky_up:
            return "Peace Sign"
        elif count == 1 and index_up and not middle_up and not ring_up and not pinky_up:
            return "Pointing"
        elif count == 3 and thumb_up and index_up and pinky_up and not middle_up and not ring_up:
            return "Rock On"
        elif count == 4 and not pinky_up:
            return "Four Fingers"
        else:
            return f"{count} Fingers"
    
    def _announce_finger_count(self, count: int, gesture: str = None):
        """Announce finger count using text-to-speech with debouncing
        
        Args:
            count: Number of fingers
            gesture: Optional gesture name
        """
        current_time = time.time()
        
        # Debouncing: only announce if count changed AND enough time has passed
        if self.last_announced_count == count:
            return  # Don't announce same count again
        
        if current_time - self.last_announcement_time < self.announcement_cooldown:
            return  # Don't announce too frequently
        
        # Prepare announcement text with correct grammar
        if count == 0:
            text = "0 fingers"
        elif count == 1:
            text = "1 finger"
        else:
            text = f"{count} fingers"
        
        # Don't add gesture info to keep announcements simple and clear
        # Announce in a separate thread to avoid blocking video processing
        if not self.tts_thread or not self.tts_thread.is_alive():
            self.last_announcement_time = current_time
            self.last_announced_count = count  # Track what we're about to announce
            self.tts_thread = threading.Thread(
                target=self._speak, args=(text,), daemon=True
            )
            self.tts_thread.start()
    
    def _speak(self, text: str):
        """Internal method to speak text (runs in thread)"""
        try:
            with self.tts_lock:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
    
    def _draw_statistics(self, frame: np.ndarray):
        """Draw statistics overlay on the frame
        
        Args:
            frame: Input frame to draw on
        """
        height, width = frame.shape[:2]
        
        # Create semi-transparent overlay for statistics
        overlay = frame.copy()
        
        # Statistics panel background
        panel_height = 200
        cv2.rectangle(overlay, (10, 10), (400, panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Calculate runtime
        if self.start_time:
            runtime = datetime.now() - self.start_time
            runtime_str = str(runtime).split('.')[0]  # Remove microseconds
        else:
            runtime_str = "00:00:00"
        
        # Display statistics
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        color = (255, 255, 255)
        thickness = 1
        line_height = 25
        y_offset = 35
        
        stats = [
            f"Runtime: {runtime_str}",
            f"Total Gestures: {self.total_gestures}",
            f"Current: {self.current_finger_count if self.current_finger_count is not None else 'N/A'} fingers"
        ]
        
        # Most common gesture
        if self.gesture_counts:
            most_common = max(self.gesture_counts.items(), key=lambda x: x[1])
            stats.append(f"Most Common: {most_common[0]} ({most_common[1]}x)")
        
        for i, stat in enumerate(stats):
            y = y_offset + i * line_height
            cv2.putText(frame, stat, (20, y), font, font_scale, color, thickness, cv2.LINE_AA)
    
    def _draw_finger_count_display(self, frame: np.ndarray, count: int):
        """Draw large finger count display
        
        Args:
            frame: Input frame to draw on
            count: Number of fingers to display
        """
        height, width = frame.shape[:2]
        
        # Large number display in center-top
        font = cv2.FONT_HERSHEY_TRIPLEX
        font_scale = 5.0
        thickness = 8
        
        text = str(count)
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Position in center-top
        x = (width - text_width) // 2
        y = text_height + 50
        
        # Draw shadow for better visibility
        cv2.putText(frame, text, (x + 3, y + 3), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
        
        # Color-coded display
        colors = [
            (50, 50, 50),      # 0 - Dark gray
            (0, 255, 255),     # 1 - Yellow
            (0, 255, 0),       # 2 - Green
            (255, 165, 0),     # 3 - Orange
            (0, 165, 255),     # 4 - Blue
            (255, 0, 255)      # 5 - Magenta
        ]
        color = colors[min(count, 5)]
        
        # Draw main text
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)
    
    def _draw_gesture_label(self, frame: np.ndarray, gesture: str):
        """Draw gesture name below finger count
        
        Args:
            frame: Input frame to draw on
            gesture: Gesture name to display
        """
        height, width = frame.shape[:2]
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        thickness = 2
        color = (255, 255, 255)
        
        (text_width, text_height), baseline = cv2.getTextSize(gesture, font, font_scale, thickness)
        x = (width - text_width) // 2
        y = 150
        
        # Background for better visibility (semi-transparent)
        overlay = frame.copy()
        cv2.rectangle(overlay, (x - 10, y - text_height - 5), 
                     (x + text_width + 10, y + baseline + 5), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(frame, gesture, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a single frame and return annotated frame
        
        Args:
            frame: Input frame from webcam
            
        Returns:
            Annotated frame with overlays
        """
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        # Process with MediaPipe
        results = self.hands.process(rgb_frame)
        
        # Convert back to BGR for OpenCV
        rgb_frame.flags.writeable = True
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        # Track total finger count across all hands
        total_finger_count = 0
        detected_gesture = None
        primary_hand_landmarks = None
        primary_hand_label = None
        
        # Process each detected hand
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Count fingers for this hand
                hand_label = handedness.classification[0].label
                landmarks = hand_landmarks.landmark
                finger_count = self.count_fingers(landmarks, hand_label)
                
                # Sum finger counts from all hands
                total_finger_count += finger_count
                
                # Track first hand for gesture recognition (can be enhanced later)
                if primary_hand_landmarks is None:
                    primary_hand_landmarks = landmarks
                    primary_hand_label = hand_label
        
        # Recognize gesture for the primary hand
        if primary_hand_landmarks is not None and primary_hand_label is not None:
            detected_gesture = self.recognize_gesture(primary_hand_landmarks, primary_hand_label)
        
        # Update statistics
        if total_finger_count != self.current_finger_count:
            self.current_finger_count = total_finger_count
            
            if detected_gesture:
                self.gesture_counts[detected_gesture] += 1
                self.total_gestures += 1
            
            # Announce change (always announce, even if no gesture detected)
            self._announce_finger_count(total_finger_count, detected_gesture)
        
        # Draw overlays
        self._draw_finger_count_display(frame, total_finger_count)
        
        if detected_gesture:
            self._draw_gesture_label(frame, detected_gesture)
        
        self._draw_statistics(frame)
        
        return frame
    
    def run(self):
        """Main application loop"""
        try:
            # Initialize camera
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                raise RuntimeError(f"Error: Could not open camera {self.camera_id}")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            self.running = True
            self.start_time = datetime.now()
            
            print("Finger Counter Application Started")
            print("Press 'q' to quit")
            print("-" * 50)
            
            while self.running:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Warning: Failed to grab frame")
                    break
                
                # Process frame
                annotated_frame = self.process_frame(frame)
                
                # Display frame
                cv2.imshow('Finger Counter - Professional Edition', annotated_frame)
                
                # Check for quit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"Error in main loop: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up resources...")
        self.running = False
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        # Stop TTS engine
        try:
            self.tts_engine.stop()
        except:
            pass
        
        print("Cleanup complete. Goodbye!")


def main():
    """Entry point for the application"""
    print("=" * 50)
    print("Professional Finger Counter Application")
    print("=" * 50)
    
    try:
        app = FingerCounter(camera_id=0)
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
