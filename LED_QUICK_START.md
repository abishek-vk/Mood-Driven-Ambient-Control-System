# 🎭 MOOD-DRIVEN LED CONTROL - QUICK START GUIDE

## 📋 What You Need

### Hardware
- [ ] Arduino (Uno/Nano)
- [ ] 2 × LEDs (Green + Red recommended)
- [ ] 2 × 220Ω Resistors
- [ ] Breadboard & Jumper Wires
- [ ] USB Cable

### Software
- [ ] Python 3.7+
- [ ] Arduino IDE
- [ ] Dependencies installed (`pip install -r requirements.txt`)

---

## ⚡ Hardware Setup (5 minutes)

```
Arduino Pin 10 ──[220Ω]──► LED1 (Green) ──► GND
Arduino Pin 11 ──[220Ω]──► LED2 (Red)   ──► GND
```

✅ Check:
- LEDs light up when pins go HIGH
- Both LEDs are properly connected to GND

---

## 📥 Software Setup (5 minutes)

### Step 1: Upload Arduino Sketch
```
1. Open Arduino IDE
2. File → Open → arduino_sketch/mood_led_control.ino
3. Select your board (Arduino Uno)
4. Select your COM port
5. Click Upload
6. Wait for "Upload complete"
```

### Step 2: Install Python Dependencies
```bash
cd facial-recognition-system
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python src/led_control.py
```

---

## 🚀 Running the System

### Full System (Recommended)
```bash
python src/rfid_emotion_led_control.py
```

**What happens:**
1. Waits for RFID card scan
2. Detects face via camera
3. Analyzes emotion
4. **LEDs blink based on mood for 10 seconds**
5. Shows results

### Test LED Control Only
```bash
python src/led_control.py
```

Tests all emotions and LED patterns (no hardware needed)

---

## 🎨 LED Behavior

| Emotion | LED Status | Visual |
|---------|-----------|--------|
| 😊 Happy | LED 1 Blinks | 🟢💚 GREEN |
| 😮 Surprise | LED 1 Blinks | 🟢💚 GREEN |
| 😢 Sad | LED 2 Blinks | 🔴❤️ RED |
| 😠 Angry | LED 2 Blinks | 🔴❤️ RED |
| 😨 Fear | LED 2 Blinks | 🔴❤️ RED |
| 🤢 Disgust | LED 2 Blinks | 🔴❤️ RED |
| 😐 Neutral | Both Blink | ↔️ ALTERNATING |

---

## 🔧 Adjust Blink Speed

Edit `src/rfid_emotion_led_control.py`:

```python
led_blink_frequency = 2  # Change to 1-10 Hz
# 1 = Slow, 2 = Normal, 5+ = Fast
```

---

## ⚠️ Common Issues

### LEDs Don't Blink
✓ Check Arduino connection with serial monitor
✓ Verify LED wiring (long leg to pin, short to GND)
✓ Check resistors aren't burned

### "No Arduino Found"
✓ Check USB cable connection
✓ Install CH340 driver (for cheap Arduino clones)
✓ Check Device Manager for COM port

### Camera Issues
✓ Camera not in use by other apps
✓ Give Python permission to access camera
✓ Check lighting conditions

### Face Not Detected
✓ Move closer to camera (30-100cm)
✓ Improve lighting
✓ Face should be clearly visible

---

## 📊 Serial Commands (Arduino)

These are automatically sent by Python:

```
ALL_OFF              → Both LEDs OFF
PIN_10_ON            → LED1 ON (solid)
PIN_10_BLINK_2       → LED1 BLINK at 2 Hz
PIN_11_ON            → LED2 ON (solid)
PIN_11_BLINK_2       → LED2 BLINK at 2 Hz
BOTH_BLINK_ALT_1     → Both blink alternately
```

---

## 🧪 Testing Guide

### Test 1: Arduino Communication
```bash
# Test with Arduino IDE Serial Monitor
# Arduino should print "READY"
# Send: PIN_10_BLINK_2
# LED should blink
```

### Test 2: LED Module
```bash
python src/led_control.py
# Should show simulation of all emotions
# No Arduino needed for this test
```

### Test 3: Full System
```bash
python src/rfid_emotion_led_control.py
# Scan RFID card → See LEDs blink based on your emotion
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `src/led_control.py` | LED controller (emotion→LED mapping) |
| `src/rfid_emotion_led_control.py` | Main system (RFID+Face+Emotion+LED) |
| `arduino_sketch/mood_led_control.ino` | Arduino firmware |
| `LED_INTEGRATION_GUIDE.md` | Detailed documentation |

---

## 🎯 Expected Output

```
✅ SYSTEM READY - WAITING FOR RFID SCAN

[Arduino] READY
[Facial Recognition] Camera started
[LED Controller] Ready

[After RFID Scan]
✅ RFID CARD AUTHORIZED
🎥 EMOTION ANALYSIS STARTED (10s)
[MOOD] HAPPY (0.95) → positive
[LED] Positive LED (Pin 10) BLINKING at 2 Hz

[Results]
📊 EMOTION ANALYSIS RESULTS
Emotions detected: 45
  happy        : 35 detections (77.8%) → ✨ POSITIVE
  neutral      : 10 detections (22.2%) → 😐 NEUTRAL
✅ DOMINANT EMOTION: HAPPY
   MOOD: ✨ POSITIVE
```

---

## 💡 Pro Tips

1. **Better Face Detection**: Use good lighting, face camera clearly
2. **Accurate Emotions**: Keep still for 2-3 seconds per detection
3. **Fast Response**: Increase `led_blink_frequency` to 5+
4. **Debug Mode**: Add print statements in `led_control.py` to see all commands
5. **Custom Mapping**: Edit `emotion_to_mood_map` in `led_control.py` to change behavior

---

## 📞 Support

Check these files for detailed info:
- **LED_INTEGRATION_GUIDE.md** - Full documentation
- **TROUBLESHOOTING.md** - Common issues
- **README.md** - General setup

---

**Ready? Let's make your mood light up! 🎉**
