#!/usr/bin/env python3
"""
Quick verification script to check that everything is set up correctly
Run this before running finger_counter.py
"""

import sys

def verify_setup():
    """Verify that all dependencies are installed and working"""
    print("=" * 60)
    print("Finger Counter - Setup Verification")
    print("=" * 60)
    
    checks = []
    
    # Check Python version
    print("\n1. Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        checks.append(True)
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        checks.append(False)
    
    # Check imports
    print("\n2. Checking required packages...")
    packages = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'pyttsx3': 'pyttsx3',
        'numpy': 'numpy'
    }
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"   ✓ {package} installed")
            checks.append(True)
        except ImportError:
            print(f"   ✗ {package} NOT installed")
            checks.append(False)
    
    # Check class import
    print("\n3. Checking application code...")
    try:
        from finger_counter import FingerCounter
        print("   ✓ finger_counter.py is valid")
        checks.append(True)
    except Exception as e:
        print(f"   ✗ Error importing finger_counter.py: {e}")
        checks.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    if all(checks):
        print("✓ ALL CHECKS PASSED!")
        print("\nYou're ready to run the application:")
        print("  python finger_counter.py")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running the application.")
        print("Make sure:")
        print("  1. Virtual environment is activated")
        print("  2. All packages are installed: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(verify_setup())
