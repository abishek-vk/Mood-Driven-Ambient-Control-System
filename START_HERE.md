# 🚀 QUICK START - Two LED Setup

## ⚡ 5-Minute Overview

Your system has **two LEDs** controlled by Arduino based on detected emotions from your face.

### The Setup
```
🟢 GREEN LED (Pin 10)  ← Happy, Surprised
🔴 RED LED (Pin 11)    ← Sad, Angry, Scared, Disgusted
🟢🔴 BOTH              ← Neutral (alternating)
```

---

## 🔧 Hardware Assembly (15 minutes)

### What You Need
- [ ] Arduino Uno
- [ ] 1× Green LED + 1× Red LED
- [ ] 2× 220Ω resistors
- [ ] Breadboard + 4 jumper wires
- [ ] USB cable

### Wiring (3 simple steps)

**Step 1: Green LED**
```
Arduino Pin 10 ──[220Ω]──→ Green LED (long leg)
                                └──→ GND
```

**Step 2: Red LED**
```
Arduino Pin 11 ──[220Ω]──→ Red LED (long leg)
                                └──→ GND
```

**Step 3: Ground**
```
Arduino GND ──→ Breadboard GND Rail (both LEDs connect here)
```

---

## 💻 Software (5 minutes)

### 1. Upload Arduino Code
1. Open Arduino IDE
2. Load: `arduino_sketch/mood_led_control.ino`
3. Click Upload
4. Check Serial Monitor → should show "READY"

### 2. Test Connection
```bash
python test_arduino.py
```
Expected: ✅ "Arduino connected" message

### 3. Run Real-time Detection
```bash
python src/main.py
```
Expected: 
- Webcam opens
- Emotion detected
- LEDs respond to your face 🎉

---

## 📊 Quick Command Reference

| Emotion | LED | Result |
|---------|-----|--------|
| 😊 Smile | 🟢 | Green blinks = Happy! |
| 😢 Frown | 🔴 | Red blinks = Sad... |
| 😐 Neutral | 🟢🔴 | Both alternate = Thinking... |

---

## 🎯 What Each File Does

```
📄 CONNECTION_DIAGRAM.md     ← START HERE for wiring
📄 TWO_LED_IMPLEMENTATION.md ← Python code explained
📄 QUICK_REFERENCE.md        ← Cheat sheet
📄 SYSTEM_ARCHITECTURE_DIAGRAM.txt ← Full system flow
📄 INDEX.md                  ← Full navigation
```

---

## ✨ Features

✅ Real-time emotion detection
✅ Automatic LED response
✅ Green for happy/surprised
✅ Red for sad/angry/scared
✅ Alternating for neutral
✅ Configurable blink speed
✅ Easy to customize

---

## 🆘 Quick Troubleshooting

| Issue | Fix |
|-------|-----|
| LED won't light | Check LED polarity (long leg toward resistor) |
| Arduino not found | Check COM port in Device Manager |
| Only one LED works | Test pins individually: `PIN_10_ON`, `PIN_11_ON` |
| Emotion detection slow | Reduce camera resolution or close other apps |

---

## 📞 Need Help?

- **Wiring questions:** See `CONNECTION_DIAGRAM.md`
- **Code questions:** See `TWO_LED_IMPLEMENTATION.md`
- **Command questions:** See `QUICK_REFERENCE.md`
- **System overview:** See `SYSTEM_ARCHITECTURE_DIAGRAM.txt`
- **Navigation:** See `INDEX.md`

---

## ✅ Checklist

- [ ] Hardware gathered
- [ ] LEDs wired to breadboard
- [ ] Arduino connected to PC
- [ ] `mood_led_control.ino` uploaded
- [ ] Serial monitor shows "READY"
- [ ] `test_arduino.py` passes
- [ ] `src/main.py` runs and detects emotions
- [ ] LEDs respond to your facial expressions
- [ ] System working! 🎉

---

## 🎉 That's It!

Once wired up and tested, your system automatically:
1. Detects your face via webcam
2. Predicts your emotion
3. Lights up the matching LED
4. Responds in real-time

**No more configuration needed!**

---

## 🚀 Next Ideas (Optional)

- Add more LEDs for other emotions
- Change blink speed for different confidence levels
- Log emotion history
- Integrate with music or lighting
- Deploy on Raspberry Pi

---

**Ready? Start with:** 📄 `CONNECTION_DIAGRAM.md`

**Questions?** All docs are in the root folder.

**Good luck!** 🚀
