# ⚡ Quick Wiring Reference Card

## Pin Connections

```
╔═══════════════════════════════════════════════════════════╗
║           MOOD-DRIVEN AMBIENT CONTROL SYSTEM              ║
║                   TWO LED SETUP                           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  POSITIVE MOOD LED (Green)                                ║
║  ───────────────────────────                              ║
║  Arduino Pin 10 ──[220Ω]──→ Green LED (+)                ║
║                               └─→ GND                     ║
║  Status: ✅ ACTIVE                                         ║
║                                                           ║
║  ─────────────────────────────────────────────────────── ║
║                                                           ║
║  NEGATIVE MOOD LED (Red)                                  ║
║  ─────────────────────────                                ║
║  Arduino Pin 11 ──[220Ω]──→ Red LED (+)                  ║
║                               └─→ GND                     ║
║  Status: ✅ ACTIVE                                         ║
║                                                           ║
║  ─────────────────────────────────────────────────────── ║
║                                                           ║
║  GROUND REFERENCE                                         ║
║  ───────────────────                                      ║
║  Arduino GND ──→ Breadboard GND rail (Blue -)            ║
║  Both LEDs ──→ Same GND rail                              ║
║  Status: ✅ ACTIVE                                         ║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║              RESISTOR SPECIFICATIONS                      ║
╠═══════════════════════════════════════════════════════════╣
║  Value: 220Ω (Ohm)                                        ║
║  Quantity: 2 (one per LED)                                ║
║  Purpose: Current limiting (protects LEDs)                ║
║  Power Rating: 1/4W minimum recommended                   ║
╚═══════════════════════════════════════════════════════════╝
```

## Breadboard Layout (Top View)

```
                     Arduino Connections
                              │
                    ┌─────────┴─────────┐
                    │                   │
              Pin 10│                   │Pin 11
                 GND│                   │GND
                    ▼                   ▼
┌──────────────────────────────────────────────────────────┐
│                    BREADBOARD                            │
│                                                          │
│  + (Red Power)                                           │
│  │                                                       │
│  ├─ [220Ω] ──┬──────▶ 🟢 Green LED                       │
│  │           │            ├─ (Anode +)                   │
│  │           │            └─ (Cathode -)                 │
│  │           │                      │                    │
│  ├─ [220Ω] ──┼──────▶ 🔴 Red LED    │                    │
│  │           │            ├─ (Anode +)                   │
│  │           │            └─ (Cathode -)                 │
│  │           │                      │                    │
│  - (Blue Ground) ◄──────────────────┘                    │
│  │                                                       │
│  └─ Connected to Arduino GND                             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Emotion to LED Mapping

```
┌─────────────────────────────────────────────┐
│    EMOTION DETECTION → LED RESPONSE         │
├─────────────────────────────────────────────┤
│                                             │
│  😊 HAPPY      ──→ 🟢 GREEN LED (BLINK)   │
│  😲 SURPRISE   ──→ 🟢 GREEN LED (BLINK)   │
│                                             │
│  ──────────────────────────────────────    │
│                                             │
│  😢 SAD        ──→ 🔴 RED LED (BLINK)     │
│  😠 ANGRY      ──→ 🔴 RED LED (BLINK)     │
│  😨 FEAR       ──→ 🔴 RED LED (BLINK)     │
│  🤢 DISGUST    ──→ 🔴 RED LED (BLINK)     │
│                                             │
│  ──────────────────────────────────────    │
│                                             │
│  😐 NEUTRAL    ──→ 🟢🔴 BOTH (ALTERNATE)  │
│                                             │
└─────────────────────────────────────────────┘
```

## Serial Commands Cheat Sheet

```
╔════════════════════════════════════════════════════╗
║         ARDUINO SERIAL COMMANDS (9600 baud)        ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  GREEN LED (Pin 10) Control:                       ║
║  ├─ PIN_10_ON         → Turn solid ON              ║
║  ├─ PIN_10_OFF        → Turn OFF                   ║
║  └─ PIN_10_BLINK_2    → Blink at 2 Hz              ║
║                                                    ║
║  RED LED (Pin 11) Control:                         ║
║  ├─ PIN_11_ON         → Turn solid ON              ║
║  ├─ PIN_11_OFF        → Turn OFF                   ║
║  └─ PIN_11_BLINK_2    → Blink at 2 Hz              ║
║                                                    ║
║  Both LEDs Control:                                ║
║  ├─ BOTH_BLINK_ALT_1  → Alternate blink (1 Hz)    ║
║  └─ ALL_OFF           → Turn both OFF              ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

## Python API Quick Reference

```python
# Import
from src.led_control import LEDController
import serial

# Initialize
ser = serial.Serial('COM3', 9600)  # Adjust COM port
led = LEDController(serial_connection=ser)

# Automatic (Emotion-based)
led.set_mood('happy')        # 🟢 Green blinks
led.set_mood('sad')          # 🔴 Red blinks
led.set_mood('neutral')      # 🟢🔴 Both alternate

# Manual Control
led.led_positive_on()                      # Green ON
led.led_negative_blink(frequency=3)        # Red blink at 3 Hz
led.all_leds_off()                         # Both OFF

# With Confidence (optional)
led.set_mood('happy', confidence=0.95)     # 95% confident
```

## Hardware Checklist

```
BEFORE CONNECTING:
□ Arduino Uno (or compatible)
□ 1× Green LED (5mm common cathode)
□ 1× Red LED (5mm common cathode)
□ 2× 220Ω Resistors (1/4W)
□ 1× Breadboard (830 holes)
□ 4× Male-to-Male Jumper Wires
□ 1× USB Cable (Arduino programming)
□ 1× Serial Cable/Adapter (if needed)

WIRING VERIFICATION:
□ Green LED longer leg → Pin 10 via 220Ω resistor
□ Green LED shorter leg → GND
□ Red LED longer leg → Pin 11 via 220Ω resistor
□ Red LED shorter leg → GND
□ Arduino GND → Breadboard GND rail
□ No loose connections
□ Resistors firmly in place
□ LEDs perpendicular to breadboard
```

## Testing Steps

```
1. HARDWARE TEST
   python test_arduino.py
   Expected: "Arduino Ready" message

2. LED CONTROL TEST (No Arduino needed)
   python src/led_control.py
   Expected: LED control messages in console

3. EMOTION DETECTION TEST
   python test_mood_led.py
   Expected: Real-time emotion detection with LED control

4. FULL INTEGRATION TEST
   python src/main.py
   Expected: Webcam + emotion detection + LED response
```

## Current Status ✅

- [x] Hardware design finalized
- [x] Arduino sketch implemented and tested
- [x] Python LED control module created
- [x] Emotion-to-LED mapping implemented
- [x] Serial communication established
- [x] Documentation complete

**System is READY for deployment!** 🚀
