#!/usr/bin/env python
"""
RFID + Facial Emotion Detection Integration (Lightweight Version)
Listens to Arduino for RFID scan, then performs emotion analysis
Uses OpenCV for face detection (faster startup)
"""

import cv2
import numpy as np
import serial
import serial.tools.list_ports
import threading
import time
import os
import warnings
import pygame

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

# Import emotion detector only
from emotion_detector import AdvancedEmotionDetector

# Initialize pygame mixer for audio
pygame.mixer.init()

# Define music paths for different emotions
MUSIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'music')
EMOTION_MUSIC = {
    'happy': os.path.join(MUSIC_DIR, 'happy.mp3'),
    'sad': os.path.join(MUSIC_DIR, 'sad.mp3'),
    'angry': os.path.join(MUSIC_DIR, 'angry.mp3'),
    'neutral': os.path.join(MUSIC_DIR, 'neutral.mp3')
}

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
            print(f"  - {port.device}: {port.description}")
        
        # Try to find Arduino by checking device descriptions
        arduino_port = None
        for port in ports:
            desc = port.description.upper()
            # Look specifically for Arduino first
            if 'ARDUINO' in desc:
                arduino_port = port.device
                print(f"\n✓ Found Arduino at: {port.device}")
                break
            # Fallback to CH340 (common Arduino clone chip) if no Arduino found
            elif 'CH340' in desc and not arduino_port:
                arduino_port = port.device
            # Last resort: USB Serial devices
            elif ('USB SERIAL' in desc or 'COM' in desc) and not arduino_port:
                arduino_port = port.device
        
        return arduino_port
        
        return None
    
    def connect(self):
        """Connect to Arduino with retry logic"""
        try:
            port = self.find_arduino()
            if port is None:
                print("\n⚠️  No Arduino found on COM ports")
                return False
            
            self.port_name = port
            
            print(f"\nConnecting to Arduino on {port}...")
            self.ser = serial.Serial(port, self.baudrate, timeout=1)
            
            time.sleep(2)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            
            print(f"✅ Connected to Arduino on {port}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def read_status(self):
        """Read status from Arduino"""
        if self.ser is None or not self.ser.is_open:
            return None
        
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    return line
        except:
            pass
        
        return None
    
    def disconnect(self):
        """Safely disconnect from Arduino"""
        if self.ser and self.ser.is_open:
            self.ser.close()

class EmotionAnalyzer:
    """Performs emotion analysis on detected faces using OpenCV"""
    def __init__(self):
        print("Loading Face Detector (OpenCV)...")
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
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
        """Analyze emotions for specified duration"""
        if self.cap is None:
            print("Camera not available")
            return
        
        self.analyzing = True
        start_time = time.time()
        frame_count = 0
        emotions_detected = {}
        
        print(f"\n{'='*60}")
        print(f"🎥 EMOTION ANALYSIS STARTED ({duration}s)")
        print(f"{'='*60}")
        
        while self.analyzing and (time.time() - start_time) < duration:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame_count += 1
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            
            # Detect faces using OpenCV
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,
                minNeighbors=5,
                minSize=(50, 50),
                maxSize=(400, 400)
            )
            
            # Analyze each face
            for idx, (x, y, w, h) in enumerate(faces):
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
            
            cv2.imshow('RFID + Emotion Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.analyzing = False
        
        # Show results
        print(f"\n{'='*60}")
        print("📊 EMOTION ANALYSIS RESULTS")
        print(f"{'='*60}")
        
        if emotions_detected:
            total = sum(emotions_detected.values())
            print(f"Frames analyzed: {frame_count}")
            print(f"Total emotions detected: {total}\n")
            
            for emotion, count in sorted(emotions_detected.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total) * 100
                print(f"  {emotion.upper():12} : {count:3} detections ({percentage:5.1f}%)")
            
            dominant_emotion = max(emotions_detected, key=emotions_detected.get)
            print(f"\n✅ DOMINANT EMOTION: {dominant_emotion.upper()}")
            
            # Stop any currently playing music
            pygame.mixer.music.stop()
            
            # Play music based on dominant emotion
            if dominant_emotion in EMOTION_MUSIC and os.path.exists(EMOTION_MUSIC[dominant_emotion]):
                print(f"\n🎵 Playing music for {dominant_emotion} mood...")
                pygame.mixer.music.load(EMOTION_MUSIC[dominant_emotion])
                pygame.mixer.music.play()
            else:
                print("\n⚠️ No music file found for this emotion")
        else:
            print("❌ No emotions detected")
        
        print(f"{'='*60}\n")
    
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
    
    # Configuration for emotion analysis
    analysis_duration = 5  # Increased to 30 seconds for better emotion detection
    
    try:
        while True:
            status = rfid.read_status()
            if status:
                if "ACCESS_GRANTED" in status:
                    print("\n" + "="*70)
                    print("✅ RFID CARD AUTHORIZED")
                    print("="*70)
                    analyzer.analyze_emotion(duration=analysis_duration)
                    print("Waiting for next RFID scan...\n")
                
                elif "ACCESS_DENIED" in status:
                    print("\n" + "="*70)
                    print("❌ RFID CARD NOT AUTHORIZED")
                    print("="*70)
                    print("Access Denied\n")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  System interrupted by user")
    
    finally:
        print("\n🛑 Shutting down...")
        analyzer.stop_camera()
        rfid.disconnect()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print("✅ System closed")

if __name__ == "__main__":
    main()
