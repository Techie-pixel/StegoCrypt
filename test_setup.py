"""
Test script to verify steganography functions work correctly
Run this before using the GUI to ensure everything is installed properly
"""

def test_imports():
    """Test if all required libraries are installed"""
    print("Testing imports...")
    
    try:
        from PIL import Image
        print("✓ Pillow (PIL) imported successfully")
    except ImportError:
        print("✗ Pillow not found. Install: pip install Pillow")
        return False
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError:
        print("✗ OpenCV not found. Install: pip install opencv-python")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError:
        print("✗ NumPy not found. Install: pip install numpy")
        return False
    
    try:
        import wave
        print("✓ Wave module available")
    except ImportError:
        print("✗ Wave module not found (should be built-in)")
        return False
    
    try:
        import tkinter as tk
        print("✓ Tkinter imported successfully")
    except ImportError:
        print("✗ Tkinter not found. Install system package: python3-tk")
        return False
    
    return True


def test_basic_encoding():
    """Test basic encoding/decoding logic"""
    print("\nTesting encoding/decoding logic...")
    
    # Test text to binary conversion
    message = "Test"
    binary = ''.join(format(ord(char), '08b') for char in message)
    print(f"✓ Text to binary: '{message}' -> {binary[:16]}...")
    
    # Test binary to text conversion
    decoded = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            decoded += chr(int(byte, 2))
    
    if decoded == message:
        print(f"✓ Binary to text: {binary[:16]}... -> '{decoded}'")
        return True
    else:
        print(f"✗ Decoding failed: expected '{message}', got '{decoded}'")
        return False


def main():
    print("="*50)
    print("STEGANOGRAPHY TOOL - INSTALLATION TEST")
    print("="*50)
    
    imports_ok = test_imports()
    logic_ok = test_basic_encoding()
    
    print("\n" + "="*50)
    if imports_ok and logic_ok:
        print("✓ ALL TESTS PASSED!")
        print("You can now run: python steganography_app.py")
    else:
        print("✗ SOME TESTS FAILED")
        print("Please install missing dependencies:")
        print("pip install -r requirements.txt")
    print("="*50)


if __name__ == "__main__":
    main()
