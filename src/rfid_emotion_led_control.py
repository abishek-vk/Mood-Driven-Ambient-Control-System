#!/usr/bin/env python
"""
RFID + FACIAL EMOTION DETECTION + LED MOOD CONTROL
Complete integration with mood-driven LED control

Flow:
1. Wait for RFID card scan
2. If authorized, open camera and detect face
3. Analyze emotion from face
4. Control LEDs based on detected mood
   - Positive mood (Happy, Surprise) → LED 1 blinks
   - Negative mood (Sad, Angry, Fear) → LED 2 blinks
   - Neutral → Both LEDs blink alternately
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

# Import custom modules
from emotion_detector import AdvancedEmotionDetector
from led_control import LEDController

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


class MoodDrivenEmotionAnalyzer:
    """Performs emotion analysis with mood-driven LED control"""
    def __init__(self, led_controller=None, use_simulation=False):
        print("Loading Face Detector (OpenCV)...")
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        print("Loading Emotion Detector...")
        self.emotion_detector = AdvancedEmotionDetector()
        
        # Initialize LED controller
        self.led_controller = led_controller or LEDController(serial_connection=None)
        self.use_simulation = use_simulation
        
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
    
    def analyze_emotion_with_led(self, duration=10, blink_frequency=2):
        """
        Analyze emotions and control LEDs based on mood
        
        Args:
            duration: Analysis duration in seconds
            blink_frequency: LED blink frequency (1-10 Hz)
        """
        if self.cap is None:
            print("Camera not available")
            return
        
        self.analyzing = True
        start_time = time.time()
        frame_count = 0
        emotions_detected = {}
        current_emotion = None
        current_confidence = 0
        
        print(f"\n{'='*60}")
        print(f"🎥 EMOTION ANALYSIS STARTED ({duration}s)")
        print(f"💡 LED CONTROL ACTIVE")
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
                        current_emotion = emotion
                        current_confidence = confidence
                        
                        if emotion not in emotions_detected:
                            emotions_detected[emotion] = 0
                        emotions_detected[emotion] += 1
                        
                        # Get color for emotion
                        color = self.get_emotion_color(emotion)
                        
                        # Draw on frame
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        label = f"{emotion}: {confidence*100:.0f}%"
                        cv2.putText(frame, label, (x, y-10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                        
                        # Control LEDs based on emotion (UPDATE EVERY FRAME)
                        self.led_controller.set_mood(emotion, confidence, blink_frequency)
            
            # Handle no faces - turn off LEDs
            if len(faces) == 0:
                self.led_controller.all_leds_off()
            
            # Show info panel on frame
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            
            # Display stats
            cv2.putText(frame, f"Faces: {len(faces)} | Time remaining: {remaining}s", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if current_emotion:
                mood_status = self.get_mood_status(current_emotion)
                cv2.putText(frame, f"Current Mood: {mood_status}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if current_emotion in ['happy', 'surprise']:
                    cv2.putText(frame, "LED 1 (Green) → ACTIVE", 
                               (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                elif current_emotion in ['sad', 'angry', 'fear', 'disgust']:
                    cv2.putText(frame, "LED 2 (Red) → ACTIVE", 
                               (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "LEDs → ALTERNATING", 
                               (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            cv2.imshow('Mood-Driven LED Control System', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.analyzing = False
        
        # Turn off LEDs after analysis
        self.led_controller.all_leds_off()
        
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
                mood = self.get_mood_status(emotion)
                print(f"  {emotion.upper():12} : {count:3} detections ({percentage:5.1f}%) → {mood}")
            
            dominant_emotion = max(emotions_detected, key=emotions_detected.get)
            print(f"\n✅ DOMINANT EMOTION: {dominant_emotion.upper()}")
            mood = self.get_mood_status(dominant_emotion)
            print(f"   MOOD: {mood}")
        else:
            print("❌ No emotions detected")
        
        print(f"{'='*60}\n")
    
    def get_emotion_color(self, emotion):
        """Get color for emotion"""
        colors = {
            'happy': (0, 255, 0),      # Green
            'sad': (255, 0, 0),        # Blue
            'angry': (0, 0, 255),      # Red
            'fear': (255, 0, 255),     # Magenta
            'neutral': (128, 128, 128),  # Gray
            'disgust': (0, 165, 255),  # Orange
            'surprise': (0, 255, 255)  # Yellow
        }
        return colors.get(emotion, (255, 255, 255))
    
    def get_mood_status(self, emotion):
        """Get mood status text"""
        if emotion in ['happy', 'surprise']:
            return "✨ POSITIVE"
        elif emotion in ['sad', 'angry', 'fear', 'disgust']:
            return "😟 NEGATIVE"
        else:
            return "😐 NEUTRAL"
    
    def stop_camera(self):
        """Stop camera"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


