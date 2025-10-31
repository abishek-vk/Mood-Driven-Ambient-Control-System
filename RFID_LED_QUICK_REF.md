# ⚡ RFID + LED Emotion Control - Quick Reference

## 🎯 What This System Does

```
1. Scan RFID Card ──→ Validates Access
2. If Authorized ──→ Starts Emotion Detection
3. Detects Emotion ──→ Happy OR Angry
4. Controls LEDs ──→ 🟢 Green OR 🔴 Red Blinks
5. Plays Music ──→ Mood-appropriate songs
```

---

## 🔌 Hardware Wiring - 30 Seconds

```
Arduino Pins:
  Pin 2  ──[220Ω]──→ 🟢 GREEN LED
  Pin 3  ──[220Ω]──→ 🔴 RED LED
  GND    ────────→ Both LEDs (common)

LED Orientation:
  Long leg (Anode +)  → Resistor → Arduino Pin
  Short leg (Cathode -) → GND
```

---

## 💻 Python Commands

```python
# When emotion detected:
send_led_command("LED_GREEN_BLINK")  # Happy detected
send_led_command("LED_RED_BLINK")    # Angry detected
send_led_command("LED_OFF")          # Other emotion
```

---

## 📡 Arduino Serial Messages

**From Arduino to Python:**
```
ACCESS_GRANTED   ← RFID card authorized
ACCESS_DENIED    ← RFID card rejected
```

**From Python to Arduino:**
```
LED_GREEN_BLINK  → Turn on green LED
LED_RED_BLINK    → Turn on red LED
LED_OFF          → Turn off both LEDs
```

---

## ⚡ LED Behavior

| Emotion | LED | Pattern |
|---------|-----|---------|
| 😊 Happy | 🟢 Green | Blink 1 Hz (500ms) |
| 😠 Angry | 🔴 Red | Blink 1 Hz (500ms) |
| Other | ❌ Off | No blink |

---

## 🚀 Quick Start (3 Steps)

### Step 1: Wire LEDs
```
Pin 2 → [220Ω] → Green LED → GND
Pin 3 → [220Ω] → Red LED → GND
```

### Step 2: Upload Arduino Code
```
File → Open → rfid_led_control.ino
Select Board: Arduino UNO
Click Upload
```

### Step 3: Run Python
```bash
python src/rfid_emotion_lite.py
```

---

## ✅ Testing

### Test 1: Check Connection
```bash
# Should print "Connected"
python -c "import serial; s = serial.Serial('COM3', 9600); print('Connected')"
```

### Test 2: Manual LED Test
```cpp
// In Arduino Serial Monitor, send:
LED_GREEN_BLINK
// Green LED should blink

LED_RED_BLINK
// Red LED should blink

LED_OFF
// Both LEDs should turn off
```

### Test 3: Full System
```bash
python src/rfid_emotion_lite.py
# Then scan RFID card and make expressions
```

---

## 🔧 Pin Reference

```
Arduino Pin 2  → Green LED (Pin D2)
Arduino Pin 3  → Red LED (Pin D3)
Arduino GND    → Common ground

Old Pins (Still Used):
  Pin 10  → RFID SS (Chip Select)
  Pin 9   → RFID RST (Reset)
  Pin 7   → Buzzer
  A4/A5   → LCD I2C
```

---

## 📊 LED Blinking Speed

**Current Setting:** 500ms intervals = 1 Hz (blinks twice per second)

**To Change Speed** (in Arduino):
```cpp
const int BLINK_INTERVAL = 500;  // milliseconds

// Faster:
const int BLINK_INTERVAL = 250;  // 2 Hz (4 blinks/sec)

// Slower:
const int BLINK_INTERVAL = 1000; // 0.5 Hz (1 blink/2 sec)
```

---

## 🎯 Serial Communication Timing

```
Timeline:
0ms    ┌─ RFID scan detected
       │
100ms  ├─ Card validated
       │
200ms  ├─ Emotion analysis starts
       │
200-5000ms  Analyzing video frames
       │
5000ms ├─ Emotion determined (e.g., "HAPPY")
       │
5050ms ├─ Python sends "LED_GREEN_BLINK"
       │
5100ms ├─ Arduino receives command
       │
5150ms └─ Green LED starts blinking
```

---

## 🆘 Common Issues

| Issue | Fix |
|-------|-----|
| LEDs won't light | Check polarity: long leg to resistor |
| Only one LED works | Test pins individually |
| Arduino not found | Check COM port, reinstall drivers |
| Emotion not detected | Improve lighting, get closer to camera |
| LEDs not blinking | Check BLINK_INTERVAL value |

---

## 📋 Emotion Ranges

| Emotion | Typical Confidence |
|---------|-------------------|
| Happy | 0.70 - 0.99 |
| Angry | 0.60 - 0.95 |
| Sad | 0.50 - 0.90 |
| Other | Variable |

---

## 🎨 LED Meanings

```
🟢 GREEN BLINK  = Happy mood detected
                = Positive emotion
                = Joyful expression

🔴 RED BLINK    = Angry mood detected
                = Negative emotion
                = Upset expression

⚫ OFF           = Neutral or other emotion
                = No clear emotional state
```

---

## 💾 Files Modified

| File | Changes |
|------|---------|
| `arduino_sketch/rfid_led_control.ino` | Added LED pins 2 & 3, LED control logic |
| `src/rfid_emotion_lite.py` | Added LED command sending, emotion-to-LED mapping |

---

## 🔗 Documentation

**For Detailed Info:**
- Hardware: `RFID_LED_INTEGRATION.md`
- Wiring: `CONNECTION_DIAGRAM.md` (adapted for pins 2 & 3)
- Code: Look at function `control_leds_for_emotion()` in Python

---

## ✨ Features

✅ RFID access control
✅ Real-time emotion detection
✅ Automatic LED response
✅ Green LED for happy
✅ Red LED for angry
✅ Music playback
✅ LCD display feedback
✅ Buzzer alerts

---

**Ready to use! Scan your RFID and show emotions!** 🎉

