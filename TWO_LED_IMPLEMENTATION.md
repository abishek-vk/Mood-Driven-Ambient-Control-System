# 🟢🔴 Two LED Implementation Guide

## ✅ Implementation Complete!

Your Mood-Driven Ambient Control System now features **two independent LEDs** to indicate emotional states:

### LED Configuration

| LED | Color | Emotion | Pin | Status |
|-----|-------|---------|-----|--------|
| **LED1** | 🟢 **Green** | Positive (Happy, Surprise) | **Pin 10** | ✅ Active |
| **LED2** | 🔴 **Red** | Negative (Sad, Angry, Fear, Disgust) | **Pin 11** | ✅ Active |
| **Both** | 🟢🔴 **Alternating** | Neutral | Both Pins | ✅ Active |

---

## 🔌 Circuit Connections

### Physical Wiring (Breadboard)

```
┌─────────────────────────────────────────────────────┐
│                  Arduino UNO                        │
│                                                     │
│  GND  ─────────────────┐                            │
│                        │                            │
│  Pin 10 ──[220Ω]──┬──> 🟢 LED1 (Green)             │
│                  └────────> GND                     │
│                                                     │
│  Pin 11 ──[220Ω]──┬──> 🔴 LED2 (Red)               │
│                  └────────> GND                     │
└─────────────────────────────────────────────────────┘
```

### Step-by-Step Wiring Instructions

#### **Components Needed:**
- ✅ 1× Arduino Uno
- ✅ 1× Green LED (common cathode)
- ✅ 1× Red LED (common cathode)
- ✅ 2× 220Ω Resistors
- ✅ 1× Breadboard
- ✅ 4× Jumper wires

#### **Step 1: Set up LED1 (Green) on Pin 10**

```
1. Insert Green LED into breadboard:
   - Longer leg (Anode, +) → column A
   - Shorter leg (Cathode, -) → GND row

2. Connect 220Ω resistor:
   - Start from Arduino Pin 10
   - End at green LED's longer leg (Anode)

3. Connect ground:
   - Green LED's shorter leg → GND row (blue -)
   - Arduino GND → same GND row
```

**Wiring Summary for LED1:**
```
Arduino Pin 10 ──[220Ω]──> Green LED (+) ──> GND
```

#### **Step 2: Set up LED2 (Red) on Pin 11**

```
1. Insert Red LED into breadboard (next to green LED):
   - Longer leg (Anode, +) → column B
   - Shorter leg (Cathode, -) → GND row

2. Connect 220Ω resistor:
   - Start from Arduino Pin 11
   - End at red LED's longer leg (Anode)

3. Connect ground:
   - Red LED's shorter leg → GND row (blue -)
```

**Wiring Summary for LED2:**
```
Arduino Pin 11 ──[220Ω]──> Red LED (+) ──> GND
```

#### **Step 3: Connect Ground Reference**

```
Connect Arduino GND pin to the negative (blue -) row on breadboard
This ensures common ground for all components
```

---

## 💻 Python Implementation

### Emotion to LED Mapping

Your system automatically maps emotions to LED states:

```python
# Positive Emotions (Green LED - PIN 10)
🟢 HAPPY    → LED 1 ON / BLINKING
🟢 SURPRISE → LED 1 ON / BLINKING

# Negative Emotions (Red LED - PIN 11)
🔴 SAD     → LED 2 ON / BLINKING
🔴 ANGRY   → LED 2 ON / BLINKING
🔴 FEAR    → LED 2 ON / BLINKING
🔴 DISGUST → LED 2 ON / BLINKING

# Neutral (Both Alternating)
🟢🔴 NEUTRAL → Both blink alternately
```

### Python Code Structure

#### **src/led_control.py**

The `LEDController` class manages both LEDs:

```python
class LEDController:
    def __init__(self, serial_connection=None, 
                 led_positive_pin=10,      # Green LED
                 led_negative_pin=11):     # Red LED
        self.ser = serial_connection
        self.led_positive_pin = 10   # Pin 10 = Green
        self.led_negative_pin = 11   # Pin 11 = Red
    
    # Available methods:
    def led_positive_on()        # Turn ON green LED
    def led_negative_on()        # Turn ON red LED
    def led_positive_blink()     # Blink green LED
    def led_negative_blink()     # Blink red LED
    def led_both_blink_alternating()  # Both blink opposite
    def set_mood(emotion)        # Automatic LED control
    def all_leds_off()           # Turn off both LEDs
```

---

## 📡 Arduino Communication

### Serial Commands

The Python code sends these commands to Arduino:

| Command | Action |
|---------|--------|
| `PIN_10_ON` | Green LED ON (solid) |
| `PIN_10_OFF` | Green LED OFF |
| `PIN_10_BLINK_2` | Green LED blink at 2 Hz |
| `PIN_11_ON` | Red LED ON (solid) |
| `PIN_11_OFF` | Red LED OFF |
| `PIN_11_BLINK_2` | Red LED blink at 2 Hz |
| `BOTH_BLINK_ALT_1` | Both LEDs blink alternately at 1 Hz |
| `ALL_OFF` | Turn off both LEDs |

### Arduino Sketch (mood_led_control.ino)

