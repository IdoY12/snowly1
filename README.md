# Professional Real-Time Finger Counting Application

A production-ready Python application for real-time finger counting using computer vision and AI with voice feedback. Features accurate hand detection, finger counting (0-5), gesture recognition, and a professional UI with statistics dashboard.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install opencv-python mediapipe pyttsx3 numpy

# 4. Run the application
python finger_counter.py

# 5. Press 'q' to quit, then deactivate venv
deactivate
```

For detailed instructions, see the [Installation](#installation) section below.

## Features

### Core Functionality
- ✅ **Real-time webcam capture** with smooth hand detection
- ✅ **Accurate finger counting** (0-5 fingers) with proper hand orientation detection
- ✅ **Text-to-speech voice announcements** when finger count changes
- ✅ **Visual display** with MediaPipe hand landmarks overlay
- ✅ **Intelligent debouncing** to prevent announcement spam
- ✅ **Support for both hands** (left and right) with proper orientation detection

### Advanced Features
- 🎯 **Gesture recognition**: Peace sign, Fist, Open Palm, Pointing, Rock On, and more
- 📊 **Real-time statistics dashboard** showing:
  - Runtime duration
  - Total gestures detected
  - Current finger count
  - Most common gesture
- 🎨 **Professional UI** with:
  - Semi-transparent overlays
  - Large, clear on-screen number display (color-coded)
  - Visual gesture labels
  - Hand landmarks visualization
- ⚡ **Performance optimized** for real-time processing

## Requirements

- Python 3.8 or higher
- Webcam/Camera device
- Operating System: Windows, macOS, or Linux

## Installation

### Step 1: Create a Virtual Environment

**⚠️ IMPORTANT: Always use a virtual environment to avoid conflicts with system packages.**

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Note:** After activation, you should see `(venv)` at the beginning of your command prompt.

### Step 2: Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install opencv-python mediapipe pyttsx3 numpy
```

**Alternative (using requirements.txt):**
```bash
pip install -r requirements.txt
```

This will install:
- `opencv-python` (>=4.8.0) - Computer vision and webcam interface
- `mediapipe` (>=0.10.0) - Hand detection and landmark tracking
- `pyttsx3` (>=2.90) - Text-to-speech engine
- `numpy` (>=1.24.0) - Numerical operations

### Step 3: Verify Installation

Verify that packages are installed correctly:

```bash
pip list
```

You should see `opencv-python`, `mediapipe`, `pyttsx3`, and `numpy` in the list.

## Usage

### Running the Application

**⚠️ IMPORTANT: Always activate the virtual environment before running the application.**

1. **Activate the virtual environment** (if not already activated):

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
  venv\Scripts\activate
   ```

2. **Run the application:**
   ```bash
   python finger_counter.py
   ```

   Or on some systems:
   ```bash
   python3 finger_counter.py
   ```

3. **Deactivate the virtual environment** when done:
   ```bash
   deactivate
   ```

### Controls

- **'q' key**: Quit the application
- **Ctrl+C**: Interrupt and exit (cleanup will be performed)

### How It Works

1. **Launch**: The application opens your default webcam
2. **Position your hand(s)**: Place one or both hands in front of the camera
3. **Count fingers**: The system detects and counts extended fingers in real-time
4. **Voice feedback**: When the finger count changes, you'll hear: "You are holding up [number] finger(s)"
5. **Visual feedback**: 
   - Large number display (center-top) shows the current count
   - Hand landmarks are overlaid on detected hands
   - Gesture name appears below the number
   - Statistics panel shows runtime and gesture history

## Technical Details

### Architecture

The application uses an object-oriented design with clear separation of concerns:

- **FingerCounter Class**: Main application class handling all functionality
- **MediaPipe Hands**: State-of-the-art hand detection and landmark tracking
- **OpenCV**: Webcam interface and image processing
- **pyttsx3**: Cross-platform text-to-speech engine

### Finger Counting Algorithm

The application uses MediaPipe's hand landmarks to determine finger states:

1. **Landmark Detection**: MediaPipe detects 21 hand landmarks per hand
2. **Finger State Detection**: For each finger, compares tip position with PIP joint:
   - Thumb: Uses x-coordinate comparison (handedness-aware)
   - Other fingers: Uses y-coordinate comparison
3. **Orientation Awareness**: Handles both left and right hands correctly
4. **Multi-hand Support**: Tracks maximum finger count across all detected hands

### Gesture Recognition

Recognized gestures include:
- **Fist** (0 fingers)
- **Open Palm** (5 fingers)
- **Peace Sign** (index + middle)
- **Pointing** (index only)
- **Rock On** (thumb + index + pinky)
- **Four Fingers** (all except pinky)
- **Generic counts** for other combinations

### Text-to-Speech

- Uses `pyttsx3` for cross-platform TTS
- Runs in a separate thread to avoid blocking video processing
- Implements debouncing (1.5 second cooldown) to prevent announcement spam
- Configurable voice, rate, and volume

### Performance Optimization

- Efficient MediaPipe processing with optimized confidence thresholds
- Non-blocking TTS using threading
- Minimal frame processing overhead
- Real-time performance on modern hardware

## Troubleshooting

### Camera Issues

**Problem**: "Error: Could not open camera"

**Solutions**:
1. Check if another application is using the camera
2. Verify camera permissions (especially on macOS)
3. Try different camera IDs: Modify `camera_id=0` to `camera_id=1` in the code
4. On Linux, ensure you have video device access permissions

**macOS Specific**:
- Grant camera permissions in System Preferences → Security & Privacy → Camera
- Check System Preferences → Privacy → Camera

### Text-to-Speech Issues

**Problem**: No voice output or errors with TTS

**Solutions**:
1. **macOS**: TTS should work out of the box
2. **Windows**: Ensure you have SAPI5 installed (usually pre-installed)
3. **Linux**: Install `espeak` or `festival`:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install espeak
   
   # Fedora
   sudo dnf install espeak
   ```
