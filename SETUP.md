# Quick Setup Guide

## Prerequisites
- Python 3.8 or higher
- Webcam/Camera device

## Step-by-Step Setup

### 1. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
```

**Windows:**
```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt when activated.

### 3. Install Dependencies

With the virtual environment activated:

```bash
pip install opencv-python mediapipe pyttsx3 numpy
```

### 4. Run the Application

Make sure the virtual environment is activated, then:

```bash
python finger_counter.py
```

### 5. Deactivate Virtual Environment (when done)

```bash
deactivate
```

## Troubleshooting

### Virtual Environment Not Activating

- **macOS/Linux**: Make sure you use `source venv/bin/activate` (not just `venv/bin/activate`)
- **Windows**: Use `venv\Scripts\activate` (backslashes, not forward slashes)
- Verify the venv folder exists: `ls venv` (macOS/Linux) or `dir venv` (Windows)

### Package Installation Errors

- Make sure the virtual environment is activated before installing
- Upgrade pip: `pip install --upgrade pip`
- Try installing packages individually to identify the problematic one

### Python Not Found

- Use `python3` instead of `python` on macOS/Linux
- Verify Python installation: `python --version` or `python3 --version`
