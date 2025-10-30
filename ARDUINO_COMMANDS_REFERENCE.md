# 🎛️ Arduino LED Commands Reference Card

## Serial Communication Format

**Baud Rate:** 9600  
**Data Bits:** 8  
**Stop Bits:** 1  
**Parity:** None  
**Line Ending:** `\n` (newline)

---

## Core Commands

### All Lights OFF
```
Command: ALL_OFF
Effect: Both LEDs turn off immediately
Usage: When analysis ends, no face detected, etc.
```

### LED1 Control (Pin 10 - Positive Mood)

#### Turn LED1 ON (solid)
```
Command: PIN_10_ON
Effect: LED1 stays on continuously
LED State: Solid light
```

#### Turn LED1 OFF
```
Command: PIN_10_OFF
Effect: LED1 turns off
LED State: Dark
```

#### Blink LED1
```
Command: PIN_10_BLINK_X
Where X = frequency in Hz (1-10)

Examples:
PIN_10_BLINK_1  → Blink 1 time per second (slow)
PIN_10_BLINK_2  → Blink 2 times per second (normal)
PIN_10_BLINK_5  → Blink 5 times per second (fast)
```

---

### LED2 Control (Pin 11 - Negative Mood)

#### Turn LED2 ON (solid)
```
Command: PIN_11_ON
Effect: LED2 stays on continuously
LED State: Solid light
```

#### Turn LED2 OFF
```
Command: PIN_11_OFF
Effect: LED2 turns off
LED State: Dark
```

#### Blink LED2
```
Command: PIN_11_BLINK_X
Where X = frequency in Hz (1-10)

Examples:
PIN_11_BLINK_1  → Blink 1 time per second (slow)
PIN_11_BLINK_2  → Blink 2 times per second (normal)
PIN_11_BLINK_5  → Blink 5 times per second (fast)
```

---

### Both LEDs Control

#### Blink Alternately
```
Command: BOTH_BLINK_ALT_X
Where X = frequency in Hz (1-10)

Effect: LED1 and LED2 blink opposite each other
        When LED1 is ON, LED2 is OFF (and vice versa)

Examples:
BOTH_BLINK_ALT_1  → Slow alternating (1 Hz)
BOTH_BLINK_ALT_2  → Normal alternating (2 Hz)
BOTH_BLINK_ALT_3  → Fast alternating (3 Hz)
```

---

## Emotion-Based Command Sequences

### Happy/Surprise Detected
```
Step 1: ALL_OFF                (clear previous state)
Step 2: PIN_10_BLINK_2         (blink positive LED at 2 Hz)
        Duration: 10 seconds
Step 3: ALL_OFF                (turn off after analysis)
```

### Sad/Angry/Fear Detected
```
Step 1: ALL_OFF                (clear previous state)
Step 2: PIN_11_BLINK_2         (blink negative LED at 2 Hz)
        Duration: 10 seconds
Step 3: ALL_OFF                (turn off after analysis)
```

### Neutral Detected
```
Step 1: ALL_OFF                (clear previous state)
Step 2: BOTH_BLINK_ALT_1       (both blink alternately at 1 Hz)
        Duration: 10 seconds
Step 3: ALL_OFF                (turn off after analysis)
```

---

## Communication Examples

### Python Sending Commands to Arduino

```python
# Send command via serial
ser.write(b"PIN_10_BLINK_2\n")

# Command breakdown:
# - PIN_10      → Pin number 10
# - BLINK       → Action (blink)
# - 2           → 2 Hz frequency
# - \n          → Newline terminator (required!)
```

### Testing with Arduino Serial Monitor

1. Open Arduino IDE
2. Click: `Tools → Serial Monitor`
3. Set baud rate to 9600
4. Type command, press Enter

```
Arduino should reply: CMD: PIN_10_BLINK_2
LED1 should start blinking
```

---

## Frequency Guide

