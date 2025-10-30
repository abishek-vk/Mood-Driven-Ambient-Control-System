#!/usr/bin/env python
"""
LED Control Module for Mood-Driven Ambient Control System
Controls two LEDs based on detected emotion/mood
- LED 1 (Positive): Happy, Surprise (Green pin)
- LED 2 (Negative): Sad, Angry, Fear, Disgust (Red pin)
- Neutral: Alternating or both OFF
"""

import serial
import time
from enum import Enum
import threading

class MoodCategory(Enum):
    """Emotion to Mood mapping"""
    POSITIVE = "positive"      # Happy, Surprise
    NEGATIVE = "negative"      # Sad, Angry, Fear, Disgust
    NEUTRAL = "neutral"        # Neutral


class LEDController:
    """
    Controls two LEDs connected to Arduino based on emotion detection
    """
    
    def __init__(self, serial_connection=None, 
                 led_positive_pin=10,  # Arduino pin for positive mood LED
                 led_negative_pin=11):  # Arduino pin for negative mood LED
        """
        Initialize LED Controller
        
        Args:
            serial_connection: Serial object connected to Arduino (can be None for simulation)
            led_positive_pin: Arduino pin for positive mood LED (default: 10)
            led_negative_pin: Arduino pin for negative mood LED (default: 11)
        """
        self.ser = serial_connection
        self.led_positive_pin = led_positive_pin
        self.led_negative_pin = led_negative_pin
        self.current_mood = None
        self.is_blinking = False
        self.blink_thread = None
        self.emotion_to_mood_map = {
            'happy': MoodCategory.POSITIVE,
            'surprise': MoodCategory.POSITIVE,
            'sad': MoodCategory.NEGATIVE,
            'angry': MoodCategory.NEGATIVE,
            'fear': MoodCategory.NEGATIVE,
            'disgust': MoodCategory.NEGATIVE,
            'neutral': MoodCategory.NEUTRAL
        }
    
    def emotion_to_mood(self, emotion):
        """
        Convert emotion string to mood category
        
        Args:
            emotion (str): Emotion name ('happy', 'sad', etc.)
            
        Returns:
            MoodCategory: Corresponding mood category
        """
        emotion_lower = emotion.lower().strip()
        return self.emotion_to_mood_map.get(emotion_lower, MoodCategory.NEUTRAL)
    
    def send_command_to_arduino(self, command):
        """
        Send command to Arduino via serial connection
        
        Args:
            command (str): Command to send (e.g., "LED1_ON", "LED2_BLINK")
        """
        if self.ser is None or not self.ser.is_open:
            print(f"[LED] Simulation: {command}")
            return
        
        try:
            self.ser.write((command + '\n').encode())
            print(f"[LED] Sent to Arduino: {command}")
        except Exception as e:
            print(f"[LED] Error sending command: {e}")
    
    def all_leds_off(self):
        """Turn off both LEDs"""
        self.is_blinking = False
        self.send_command_to_arduino("ALL_OFF")
        print("[LED] All LEDs OFF")
    
    def led_positive_on(self):
        """Turn ON positive mood LED (solid)"""
        self.is_blinking = False
        self.send_command_to_arduino(f"PIN_{self.led_positive_pin}_ON")
        print(f"[LED] Positive LED (Pin {self.led_positive_pin}) ON")
    
    def led_negative_on(self):
        """Turn ON negative mood LED (solid)"""
        self.is_blinking = False
        self.send_command_to_arduino(f"PIN_{self.led_negative_pin}_ON")
        print(f"[LED] Negative LED (Pin {self.led_negative_pin}) ON")
    
    def led_positive_blink(self, frequency=2):
        """
        Blink positive mood LED
        
        Args:
            frequency (int): Blinks per second (1-10)
        """
        self.is_blinking = True
        self.send_command_to_arduino(f"PIN_{self.led_positive_pin}_BLINK_{frequency}")
        print(f"[LED] Positive LED (Pin {self.led_positive_pin}) BLINKING at {frequency} Hz")
    
    def led_negative_blink(self, frequency=2):
        """
        Blink negative mood LED
        
        Args:
            frequency (int): Blinks per second (1-10)
        """
        self.is_blinking = True
        self.send_command_to_arduino(f"PIN_{self.led_negative_pin}_BLINK_{frequency}")
        print(f"[LED] Negative LED (Pin {self.led_negative_pin}) BLINKING at {frequency} Hz")
    
    def led_both_blink_alternating(self, frequency=1):
        """
        Both LEDs blink alternately (for neutral mood)
        
        Args:
            frequency (int): Blinks per second
        """
        self.is_blinking = True
        self.send_command_to_arduino(f"BOTH_BLINK_ALT_{frequency}")
        print(f"[LED] Both LEDs BLINKING alternately at {frequency} Hz")
    
    def set_mood(self, emotion, confidence=None, blink_frequency=2):
        """
        Set LED state based on detected emotion
        
        Args:
            emotion (str): Detected emotion ('happy', 'sad', etc.)
            confidence (float): Confidence score (0-1) - optional
            blink_frequency (int): How fast to blink (1-10)
        """
        mood = self.emotion_to_mood(emotion)
        self.current_mood = mood
        
        if confidence:
            print(f"[MOOD] {emotion.upper()} ({confidence*100:.1f}%) → {mood.value}")
        else:
            print(f"[MOOD] {emotion.upper()} → {mood.value}")
        
        # Control LEDs based on mood
        if mood == MoodCategory.POSITIVE:
            self.led_positive_blink(blink_frequency)
        elif mood == MoodCategory.NEGATIVE:
            self.led_negative_blink(blink_frequency)
        else:  # NEUTRAL
            self.led_both_blink_alternating(frequency=1)
    
    def manual_led_control(self, led_number, state, frequency=2):
        """
        Manually control LEDs (for testing)
        
        Args:
            led_number (int): 1 or 2
            state (str): 'ON', 'OFF', or 'BLINK'
            frequency (int): Blink frequency if state is 'BLINK'
        """
        if led_number == 1:
            pin = self.led_positive_pin
        elif led_number == 2:
            pin = self.led_negative_pin
        else:
            print(f"[LED] Invalid LED number: {led_number}")
            return
        
        if state == 'ON':
            self.send_command_to_arduino(f"PIN_{pin}_ON")
            print(f"[LED] LED {led_number} (Pin {pin}) ON")
        elif state == 'OFF':
            self.send_command_to_arduino(f"PIN_{pin}_OFF")
            print(f"[LED] LED {led_number} (Pin {pin}) OFF")
        elif state == 'BLINK':
            self.send_command_to_arduino(f"PIN_{pin}_BLINK_{frequency}")
            print(f"[LED] LED {led_number} (Pin {pin}) BLINKING at {frequency} Hz")


