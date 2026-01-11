# Installation Notes

## ⚠️ Important: Python Version Compatibility

**MediaPipe Compatibility Issue with Python 3.14**

MediaPipe currently does not support Python 3.14. MediaPipe supports Python 3.8 through 3.12.

### Solution Options:

#### Option 1: Use Python 3.11 or 3.12 (Recommended)

If you have Python 3.11 or 3.12 installed, create the virtual environment with that version:

```bash
# Check available Python versions
python3.11 --version
python3.12 --version

# Create venv with Python 3.11 or 3.12
python3.11 -m venv venv
# OR
python3.12 -m venv venv

# Then activate and install
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

pip install opencv-python mediapipe pyttsx3 numpy
```

#### Option 2: Install Python 3.11 or 3.12

**macOS (using Homebrew):**
```bash
brew install python@3.11
# OR
brew install python@3.12

# Then use that version:
python3.11 -m venv venv
# OR
python3.12 -m venv venv
```

**macOS (using pyenv):**
```bash
pyenv install 3.11.9
pyenv local 3.11.9
python3 -m venv venv
```

**Windows:**
Download and install Python 3.11 or 3.12 from [python.org](https://www.python.org/downloads/)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv
```

### Currently Installed Packages

The following packages have been successfully installed in the venv:
- ✅ opencv-python
- ✅ pyttsx3
- ✅ numpy
- ❌ mediapipe (requires Python 3.8-3.12)

## Quick Setup (Once Python 3.11/3.12 is Available)

```bash
# 1. Create virtual environment
python3.11 -m venv venv  # or python3.12

# 2. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install opencv-python mediapipe pyttsx3 numpy

# 4. Verify installation
pip list | grep -E "opencv|mediapipe|pyttsx3|numpy"

# 5. Run the application
python finger_counter.py
```
