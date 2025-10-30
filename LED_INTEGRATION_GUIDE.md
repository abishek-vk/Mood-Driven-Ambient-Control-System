# Mood-Driven Ambient Control System - LED Integration Guide

## 🎯 Project Overview

A **mood-driven ambient control system** that uses:
- **RFID Authentication** - Scan card for access
- **Face Detection** - OpenCV for detecting faces
- **Emotion Recognition** - TensorFlow model to detect emotions
- **LED Ambient Control** - Different LEDs blink based on detected mood

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RFID CARD SCAN                           │
│              (Arduino via Serial Port)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │   ACCESS GRANTED?           │
         │   (Check RFID whitelist)    │
         └────────────┬────────────────┘
                      │
         ┌────────────▼────────────┐
         │  OPEN CAMERA            │
         │  & DETECT FACES         │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │  ANALYZE EMOTION        │
         │  (TensorFlow Model)     │
         └────────────┬────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
 HAPPY/          SAD/ANGRY/          NEUTRAL
SURPRISE           FEAR/DISGUST
    │                 │                 │
    ▼                 ▼                 ▼
 LED1            LED2               BOTH
 (Green)         (Red)          (Alternating)
 BLINKS          BLINKS           BLINKS
```

## 🔌 Hardware Connection

### Components Needed:
- Arduino (Uno/Nano)
- 2 x LEDs (any color - preferably Green and Red)
- 2 x 220Ω Resistors
- Jumper wires
- Breadboard

### Wiring Diagram:
```
Arduino Pin 10 ──┬── 220Ω Resistor ──► LED1 (Green/Positive) ──► GND
                 │
Arduino Pin 11 ──┬── 220Ω Resistor ──► LED2 (Red/Negative) ──► GND
                 │
Arduino GND ─────┴─ Common Ground
```

### Pin Configuration:
| Component | Arduino Pin | Purpose |
|-----------|------------|---------|
| LED 1 | 10 | Positive Mood (Happy, Surprise) |
| LED 2 | 11 | Negative Mood (Sad, Angry, Fear, Disgust) |
| GND | GND | Ground |

## 💻 Software Installation

### 1. Update requirements.txt
```bash
pip install -r requirements.txt
```

### 2. Upload Arduino Sketch
1. Open Arduino IDE
2. Go to: `File → Open`
3. Select: `arduino_sketch/mood_led_control.ino`
4. Click: `Upload` button
5. Verify the upload was successful

### 3. Python Modules

The system includes three new Python modules:

#### **led_control.py**
- Main LED controller module
- Handles communication with Arduino
- Maps emotions to LED states

```python
from led_control import LEDController

# Initialize with Arduino connection
led_controller = LEDController(serial_connection=arduino_serial)

# Set mood based on emotion
led_controller.set_mood('happy', confidence=0.95, blink_frequency=2)
```

#### **rfid_emotion_led_control.py**
- Main script that integrates everything
- RFID scanning → Face detection → Emotion recognition → LED control

```bash
python src/rfid_emotion_led_control.py
```

## 🎨 Mood-to-LED Mapping

| Emotion | Category | LED Status | Description |
|---------|----------|-----------|-------------|
| 😊 Happy | POSITIVE | LED 1 Blinking | Green - Positive mood |
| 😮 Surprise | POSITIVE | LED 1 Blinking | Green - Positive mood |
| 😢 Sad | NEGATIVE | LED 2 Blinking | Red - Negative mood |
| 😠 Angry | NEGATIVE | LED 2 Blinking | Red - Negative mood |
| 😨 Fear | NEGATIVE | LED 2 Blinking | Red - Negative mood |
| 🤢 Disgust | NEGATIVE | LED 2 Blinking | Red - Negative mood |
| 😐 Neutral | NEUTRAL | Both Alternating | Yellow - Neutral mood |

## ⚡ LED States

### Blink Frequency Modes
- **1 Hz**: Slow blink (1 blink per second)
- **2 Hz**: Normal blink (2 blinks per second) - Default
- **3+ Hz**: Fast blink

### Arduino Commands (Sent via Serial)
```
ALL_OFF              → Turn off both LEDs
PIN_10_ON            → Turn ON LED1 (solid)
PIN_10_OFF           → Turn OFF LED1
PIN_10_BLINK_2       → Blink LED1 at 2 Hz
PIN_11_ON            → Turn ON LED2 (solid)
PIN_11_OFF           → Turn OFF LED2
PIN_11_BLINK_2       → Blink LED2 at 2 Hz
BOTH_BLINK_ALT_1     → Both LEDs blink alternately at 1 Hz
```

## 🚀 Running the System

### Option 1: Full System (with RFID)
```bash
cd c:\Users\Abi Venkat\facial-recognition-system
python src/rfid_emotion_led_control.py
```

**Flow:**
1. System waits for RFID card scan
2. If authorized, camera opens
3. Faces are detected and emotions analyzed
4. LEDs blink based on emotion for 10 seconds
5. Results are displayed

### Option 2: Test LED Control (without RFID)
```bash
python src/led_control.py
```

**This tests:**
- LED controller initialization
- Emotion-to-mood mapping
- LED simulation (if no Arduino connected)
- All emotion types

### Option 3: Simple Camera + Emotion (no LEDs)
```bash
python src/main.py
```

## 🔧 Configuration

Edit `config.ini` to adjust:
- Face detection sensitivity
- Camera resolution
- Display settings

To adjust LED blink frequency, edit in `rfid_emotion_led_control.py`:
```python
led_blink_frequency = 2  # Change this value (1-10 Hz)
```

## 🐛 Troubleshooting

### LEDs Not Blinking
1. **Check Arduino Connection:**
   ```bash
   python
   import serial
   import serial.tools.list_ports
   for port in serial.tools.list_ports.comports():
       print(port.device, port.description)
   ```

2. **Verify Wiring:**
   - Check 220Ω resistors are connected
   - Check LED polarity (long leg to pin, short leg to GND)
   - Check GND connections

3. **Test Arduino Directly:**
   - Open Serial Monitor in Arduino IDE
   - Arduino should send "READY" message
   - Send commands manually: `PIN_10_BLINK_2`

### Emotion Detection Not Working
1. Check if camera is accessible
2. Verify face is clearly visible
3. Ensure lighting is adequate

### Python Serial Errors
```bash
pip install --upgrade pyserial
```

## 📊 Example Output

```
======================================================================
🎭 MOOD-DRIVEN AMBIENT CONTROL SYSTEM WITH LED 🎭
======================================================================

