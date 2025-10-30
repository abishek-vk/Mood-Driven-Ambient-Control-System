# 🎭 MOOD-DRIVEN AMBIENT CONTROL SYSTEM - README

## 📌 Project Overview

This is a **complete mood-driven ambient control system** that combines:
- 🔐 RFID Authentication
- 👤 Face Detection  
- 🧠 Emotion Recognition (AI/ML)
- 💡 LED Ambient Control

**When you scan an RFID card, if authorized:**
1. Camera opens
2. Face is detected
3. Emotion is recognized (Happy, Sad, Angry, etc.)
4. **LEDs blink based on detected mood!**

## 🎨 LED Behavior

| Emotion | Mood | LED Status |
|---------|------|-----------|
| 😊 Happy | POSITIVE | 🟢 LED1 Blinks |
| 😮 Surprise | POSITIVE | 🟢 LED1 Blinks |
| 😢 Sad | NEGATIVE | 🔴 LED2 Blinks |
| 😠 Angry | NEGATIVE | 🔴 LED2 Blinks |
| 😨 Fear | NEGATIVE | 🔴 LED2 Blinks |
| 🤢 Disgust | NEGATIVE | 🔴 LED2 Blinks |
| 😐 Neutral | NEUTRAL | ↔️ Both Blink Alternately |

## ⚡ Quick Start (5 minutes)

### Hardware
```
Arduino Pin 10 ──[220Ω]──► LED1 (Green) ──► GND
Arduino Pin 11 ──[220Ω]──► LED2 (Red)   ──► GND
```

### Software
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Upload Arduino sketch
# Open Arduino IDE → File → Open → arduino_sketch/mood_led_control.ino → Upload

# 3. Run the system
python src/rfid_emotion_led_control.py
```

## 📚 Documentation

### 🚀 **Get Started** (Choose One)
- **[LED_QUICK_START.md](LED_QUICK_START.md)** - 5-minute setup guide ⭐ START HERE
- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Complete checklist

### 📖 **Detailed Guides**
- **[LED_INTEGRATION_GUIDE.md](LED_INTEGRATION_GUIDE.md)** - Full system documentation
- **[CIRCUIT_WIRING_GUIDE.md](CIRCUIT_WIRING_GUIDE.md)** - Hardware wiring instructions
- **[ARDUINO_COMMANDS_REFERENCE.md](ARDUINO_COMMANDS_REFERENCE.md)** - Serial commands
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Complete overview

### 🆘 **Help**
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues & solutions
- **[PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md)** - Performance optimization

## 🆕 New Files Created

### Python Modules
```
src/led_control.py                 - LED Controller Module
src/rfid_emotion_led_control.py    - Main System (RFID+Face+Emotion+LED)
```

### Arduino
```
arduino_sketch/mood_led_control.ino - Arduino Firmware
```

### Documentation
```
LED_QUICK_START.md
LED_INTEGRATION_GUIDE.md
CIRCUIT_WIRING_GUIDE.md
ARDUINO_COMMANDS_REFERENCE.md
IMPLEMENTATION_SUMMARY.md
SETUP_CHECKLIST.md
```

### Testing
```
test_system.py - Comprehensive system diagnostics
```

## 🚀 Running the System

### Option 1: Full System (Recommended)
```bash
python src/rfid_emotion_led_control.py
```
Complete workflow: RFID → Face Detection → Emotion Recognition → LED Control

### Option 2: Test LED Module Only
```bash
python src/led_control.py
```
Simulates emotion-to-LED mapping (no hardware needed)

### Option 3: Camera & Emotion Only
```bash
python src/main.py
```
Face detection and emotion recognition (no RFID or LEDs)

### Option 4: Diagnostics
```bash
python test_system.py
```
Tests all components and identifies issues

## 🔧 Configuration

Edit `src/rfid_emotion_led_control.py`:

```python
# Adjust LED blink speed (1-10 Hz)
led_blink_frequency = 2

# Adjust analysis duration (seconds)
analysis_duration = 10
```

## 📊 System Architecture

```
RFID Card Scan
    ↓
Access Check
    ├─ DENIED → LED OFF
    └─ GRANTED ↓
    Open Camera
    ↓
    Face Detection
    ↓
    Emotion Analysis
    ├─ POSITIVE → 🟢 LED1 BLINKS
    ├─ NEGATIVE → 🔴 LED2 BLINKS
    └─ NEUTRAL → ↔️ BOTH BLINK
    ↓
    Display Results
