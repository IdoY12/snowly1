# Finger Counter Application - Run Instructions

## ✅ Setup Verification Complete

All code has been tested and verified:
- ✓ Python 3.12 is correctly configured
- ✓ All dependencies installed (opencv-python, mediapipe, pyttsx3, numpy)
- ✓ Code syntax is valid
- ✓ Application initializes correctly
- ✓ TTS engine configured properly
- ✓ MediaPipe hands model loads successfully
- ✓ Bug fix applied: Announcements now trigger for all count changes

---

## 1. Final Setup Verification

Before running the application, verify everything is set up correctly:

```bash
# Make sure you're in the project directory
cd /Users/idoyahav/Desktop/git/tamp_proj

# Activate the virtual environment
source venv/bin/activate

# Run the verification script (optional but recommended)
python verify_setup.py
```

**Expected output:**
```
✓ ALL CHECKS PASSED!
You're ready to run the application:
  python finger_counter.py
```

If any checks fail, see the Troubleshooting section below.

---

## 2. Step-by-Step Instructions to Run the Application

### Step 1: Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 2: Run the Application

```bash
python finger_counter.py
```

**Alternative (if `python` doesn't work):**
```bash
python3 finger_counter.py
```

### Step 3: Grant Camera Permissions (macOS - First Time Only)

When you run the application for the first time on macOS, you'll see a system dialog asking for camera permission:

1. Click **"Open System Settings"** or go to **System Preferences → Security & Privacy → Camera**
2. Check the box next to **Terminal** (or **Python** if it appears)
3. Return to the terminal window

The application should now access your camera.

### Step 4: Use the Application

- **Position your hand(s)** in front of the camera
- **Hold up fingers** (0-5) and watch the count update in real-time
- **Listen for voice announcements** when the count changes
- **Press 'q'** to quit the application

### Step 5: Deactivate Virtual Environment (When Done)

```bash
deactivate
```

---

## 3. What to Expect When It Runs

### Initial Launch

When you first run the application, you'll see:

```
==================================================
Professional Finger Counter Application
==================================================
Finger Counter Application Started
Press 'q' to quit
--------------------------------------------------
```

### On-Screen Display

A window titled **"Finger Counter - Professional Edition"** will open showing:

1. **Live camera feed** (mirrored for natural interaction)
2. **Large number display** (center-top) showing the current finger count (0-5)
   - Color-coded: 0=gray, 1=yellow, 2=green, 3=orange, 4=blue, 5=magenta
3. **Hand landmarks** - Overlay showing detected hand joints and connections
4. **Gesture label** - Below the number (e.g., "Fist", "Open Palm", "Peace Sign")
5. **Statistics panel** (top-left) showing:
   - Runtime duration
   - Total gestures detected
   - Current finger count
   - Most common gesture

### Voice Announcements

When you change the number of fingers you're holding up, you'll hear:
- **"You are holding up zero fingers"** (for 0)
- **"You are holding up 1 finger"** (for 1)
- **"You are holding up X fingers"** (for 2-5)

**Note:** Announcements have a 1.5-second cooldown to prevent spam. If you're moving quickly between counts, not every change will be announced.

### Expected Behavior

✅ **Camera opens successfully** - Video feed appears immediately  
✅ **Hand detection works** - Hand landmarks appear when hands are in frame  
✅ **Finger counting is accurate** - Count updates in real-time (0-5)  
✅ **Voice announcements work** - TTS speaks when count changes  
✅ **Display shows count clearly** - Large number visible on screen  
✅ **No errors in terminal** - Clean output, only warnings if any

---

## 4. Troubleshooting Guide for Common Issues

### Issue: "Error: Could not open camera"

**Possible Causes:**
- Camera is being used by another application
- Camera permissions not granted
- Camera device ID is incorrect

**Solutions:**

1. **Close other applications** using the camera (Zoom, FaceTime, Photo Booth, etc.)

2. **Grant camera permissions** (macOS):
   - System Preferences → Security & Privacy → Camera
   - Check the box for Terminal or Python

3. **Try a different camera ID**:
   - Edit `finger_counter.py` line 516:
     ```python
     app = FingerCounter(camera_id=1)  # Try 1, 2, etc.
     ```

4. **Check if camera works**:
   ```bash
   # Test camera with OpenCV
   python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera available:', cap.isOpened()); cap.release()"
   ```

### Issue: No Voice Output / TTS Not Working

**Possible Causes:**
- TTS engine not configured properly
- System TTS not available
- Volume is muted

**Solutions:**

1. **macOS**: TTS should work out of the box. If not:
   - Check System Preferences → Accessibility → Spoken Content
   - Verify "Speak selection" is enabled (optional)

2. **Test TTS directly**:
   ```bash
   python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Test'); engine.runAndWait()"
   ```

3. **Check console for TTS errors** - Look for error messages in the terminal

4. **Volume**: Make sure your system volume is not muted

### Issue: Hands Not Detected / Incorrect Finger Count

**Possible Causes:**
- Poor lighting
- Background too similar to skin color
- Hand too close or too far from camera
- Hand not facing camera

**Solutions:**

1. **Improve lighting**: Use even, bright lighting on your hands
2. **Use contrasting background**: Avoid backgrounds that match your skin tone
3. **Adjust distance**: Keep hands 1-3 feet from camera
4. **Face camera**: Ensure hands are facing the camera, not at extreme angles
5. **Slow movements**: Avoid fast movements, keep hands steady
6. **Clean background**: Use a simple, contrasting background

### Issue: Application Crashes or Freezes

**Possible Causes:**
- Outdated dependencies
- Memory issues
- Camera hardware problems

**Solutions:**

1. **Update dependencies**:
   ```bash
   pip install --upgrade opencv-python mediapipe pyttsx3 numpy
   ```

2. **Check for errors**: Look at the terminal output for error messages

3. **Restart**: Close the application (press 'q') and try again

4. **Reduce camera resolution**: Edit `finger_counter.py` lines 453-454:
   ```python
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
   ```

### Issue: "ModuleNotFoundError" or Import Errors

**Solutions:**

1. **Verify virtual environment is activated**:
   ```bash
   # You should see (venv) in your prompt
   which python  # Should point to venv/bin/python
   ```

2. **Reinstall dependencies**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check installation**:
   ```bash
   pip list | grep -E "(opencv|mediapipe|pyttsx3|numpy)"
   ```

### Issue: Low FPS / Laggy Video

**Solutions:**

1. **Reduce camera resolution** (see above)
2. **Close other applications** using CPU/GPU
3. **Improve lighting** for better detection (less processing needed)
4. **Lower detection sensitivity**: Edit `finger_counter.py` lines 64-69:
   ```python
   self.hands = self.mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=1,  # Reduce from 2 to 1
       min_detection_confidence=0.7,  # Increase from 0.5
       min_tracking_confidence=0.7    # Increase from 0.5
   )
   ```

### Issue: Python Version Error

**Solution:**

The application requires Python 3.8+. Verify your version:
```bash
python --version  # or python3 --version
```

If you need to use Python 3.12 specifically (as in this setup):
```bash
python3.12 finger_counter.py
```

---

## 5. Quick Reference Commands

### Setup and Verification

```bash
# Activate virtual environment
source venv/bin/activate

# Verify setup
python verify_setup.py

# Check Python version
python --version

# Check installed packages
pip list | grep -E "(opencv|mediapipe|pyttsx3|numpy)"
```

### Running the Application

```bash
# Run application
python finger_counter.py

# Run with Python 3 explicitly
python3 finger_counter.py

# Deactivate when done
deactivate
```

### Testing Components

```bash
# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera:', cap.isOpened()); cap.release()"

# Test TTS
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Test'); engine.runAndWait()"

# Test imports
python -c "import cv2, mediapipe, pyttsx3, numpy; print('All imports OK')"
```

---

## 6. Application Features Summary

✅ **Real-time webcam capture** - Live video feed  
✅ **Hand detection** - MediaPipe hand landmarks overlay  
✅ **Finger counting** - Accurate 0-5 finger detection  
✅ **Voice announcements** - TTS speaks count when it changes  
✅ **Visual display** - Large, color-coded number display  
✅ **Gesture recognition** - Recognizes common gestures  
✅ **Statistics dashboard** - Shows runtime and gesture history  
✅ **Multi-hand support** - Works with both hands  
✅ **Debouncing** - Prevents announcement spam  
✅ **Clean exit** - Proper resource cleanup on quit

---

## 7. Testing Checklist

Before reporting issues, verify:

- [ ] Virtual environment is activated (`(venv)` in prompt)
- [ ] All packages installed (`python verify_setup.py` passes)
- [ ] Camera permissions granted (macOS)
- [ ] No other apps using camera
- [ ] Good lighting conditions
- [ ] Hand positioned 1-3 feet from camera
- [ ] Hand facing camera (not at extreme angles)
- [ ] System volume not muted
- [ ] Console output reviewed for error messages

---

## 8. Support

If you encounter issues not covered here:

1. **Check console output** for error messages
2. **Review this troubleshooting guide** thoroughly
3. **Verify setup** using `python verify_setup.py`
4. **Test individual components** (camera, TTS) separately
5. **Check system requirements** (Python 3.8+, camera hardware)

---

## Ready to Run!

Everything has been tested and verified. Your application is ready to use:

```bash
source venv/bin/activate
python finger_counter.py
```

**Enjoy counting fingers with AI!** 🖐️🤖