def main():
    print("\n" + "="*70)
    print("🎭 MOOD-DRIVEN AMBIENT CONTROL SYSTEM WITH LED 🎭")
    print("="*70)
    print("RFID Authentication + Face Detection + Emotion Recognition + LED Control")
    
    # Initialize Arduino listener
    print("\n[1/4] Initializing Arduino RFID Reader...")
    rfid = ArduinoRFIDListener()
    arduino_connected = rfid.connect()
    
    if not arduino_connected:
        print("\n⚠️  Arduino RFID reader not found")
        print("    Running in SIMULATION mode (no LED control)")
        use_simulation = True
    else:
        use_simulation = False
    
    # Initialize LED controller with Arduino connection
    print("\n[2/4] Initializing LED Controller...")
    led_controller = LEDController(serial_connection=rfid.ser if not use_simulation else None)
    
    # Initialize emotion analyzer with LED control
    print("\n[3/4] Initializing Emotion Analyzer...")
    analyzer = MoodDrivenEmotionAnalyzer(led_controller=led_controller, use_simulation=use_simulation)
    
    # Start camera
    print("\n[4/4] Starting Camera...")
    if not analyzer.start_camera():
        print("Cannot start camera")
        if rfid.ser:
            rfid.disconnect()
        return
    
    print("\n" + "="*70)
    print("✅ SYSTEM READY - WAITING FOR RFID SCAN")
    print("="*70)
    print("\n📌 System Flow:")
    print("  1️⃣  Scan your RFID card")
    print("  2️⃣  Face detection starts automatically")
    print("  3️⃣  Emotion is analyzed")
    print("  4️⃣  LEDs blink based on detected mood:")
    print("       🟢 LED 1 (Green) = POSITIVE mood (Happy, Surprise)")
    print("       🔴 LED 2 (Red)   = NEGATIVE mood (Sad, Angry, Fear)")
    print("       ↔️  BOTH          = NEUTRAL mood")
    print("  5️⃣  Results displayed after 10 seconds")
    print("\n⏹️  Press Ctrl+C to exit\n")
    
    analysis_duration = 10
    led_blink_frequency = 2  # Hz (1-10)
    
    try:
        while True:
            status = rfid.read_status() if not use_simulation else None
            
            if status:
                if "ACCESS_GRANTED" in status:
                    print("\n" + "="*70)
                    print("✅ RFID CARD AUTHORIZED - ACCESS GRANTED")
                    print("="*70)
                    analyzer.analyze_emotion_with_led(
                        duration=analysis_duration,
                        blink_frequency=led_blink_frequency
                    )
                    print("Waiting for next RFID scan...\n")
                
                elif "ACCESS_DENIED" in status:
                    print("\n" + "="*70)
                    print("❌ RFID CARD NOT AUTHORIZED - ACCESS DENIED")
                    print("="*70)
                    led_controller.all_leds_off()
                    print("Waiting for next RFID scan...\n")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  System interrupted by user")
    
    finally:
        print("\n🛑 Shutting down...")
        analyzer.stop_camera()
        led_controller.all_leds_off()
        if rfid.ser:
            rfid.disconnect()
        print("✅ System closed - All LEDs OFF")


if __name__ == "__main__":
    main()
