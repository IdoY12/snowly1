# Hand Finger Counter with Voice Feedback

A fun Python project that uses AI to count your fingers in real-time and speak the result out loud. Point your hand at the webcam and watch it count your fingers!

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## What It Does

- 📹 Opens your webcam and detects hands using MediaPipe
- ✋ Counts fingers (0-5) in real-time
- 🎤 Speaks the number of fingers out loud using text-to-speech
- ✌️ Recognizes basic gestures like Peace sign, Fist, Open Palm, Pointing, and Rock On
- 📊 Shows a simple stats panel with runtime and gesture history

## Quick Start
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
# Option A: Install from requirements.txt
pip install -r requirements.txt

# Option B: Install manually
pip install opencv-python mediapipe pyttsx3 numpy

# 4. Run it!
python finger_counter.py
```

Press `q` to quit when you're done.

## Requirements

- Python 3.8 or higher
- A webcam/camera
- Works on Windows, macOS, and Linux

## Features

- **Real-time finger counting**: Detects and counts 0-5 fingers
- **Voice feedback**: Speaks the count when it changes (e.g., "3 fingers")
- **Gesture recognition**: Identifies Peace sign, Fist, Open Palm, Pointing, Rock On, and more
- **Visual display**: Shows a large number on screen with color coding
- **Stats panel**: Displays runtime, total gestures detected, and most common gesture
- **Both hands supported**: Works with left and right hands

## How to Use

1. Run the application (see Quick Start above)
2. Position your hand(s) in front of the camera
3. The app will detect your hand and count your fingers
4. When the count changes, you'll hear it spoken out loud
5. Watch the stats panel to see your gesture history

**Controls:**
- Press `q` to quit

## Troubleshooting

**Camera not working?** Make sure no other app is using your camera, and check camera permissions in your system settings.

**No voice output?** On Linux, you may need to install `espeak`: `sudo apt-get install espeak`

---

**Enjoy counting fingers with AI!** 🖐️🤖