| Hz | Blinks/Second | Speed | Use Case |
|----|---------------|-------|----------|
| 1 | 1 | Very Slow | Neutral/calm moods |
| 2 | 2 | Slow | Default/normal |
| 3 | 3 | Medium | Slightly faster feedback |
| 4 | 4 | Medium-Fast | More noticeable |
| 5 | 5 | Fast | Rapid feedback |
| 10 | 10 | Very Fast | Alert/warning state |

---

## Expected Arduino Responses

### Successful Command
```
Input:  PIN_10_BLINK_2
Output: CMD: PIN_10_BLINK_2
        LED Pin 10 BLINKING at 2 Hz
```

### All Off Command
```
Input:  ALL_OFF
Output: All LEDs OFF
```

### Invalid Command
```
Input:  UNKNOWN_COMMAND
Output: ERR: Unknown command
```

### Connection Ready
```
After USB connection:
Output: READY
        Arduino Mood-Driven LED Control Ready
```

---

## Timing Reference

### Example Blink Pattern (2 Hz - PIN_10_BLINK_2)

```
Time    LED State
────────────────
0ms     ON
250ms   OFF
500ms   ON
750ms   OFF
1000ms  ON (1 second elapsed = 2 blinks)
1250ms  OFF
1500ms  ON
1750ms  OFF
2000ms  ON (2 seconds elapsed = 4 blinks)
...
```

**Total time for 1 blink at 2 Hz = 500ms**

---

## Quick Troubleshooting

### No Response from Arduino
✓ Check baud rate is 9600  
✓ Check USB connection  
✓ Check line ending is set to `\n`  
✓ Try unplugging and replugging USB  

### LED Won't Blink
✓ Send `PIN_10_ON` first to test if LED works  
✓ Check frequency value is 1-10  
✓ Verify pin number (10 or 11)  

### Frequency Not Working
✓ Valid range: 1-10 Hz  
✓ Arduino will clamp invalid values  
✓ Higher values = faster blinking  

### Alternating Blink Issues
✓ Use `BOTH_BLINK_ALT_X` (not separate commands)  
✓ LEDs should blink opposite to each other  
✓ Frequency must be 1-10  

---

## Command Syntax Summary

```
Format: COMMAND_PARAMETER_VALUE\n

Valid Commands:
  - ALL_OFF
  - PIN_10_ON
  - PIN_10_OFF
  - PIN_10_BLINK_X        (X = 1-10)
  - PIN_11_ON
  - PIN_11_OFF
  - PIN_11_BLINK_X        (X = 1-10)
  - BOTH_BLINK_ALT_X      (X = 1-10)

Always end with \n (newline)
Case sensitive
```

---

## Python Integration Example

```python
import serial
import time

# Open serial port
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino init

# Send LED commands
commands = [
    "ALL_OFF",
    "PIN_10_BLINK_2",
    time.sleep(5),
    "ALL_OFF"
]

for cmd in commands:
    if callable(cmd):
        cmd()
    else:
        ser.write((cmd + '\n').encode())
        print(f"Sent: {cmd}")
        time.sleep(0.1)

ser.close()
```

---

## Frequency Recommendations

**Positive Mood (LED1):**
- Happy: 2-3 Hz (moderate happiness)
- Excited: 5 Hz (fast blink)
- Very Happy: 1 Hz (slow, satisfied)

**Negative Mood (LED2):**
- Sad: 1 Hz (slow, somber)
- Angry: 3-5 Hz (fast, agitated)
- Fear: 4-5 Hz (rapid, anxious)

**Neutral (Both):**
- Neutral: 1-2 Hz (steady alternation)

---

## Safety Notes ⚠️

✓ Max frequency: 10 Hz (system may slow down beyond this)  
✓ Min frequency: 1 Hz  
✓ LEDs are safe at all frequencies  
✓ Arduino handles invalid frequencies gracefully  
✓ No damage from sending repeated commands  

---

## For More Information

📖 See `LED_INTEGRATION_GUIDE.md` for full documentation  
🔧 See `CIRCUIT_WIRING_GUIDE.md` for hardware setup  
⚡ See `LED_QUICK_START.md` for quick reference  

---

**Keep this card handy while developing!** 📌
