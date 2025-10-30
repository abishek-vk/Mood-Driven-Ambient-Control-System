#!/usr/bin/env python
"""
RFID + Facial Emotion Detection Integration
Listens to Arduino for RFID scan, then performs emotion analysis
"""

import cv2
import numpy as np
import serial
import serial.tools.list_ports
import threading
import time
import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

# Import emotion and face detectors
from face_detector_advanced import AdvancedFaceDetector
from emotion_detector import AdvancedEmotionDetector

class ArduinoRFIDListener:
    """Listens to Arduino RFID scanner"""
    def __init__(self, baudrate=9600):
        self.ser = None
        self.baudrate = baudrate
        self.last_status = None
        self.running = False
        self.port_name = None
        
    def find_arduino(self):
        """Find Arduino COM port - checks multiple criteria"""
        ports = serial.tools.list_ports.comports()
        
        print("Available COM ports:")
        for port in ports:
            print(f"  - {port.device}: {port.description} (hwid: {port.hwid})")
        
        # Try to find Arduino
        for port in ports:
            desc = port.description.upper()
            if ('ARDUINO' in desc or 'CH340' in desc or 'USB' in desc or 
                'SERIAL' in desc or 'UART' in desc):
                print(f"\n✓ Found Arduino-like device at: {port.device}")
                return port.device
        
        return None
    
    def connect(self):
        """Connect to Arduino with retry logic"""
        try:
            port = self.find_arduino()
            if port is None:
                print("\n⚠️  No Arduino found on COM ports")
                print("Make sure Arduino is connected and drivers are installed")
                return False
            
            self.port_name = port
            
            # Try to open connection
            print(f"\nConnecting to Arduino on {port} at {self.baudrate} baud...")
            self.ser = serial.Serial(port, self.baudrate, timeout=1)
            
            # Wait for Arduino to initialize after serial connection
            print("Waiting for Arduino to initialize...")
            time.sleep(2)
            
            # Clear any garbage data from serial buffer
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            
            print(f"✅ Successfully connected to Arduino on {port}")
            return True
            
        except serial.SerialException as e:
            print(f"❌ Serial connection error: {e}")
            print(f"   Make sure:")
            print(f"   1. Arduino is connected via USB")
            print(f"   2. COM port is correct")
            print(f"   3. No other program is using this COM port")
            return False
        except Exception as e:
            print(f"❌ Error connecting to Arduino: {e}")
            return False
    
    def read_status(self):
        """Read status from Arduino with error handling"""
        if self.ser is None or not self.ser.is_open:
            return None
        
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    print(f"[Arduino] {line}")
                    return line
        except UnicodeDecodeError:
            # Ignore decode errors
            pass
        except Exception as e:
            print(f"⚠️  Error reading from Arduino: {e}")
        
        return None
    
    def disconnect(self):
        """Safely disconnect from Arduino"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"✅ Disconnected from Arduino")

class EmotionAnalyzer:
    """Performs emotion analysis on detected faces"""
    def __init__(self):
        print("Loading Face Detector...")
        self.face_detector = AdvancedFaceDetector()
        
        print("Loading Emotion Detector...")
        self.emotion_detector = AdvancedEmotionDetector()
        
        self.cap = None
        self.analyzing = False
    
    def start_camera(self):
        """Start camera"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Cannot open camera")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        print("✅ Camera started")
        return True
    
    def analyze_emotion(self, duration=10):
        """Analyze emotions for specified duration (in seconds)"""
        if self.cap is None:
            print("Camera not available")
            return
        
        self.analyzing = True
        start_time = time.time()
        frame_count = 0
        emotions_detected = {}
        
        print(f"\n🎥 Emotion Analysis Started ({duration}s)")
        print("="*60)
        
        while self.analyzing and (time.time() - start_time) < duration:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame_count += 1
            frame = cv2.flip(frame, 1)
            
            # Detect faces
            faces = self.face_detector.detect_faces(frame)
            
            # Analyze each face
            for idx, face in enumerate(faces):
                x, y, w, h = face['bbox']
                
                # Validate coordinates
                if w < 30 or h < 30 or x < 0 or y < 0:
                    continue
                
                x = max(0, x)
                y = max(0, y)
                w = min(w, frame.shape[1] - x)
                h = min(h, frame.shape[0] - y)
                
                face_img = frame[y:y+h, x:x+w]
                
                if face_img is not None and face_img.size > 0:
                    emotion, confidence = self.emotion_detector.predict_emotion(face_img)
                    
                    if emotion:
                        if emotion not in emotions_detected:
                            emotions_detected[emotion] = 0
                        emotions_detected[emotion] += 1
                        
                        # Draw on frame
                        color = self.get_emotion_color(emotion)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        
                        label = f"{emotion}: {confidence*100:.0f}%"
                        cv2.putText(frame, label, (x, y-10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Show info
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            cv2.putText(frame, f"Faces: {len(faces)} | Time: {remaining}s", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to stop", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
            
            cv2.imshow('RFID + Emotion Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.analyzing = False
        
        # Show results
        print("\n" + "="*60)
        print("📊 EMOTION ANALYSIS RESULTS")
        print("="*60)
        
        if emotions_detected:
            total = sum(emotions_detected.values())
            print(f"Frames analyzed: {frame_count}")
            print(f"Total emotions detected: {total}\n")
            
            for emotion, count in sorted(emotions_detected.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total) * 100
                print(f"  {emotion.upper():12} : {count:3} detections ({percentage:5.1f}%)")
            
            # Find dominant emotion
            dominant_emotion = max(emotions_detected, key=emotions_detected.get)
            print(f"\n✅ Dominant Emotion: {dominant_emotion.upper()}")
        else:
            print("❌ No emotions detected")
        
        print("="*60 + "\n")
    
    def get_emotion_color(self, emotion):
        """Get color for emotion"""
        colors = {
            'happy': (0, 255, 0),
            'sad': (255, 0, 0),
            'angry': (0, 0, 255),
            'fear': (255, 0, 255),
            'neutral': (128, 128, 128),
            'disgust': (0, 165, 255),
            'surprise': (0, 255, 255)
        }
        return colors.get(emotion, (255, 255, 255))
    
    def stop_camera(self):
        """Stop camera"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

def main():
    print("\n" + "="*70)
    print("RFID + FACIAL EMOTION DETECTION SYSTEM")
    print("="*70)
    
    # Initialize Arduino listener
    print("\n[1/3] Initializing Arduino RFID Reader...")
    rfid = ArduinoRFIDListener()
    arduino_connected = rfid.connect()
    
    if not arduino_connected:
        print("\n❌ HARDWARE NOT CONNECTED")
        print("Please connect your Arduino and try again")
        return
    
    # Initialize emotion analyzer
    print("\n[2/3] Initializing Emotion Analyzer...")
    analyzer = EmotionAnalyzer()
    
    # Start camera
    print("\n[3/3] Starting Camera...")
    if not analyzer.start_camera():
        print("Cannot start camera")
        rfid.disconnect()
        return
    
    print("\n" + "="*70)
    print("✅ SYSTEM READY - WAITING FOR RFID SCAN")
    print("="*70)
    print("\n📌 Instructions:")
    print("  1. Scan your RFID card on the Arduino reader")
    print("  2. If authorized, emotion analysis will start automatically")
    print("  3. System will analyze emotions for 10 seconds")
    print("  4. Results will be displayed after analysis")
    print("\nPress Ctrl+C to exit\n")
    
    analysis_duration = 10  # 10 seconds per scan
    
    try:
        while True:
            status = rfid.read_status()
            if status:
                if "ACCESS_GRANTED" in status:
                    print("\n" + "="*70)
                    print("✅ RFID CARD AUTHORIZED")
                    print("="*70)
                    print("Starting Emotion Analysis...")
                    analyzer.analyze_emotion(duration=analysis_duration)
                    print("\nWaiting for next RFID scan...\n")
                
                elif "ACCESS_DENIED" in status:
                    print("\n" + "="*70)
                    print("❌ RFID CARD NOT AUTHORIZED")
                    print("="*70)
                    print("Access Denied - Emotion analysis not started\n")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  System interrupted by user")
    
    finally:
        print("\n🛑 Shutting down...")
        analyzer.stop_camera()
        rfid.disconnect()
        print("✅ System closed")

if __name__ == "__main__":
    main()