4. If issues persist, check the console for TTS error messages

### Performance Issues

**Problem**: Low FPS or laggy video

**Solutions**:
1. Reduce camera resolution in the code (modify `CAP_PROP_FRAME_WIDTH/HEIGHT`)
2. Ensure good lighting for better hand detection
3. Close other applications using the camera or CPU
4. Lower MediaPipe confidence thresholds if needed (in code)

### Hand Detection Issues

**Problem**: Hands not detected or incorrect finger count

**Solutions**:
1. **Lighting**: Ensure good, even lighting on your hands
2. **Background**: Use a contrasting background (avoid similar skin tones)
3. **Distance**: Keep hands at a reasonable distance (1-3 feet from camera)
4. **Angle**: Face hands toward the camera
5. **Clarity**: Avoid fast movements, keep hands steady

### Dependency Installation Issues

**Problem**: Errors installing dependencies

**Solutions**:
1. **Windows**: May need Visual C++ Build Tools for some packages
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. **macOS**: May need Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```
3. **Linux**: Install system dependencies:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-pip python3-dev
   sudo apt-get install libopencv-dev python3-opencv
   
   # Fedora
   sudo dnf install python3-pip python3-devel
   sudo dnf install opencv-python
   ```
4. Upgrade pip: `pip install --upgrade pip`

### Import Errors

**Problem**: "ModuleNotFoundError" when running

**Solutions**:
1. Ensure virtual environment is activated
2. Verify all dependencies are installed: `pip list`
3. Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

## Advanced Configuration

### Customizing Camera ID

Edit `finger_counter.py`:

```python
app = FingerCounter(camera_id=1)  # Change from 0 to 1, 2, etc.
```

### Adjusting Announcement Cooldown

Modify the debouncing delay:

```python
self.announcement_cooldown = 2.0  # Change from 1.5 to desired seconds
```

### Changing TTS Voice Settings

Modify in `_configure_tts()` method:

```python
self.tts_engine.setProperty('rate', 150)      # Speed (words per minute)
self.tts_engine.setProperty('volume', 0.9)    # Volume (0.0 to 1.0)
```

### Adjusting Hand Detection Sensitivity

Modify MediaPipe initialization:

```python
self.hands = self.mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,  # Lower = more sensitive
    min_tracking_confidence=0.5    # Lower = more persistent
)
```

## Code Structure

```
tamp_proj/
├── finger_counter.py      # Main application file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Key Methods

- `__init__()`: Initialize MediaPipe, TTS, and statistics
- `count_fingers()`: Count extended fingers for a hand
- `recognize_gesture()`: Identify specific gestures
- `_announce_finger_count()`: Handle TTS announcements with debouncing
- `process_frame()`: Main frame processing pipeline
- `run()`: Main application loop
- `cleanup()`: Resource cleanup on exit

## Contributing

This is a production-ready application. To extend it:

1. Add new gestures in `recognize_gesture()`
2. Customize UI in drawing methods (`_draw_*`)
3. Modify statistics tracking as needed
4. Enhance TTS features in `_announce_finger_count()`

## License

This project is provided as-is for educational and commercial use.

## Acknowledgments

- **MediaPipe**: Google's hand detection solution
- **OpenCV**: Computer vision library
- **pyttsx3**: Cross-platform text-to-speech engine

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review console output for error messages
3. Verify all dependencies are correctly installed
4. Ensure camera permissions are granted (macOS/Linux)

---

**Enjoy counting fingers with AI!** 🖐️🤖