[1/4] Initializing Arduino RFID Reader...
Available COM ports:
  - COM3: Arduino Uno

✓ Found Arduino-like device at: COM3
Connecting to Arduino on COM3...
✅ Connected to Arduino on COM3

[2/4] Initializing LED Controller...

[3/4] Initializing Emotion Analyzer...
Loading Emotion Detector...

[4/4] Starting Camera...
✅ Camera started

======================================================================
✅ SYSTEM READY - WAITING FOR RFID SCAN
======================================================================

📌 System Flow:
  1️⃣  Scan your RFID card
  2️⃣  Face detection starts automatically
  3️⃣  Emotion is analyzed
  4️⃣  LEDs blink based on detected mood:
       🟢 LED 1 (Green) = POSITIVE mood (Happy, Surprise)
       🔴 LED 2 (Red)   = NEGATIVE mood (Sad, Angry, Fear)
       ↔️  BOTH          = NEUTRAL mood
  5️⃣  Results displayed after 10 seconds

⏹️  Press Ctrl+C to exit

```

## 🎓 How It Works - Detailed Flow

### 1. RFID Authentication
- Arduino listens on serial port for RFID scans
- Compares card ID with whitelist
- Sends "ACCESS_GRANTED" or "ACCESS_DENIED"

### 2. Face Detection
- OpenCV's `haarcascade_frontalface_default.xml` detects faces
- Multiple faces can be detected simultaneously
- Face region is extracted for emotion analysis

### 3. Emotion Detection
- TensorFlow model analyzes face image
- Returns emotion class: ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
- Also provides confidence score

### 4. LED Control
- Emotion is mapped to mood category:
  - **POSITIVE**: happy, surprise → LED1 blinks
  - **NEGATIVE**: sad, angry, fear, disgust → LED2 blinks
  - **NEUTRAL**: neutral → Both blink alternately

- Command is sent to Arduino via serial port
- Arduino controls GPIO pins 10 and 11

## 📈 Enhancement Ideas

1. **Add More LEDs**
   - One LED per emotion (7 total)
   - RGB LED with color coding

2. **Sound Integration**
   - Play different tones based on mood
   - Combine with LED for more immersion

3. **Data Logging**
   - Log emotions and timestamps
   - Generate mood reports

4. **Web Dashboard**
   - Real-time monitoring
   - Historical mood data

5. **Advanced Animations**
   - Pulse effect instead of simple blink
   - Fade in/out effects
   - Multiple color combinations

## 📝 Files Overview

```
facial-recognition-system/
├── src/
│   ├── led_control.py                  # 🆕 LED Controller Module
│   ├── rfid_emotion_led_control.py     # 🆕 Main system with LED integration
│   ├── emotion_detector.py             # Emotion recognition model
│   ├── face_detector_advanced.py       # Face detection
│   └── ...
├── arduino_sketch/
│   └── mood_led_control.ino            # 🆕 Arduino firmware
└── README.md
```

## ✅ Testing Checklist

- [ ] Arduino sketch uploaded successfully
- [ ] LEDs light up when pins are HIGH
- [ ] Serial communication works (READY message received)
- [ ] Python modules import without errors
- [ ] Camera opens and displays video
- [ ] Faces are detected in camera feed
- [ ] Emotions are recognized
- [ ] LEDs respond to different emotions
- [ ] Full workflow: RFID → Face → Emotion → LED

## 🎬 Next Steps

1. **Connect Hardware**
   - Wire LEDs to Arduino pins 10 and 11
   - Connect Arduino via USB

2. **Upload Code**
   - Upload Arduino sketch
   - Install Python dependencies

3. **Test Components**
   - Test Arduino and LEDs
   - Test camera and emotion detection
   - Test full workflow

4. **Run System**
   - Execute `rfid_emotion_led_control.py`
   - Scan RFID card
   - See LEDs blink based on your emotion!

---

**Happy Ambient Control! 🎉**