class LEDSimulator:
    """
    Simulates LED behavior without Arduino for testing
    """
    def __init__(self):
        self.led1_state = False
        self.led2_state = False
        self.led1_blinking = False
        self.led2_blinking = False
        print("[LED Simulator] Ready (no Arduino needed)")
    
    def simulate_emotion(self, emotion, confidence):
        """Simulate LED response to emotion"""
        print(f"\n{'='*50}")
        print(f"  🎭 EMOTION: {emotion.upper()}")
        print(f"  📊 CONFIDENCE: {confidence*100:.1f}%")
        print(f"{'='*50}")
        
        if emotion in ['happy', 'surprise']:
            print("  ✨ POSITIVE MOOD DETECTED")
            print("  🟢 LED 1 (Positive) → BLINKING")
            print("  ⚫ LED 2 (Negative) → OFF")
        elif emotion in ['sad', 'angry', 'fear', 'disgust']:
            print("  😟 NEGATIVE MOOD DETECTED")
            print("  ⚫ LED 1 (Positive) → OFF")
            print("  🔴 LED 2 (Negative) → BLINKING")
        else:  # neutral
            print("  😐 NEUTRAL MOOD DETECTED")
            print("  🟢 LED 1 (Positive) ↔ BLINKING ALTERNATELY")
            print("  🔴 LED 2 (Negative) ↔ BLINKING ALTERNATELY")
        print()


if __name__ == "__main__":
    """Test LED Controller"""
    print("\n" + "="*60)
    print("LED CONTROL MODULE - TEST MODE")
    print("="*60 + "\n")
    
    # Test with simulator (no Arduino)
    led_controller = LEDController(serial_connection=None)
    simulator = LEDSimulator()
    
    # Test different emotions
    test_emotions = [
        ('happy', 0.95),
        ('sad', 0.87),
        ('angry', 0.92),
        ('neutral', 0.78),
        ('surprise', 0.85),
        ('fear', 0.88)
    ]
    
    for emotion, confidence in test_emotions:
        led_controller.set_mood(emotion, confidence)
        simulator.simulate_emotion(emotion, confidence)
        time.sleep(1)
    
    # Test manual control
    print("\n" + "="*50)
    print("MANUAL LED CONTROL TEST")
    print("="*50 + "\n")
    
    led_controller.manual_led_control(1, 'ON')
    time.sleep(1)
    led_controller.manual_led_control(2, 'BLINK', frequency=3)
    time.sleep(1)
    led_controller.all_leds_off()
    
    print("\n✅ LED Control Module Test Complete")