```cpp
#define LED1_PIN 10  // Green - Positive Mood
#define LED2_PIN 11  // Red - Negative Mood

// Processes commands from Python
void processCommand(String command) {
    if (command == "PIN_10_ON")
        setLEDState(&led1, true, false, 0);
    else if (command == "PIN_11_ON")
        setLEDState(&led2, true, false, 0);
    else if (command == "BOTH_BLINK_ALT_1")
        bothLEDsAlternating();
    // ... etc
}
```

---

## 🎯 Usage Examples

### Example 1: Basic LED Control

```python
from src.led_control import LEDController
import serial

# Initialize with Arduino connection
ser = serial.Serial('COM3', 9600)  # Adjust COM port
led = LEDController(serial_connection=ser)

# Automatic emotion-based control
led.set_mood('happy')      # 🟢 Green LED blinks
led.set_mood('sad')        # 🔴 Red LED blinks
led.set_mood('neutral')    # 🟢🔴 Both blink alternately
```

### Example 2: Manual LED Control

```python
# Manual control
led.led_positive_on()                    # Green ON
led.led_negative_blink(frequency=3)      # Red blink at 3 Hz
led.all_leds_off()                       # Both OFF
```

### Example 3: In Real-time Emotion Detection

```python
from src.emotion_detector import AdvancedEmotionDetector
from src.led_control import LEDController
import serial

emotion_detector = AdvancedEmotionDetector()
ser = serial.Serial('COM3', 9600)
led_controller = LEDController(serial_connection=ser)

# In your main loop:
emotion, confidence = emotion_detector.predict_emotion(face_image)
led_controller.set_mood(emotion, confidence, blink_frequency=2)
```

---

## 🧪 Testing the Setup

### Test 1: Hardware Connection Test

```bash
python test_arduino.py
```

This verifies Arduino communication.

### Test 2: LED Control Test

```bash
python -c "
from src.led_control import LEDController
led = LEDController()  # Simulation mode (no Arduino)

# Test emotions
led.set_mood('happy')
time.sleep(1)
led.set_mood('sad')
time.sleep(1)
led.set_mood('neutral')
"
```

### Test 3: Full System Test

```bash
python test_mood_led.py
```

This tests emotion detection + LED control together.

---

## 📊 Pin Configuration Summary

```
Arduino Pin Layout:
┌─────────────────────┐
│  Arduino UNO        │
│                     │
│  Pin 10 ─→ 🟢 Green │
│  Pin 11 ─→ 🔴 Red   │
│  GND   ─→ Ground    │
│                     │
└─────────────────────┘

Breadboard Layout:
┌──────────────────────────┐
│  Power Supply:           │
│  + (Red rail)   - (Blue) │
├──────────────────────────┤
│                          │
│  [220Ω] ─→ 🟢 ─→ GND    │ (Row A)
│                          │
│  [220Ω] ─→ 🔴 ─→ GND    │ (Row B)
│                          │
└──────────────────────────┘
```

---

## 🎨 LED Behavior Summary

| Emotion | LED1 (Green) | LED2 (Red) | Behavior |
|---------|--------------|-----------|----------|
| Happy | ✅ BLINK | ❌ OFF | Rapid blinking green = joy detected |
| Surprise | ✅ BLINK | ❌ OFF | Positive emotion |
| Sad | ❌ OFF | ✅ BLINK | Red LED shows negative mood |
| Angry | ❌ OFF | ✅ BLINK | Red LED shows anger |
| Fear | ❌ OFF | ✅ BLINK | Red LED shows distress |
| Disgust | ❌ OFF | ✅ BLINK | Red LED shows disgust |
| Neutral | ✅ BLINK | ✅ BLINK | Both blink alternately (indecision) |

---

## 🔧 Troubleshooting

### LED Not Lighting Up

1. **Check polarity:**
   - Longer leg = Anode (+) connects to resistor from Arduino pin
   - Shorter leg = Cathode (-) connects to GND

2. **Check connections:**
   - Verify resistor value (should be 220Ω or 330Ω)
   - Check for loose jumper wires
   - Verify GND connection

3. **Check Arduino code:**
   - Upload `mood_led_control.ino` to Arduino
   - Open Serial Monitor to see debug output

### Only One LED Works

- Check that both pins are configured in Arduino
- Verify pin assignments: Pin 10 (Green), Pin 11 (Red)
- Test pins independently with simple `digitalWrite()` commands

### LEDs Flickering

- Ensure stable power supply
- Check for loose connections
- Reduce blink frequency in code if needed

---

## 📝 File Locations

```
✅ Arduino Sketch: arduino_sketch/mood_led_control.ino
✅ Python LED Control: src/led_control.py
✅ Python Emotion Detection: src/emotion_detector.py
✅ Integration Script: src/main.py
✅ Wiring Guide: CIRCUIT_WIRING_GUIDE.md
✅ LED Guide: LED_SYSTEM_README.md
```

---

## ✨ Ready to Use!

Your two-LED system is fully implemented and ready for:
- 🎭 Real-time emotion detection
- 🟢 Positive mood indication (Green)
- 🔴 Negative mood indication (Red)
- 🎯 Ambient control based on emotional state

Happy coding! 🚀