```

## 🎛️ LED Control Commands

The system sends these commands to Arduino:

```
ALL_OFF              → Turn off both LEDs
PIN_10_ON            → LED1 ON (solid)
PIN_10_OFF           → LED1 OFF
PIN_10_BLINK_2       → LED1 BLINK at 2 Hz
PIN_11_ON            → LED2 ON (solid)
PIN_11_OFF           → LED2 OFF
PIN_11_BLINK_2       → LED2 BLINK at 2 Hz
BOTH_BLINK_ALT_1     → Both LEDs blink alternately
```

## ✨ Features

✅ RFID authentication  
✅ Real-time face detection  
✅ 7-emotion recognition (angry, disgust, fear, happy, sad, surprise, neutral)  
✅ **Mood-driven LED control** ✨  
✅ Configurable blink frequency (1-10 Hz)  
✅ No Arduino simulation mode  
✅ Comprehensive documentation  
✅ Automated diagnostics  

## 🔌 Hardware Requirements

### Components
- Arduino (Uno, Nano, or compatible)
- 2 × LEDs (any color, preferably green & red)
- 2 × 220Ω resistors
- Breadboard & jumper wires
- USB cable
- Webcam

### Software
- Python 3.7+
- Arduino IDE
- Dependencies: opencv-python, tensorflow, numpy, pyserial

## 📈 Emotion Recognition

The system recognizes 7 emotions:

| Emotion | Category |
|---------|----------|
| Happy ✨ | Positive |
| Surprise 😮 | Positive |
| Sad 😢 | Negative |
| Angry 😠 | Negative |
| Fear 😨 | Negative |
| Disgust 🤢 | Negative |
| Neutral 😐 | Neutral |

## 🧪 Testing

Verify everything works:

```bash
# Run diagnostics
python test_system.py

# Test LED module (no hardware)
python src/led_control.py

# Full system test (with RFID if available)
python src/rfid_emotion_led_control.py
```

## 🐛 Troubleshooting

### LEDs Not Blinking?
1. Check Arduino connection
2. Verify LED wiring (long leg → pin, short leg → GND)
3. Test with Arduino Serial Monitor: send `PIN_10_BLINK_2`
4. Run `python test_system.py` to diagnose

### Face Not Detected?
- Ensure good lighting
- Face should be 30-100cm from camera
- Face should be clearly visible

### Arduino Not Found?
- Check USB connection
- Install CH340 driver for clone boards
- Run `python test_system.py`

See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for more help.

## 📞 Need Help?

1. **Quick help?** Read [LED_QUICK_START.md](LED_QUICK_START.md)
2. **Setup issues?** Follow [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
3. **Wiring problems?** Check [CIRCUIT_WIRING_GUIDE.md](CIRCUIT_WIRING_GUIDE.md)
4. **Arduino commands?** See [ARDUINO_COMMANDS_REFERENCE.md](ARDUINO_COMMANDS_REFERENCE.md)
5. **Errors?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 📁 Project Structure

```
facial-recognition-system/
├── src/
│   ├── led_control.py                 # 🆕 LED Controller
│   ├── rfid_emotion_led_control.py    # 🆕 Main System
│   ├── emotion_detector.py            # Emotion model
│   ├── face_detector_advanced.py      # Face detection
│   ├── main.py                        # Camera + emotion
│   └── ...
│
├── arduino_sketch/
│   └── mood_led_control.ino           # 🆕 Arduino Code
│
├── LED_QUICK_START.md                 # 🆕 Quick guide
├── LED_INTEGRATION_GUIDE.md           # 🆕 Full docs
├── CIRCUIT_WIRING_GUIDE.md            # 🆕 Hardware guide
├── ARDUINO_COMMANDS_REFERENCE.md      # 🆕 Command ref
├── IMPLEMENTATION_SUMMARY.md          # 🆕 Summary
├── SETUP_CHECKLIST.md                 # 🆕 Checklist
├── test_system.py                     # 🆕 Tests
│
├── config.ini
├── requirements.txt
├── README.md
└── TROUBLESHOOTING.md
```

## 🎯 Quick Reference

### Run Commands
```bash
# Full system
python src/rfid_emotion_led_control.py

# LED test (no hardware)
python src/led_control.py

# Diagnostics
python test_system.py

# Simple camera + emotion
python src/main.py
```

### Arduino Setup
```
1. Connect hardware (LEDs to pins 10 & 11)
2. Open Arduino IDE
3. File → Open → arduino_sketch/mood_led_control.ino
4. Select board: Arduino Uno
5. Click Upload
```

### LED Behavior
```
Happy/Surprise    → 🟢 LED1 Blinks
Sad/Angry/Fear    → 🔴 LED2 Blinks
Neutral           → ↔️ Both Blink
```

## 🎉 You're Ready!

Everything is set up and ready to use!

1. **Read** [LED_QUICK_START.md](LED_QUICK_START.md) (5 min)
2. **Connect** hardware (5 min)
3. **Upload** Arduino sketch (2 min)
4. **Run** `python src/rfid_emotion_led_control.py`
5. **Enjoy!** 🎭✨

---

## 📝 License

See LICENSE file for details.

## 👤 Author

Created for mood-driven ambient control project.

---

**Your system is now ready to light up based on emotions! 💚❤️✨**

For questions or issues, refer to the documentation files listed above.
