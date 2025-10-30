#!/usr/bin/env python
"""
Test script to verify all components of the mood-driven LED system
Run this to diagnose any issues before running the full system
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Python Modules Import")
    print("="*60)
    
    try:
        print("✓ Importing cv2 (OpenCV)...", end=" ")
        import cv2
        print("✅")
    except ImportError as e:
        print(f"❌ {e}")
        return False
    
    try:
        print("✓ Importing tensorflow...", end=" ")
        import tensorflow as tf
        print("✅")
    except ImportError as e:
        print(f"❌ {e}")
        return False
    
    try:
        print("✓ Importing numpy...", end=" ")
        import numpy as np
        print("✅")
    except ImportError as e:
        print(f"❌ {e}")
        return False
    
    try:
        print("✓ Importing serial...", end=" ")
        import serial
        print("✅")
    except ImportError as e:
        print(f"❌ {e}")
        return False
    
    try:
        print("✓ Importing led_control...", end=" ")
        from led_control import LEDController
        print("✅")
    except ImportError as e:
        print(f"❌ {e}")
        return False
    
    try:
        print("✓ Importing emotion_detector...", end=" ")
        from emotion_detector import AdvancedEmotionDetector
        print("✅")
    except ImportError as e:
        print(f"❌ {e}")
        return False
    
    return True


def test_camera():
    """Test if camera is accessible"""
    print("\n" + "="*60)
    print("TEST 2: Camera Access")
    print("="*60)
    
    try:
        import cv2
        print("✓ Attempting to open camera...", end=" ")
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print("✅")
                print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
                cap.release()
                return True
            else:
                print("❌ Camera opened but cannot read frames")
                cap.release()
                return False
        else:
            print("❌ Cannot open camera - check if it's in use")
            return False
    except Exception as e:
        print(f"❌ {e}")
        return False


def test_emotion_detector():
    """Test if emotion detector loads"""
    print("\n" + "="*60)
    print("TEST 3: Emotion Detector")
    print("="*60)
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        print("✓ Loading emotion model...", end=" ")
        from emotion_detector import AdvancedEmotionDetector
        
        detector = AdvancedEmotionDetector()
        print("✅")
        
        # Test prediction
        import cv2
        import numpy as np
        
        print("✓ Testing emotion prediction...", end=" ")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                emotion, confidence = detector.predict_emotion(frame)
                print("✅")
                print(f"  Sample prediction: {emotion} ({confidence*100:.1f}%)")
                cap.release()
                return True
            cap.release()
        
        print("⚠️  Could not test with camera")
        return True
    
    except Exception as e:
        print(f"❌ {e}")
        return False


def test_led_controller():
    """Test LED controller"""
    print("\n" + "="*60)
    print("TEST 4: LED Controller")
    print("="*60)
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        print("✓ Initializing LED Controller...", end=" ")
        from led_control import LEDController
        
        led = LEDController(serial_connection=None)
        print("✅")
        
        # Test emotion to mood mapping
        print("✓ Testing emotion→mood mapping...", end=" ")
        test_emotions = ['happy', 'sad', 'angry', 'neutral']
        success = True
        for emotion in test_emotions:
            mood = led.emotion_to_mood(emotion)
            if mood is None:
                success = False
                break
        
        if success:
            print("✅")
            print(f"  Tested emotions: {', '.join(test_emotions)}")
        else:
            print("❌")
            return False
        
        # Test commands
        print("✓ Testing LED commands...", end=" ")
        led.set_mood('happy', confidence=0.9)
        print("✅")
        
        return True
    
    except Exception as e:
        print(f"❌ {e}")
        return False


def test_arduino_connection():
    """Test Arduino connection"""
    print("\n" + "="*60)
    print("TEST 5: Arduino Connection")
    print("="*60)
    
    try:
        import serial
        import serial.tools.list_ports
        
        print("✓ Scanning COM ports...", end=" ")
        ports = serial.tools.list_ports.comports()
        
        if len(ports) == 0:
            print("⚠️")
            print("  No COM ports found")
            print("  (Arduino may not be connected - this is OK for testing)")
            return True
        
        print("✅")
        print(f"  Found {len(ports)} COM port(s):")
        
        arduino_port = None
        for port in ports:
            print(f"    - {port.device}: {port.description}")
            if 'ARDUINO' in port.description.upper() or 'CH340' in port.description.upper():
                arduino_port = port.device
        
        if arduino_port:
            print(f"\n✓ Attempting to connect to {arduino_port}...", end=" ")
            try:
                ser = serial.Serial(arduino_port, 9600, timeout=2)
                import time
                time.sleep(2)
                
                # Try to read READY message
                if ser.in_waiting > 0:
                    response = ser.read(100).decode('utf-8', errors='ignore')
                    if 'READY' in response:
                        print("✅")
                        print(f"  Arduino responded: {response.strip()}")
                    else:
                        print("⚠️")
                        print(f"  Response: {response.strip()}")
                else:
                    print("⚠️")
                    print("  No response from Arduino (may need to reset)")
                
                ser.close()
                return True
            
            except Exception as e:
                print(f"❌ {e}")
                return False
        else:
            print("  ⚠️  Arduino not identified (may not have drivers installed)")
            return True
    
    except Exception as e:
        print(f"❌ {e}")
        return False


def test_face_detection():
    """Test face detection"""
    print("\n" + "="*60)
    print("TEST 6: Face Detection")
    print("="*60)
    
    try:
        import cv2
        
        print("✓ Loading Haar Cascade...", end=" ")
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        print("✅")
        
        print("✓ Capturing frame from camera...", end=" ")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print("✅")
                
                # Try to detect faces
                print("✓ Detecting faces...", end=" ")
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                print("✅")
                
                if len(faces) > 0:
                    print(f"  Detected {len(faces)} face(s)")
                else:
                    print("  ⚠️  No faces detected (make sure you're in front of camera)")
                
                cap.release()
                return True
        
        print("❌ Cannot access camera")
        return False
    
    except Exception as e:
        print(f"❌ {e}")
        return False


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    tests = [
        ("Python Modules", results[0]),
        ("Camera Access", results[1]),
        ("Emotion Detector", results[2]),
        ("LED Controller", results[3]),
        ("Arduino Connection", results[4]),
        ("Face Detection", results[5]),
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print("="*60)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready to use.")
        print("\nRun: python src/rfid_emotion_led_control.py")
        return True
    elif passed >= 4:
        print("\n⚠️  Some tests failed, but system may still work.")
        print("Check the failures above and fix any issues.")
        return True
    else:
        print("\n❌ Multiple tests failed. Please fix issues before running system.")
        return False


def main():
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "🎭 MOOD-LED SYSTEM - DIAGNOSTIC TEST" + " "*12 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Run tests
    results.append(test_imports())
    results.append(test_camera())
    results.append(test_emotion_detector())
    results.append(test_led_controller())
    results.append(test_arduino_connection())
    results.append(test_face_detection())
    
    # Print summary
    success = print_summary(results)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
