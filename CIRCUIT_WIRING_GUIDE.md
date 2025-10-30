# ⚡ LED Circuit Wiring Guide

## Simplified Connection Diagram

```
┌─────────────────┐
│     Arduino     │
│      UNO        │
│                 │
│  [10] ──────────┼──[220Ω]──┬──> 📍 LED1 (Green) ──┐
│                 │           │                      ├──> GND
│  [11] ──────────┼──[220Ω]──┬──> 📍 LED2 (Red)   ──┘
│                 │           │
│  [GND] ─────────┼───────────┴──> Ground Reference
│                 │
└─────────────────┘
```

## Breadboard Layout

```
┌──────────────────────────────────────────┐
│  Breadboard (Top View)                   │
├──────────────────────────────────────────┤
│                                          │
│  +  -  |  a  b  c  d  e  |  f  g  h  i  │
│  ─────┼─────────────────┼──────────────  │
│  A  │ ●              ●  │  ●         │  │   Arduino Pin 10
│     │ │              │  │  │ [220Ω]     │
│  B  │ ●──────────────●  │  ●─────────   │   ↓
│     │ │              │  │      │        │
│  C  │ ●              ●  │  ●   ●   ●   │   LED1 (+)
│     │                   │              │
│  D  │ ●              ●  │  ●         │  │   Arduino Pin 11
│     │ │              │  │  │ [220Ω]     │
│  E  │ ●──────────────●  │  ●─────────   │   ↓
│     │ │              │  │      │        │
│  F  │ ●              ●  │  ●   ●   ●   │   LED2 (+)
│     │                   │              │
│  G  │ ●              ●  │  ●         │  │   GND Reference
│     │ │              │  │  │         │  │
│     └──────────────────────────────────── │
│                                          │
│  Legend:                                 │
│  ● = Hole                                │
│  ─ = Wire Connection                     │
│  + = Positive (Red row)                  │
│  - = Negative (Blue row)                 │
└──────────────────────────────────────────┘
```

## Step-by-Step Wiring Instructions

### What You Need:
- [ ] Arduino Uno/Nano
- [ ] Breadboard
- [ ] 2 × LEDs (green & red)
- [ ] 2 × 220Ω resistors
- [ ] 6 × Jumper wires (male-to-male)
- [ ] USB cable

### Wiring Steps:

#### Step 1: Prepare the Breadboard
1. Place breadboard on flat surface
2. Take note of the + (positive/red) and - (negative/blue) rows on sides

#### Step 2: Install LED 1 (Green) - Pin 10
```
1. Insert green LED vertically into breadboard:
   - Longer leg (anode, +) → into column for resistor
   - Shorter leg (cathode, -) → into negative row (blue -)

2. Connect 220Ω resistor:
   - One end: from Arduino Pin 10
   - Other end: to the longer leg side of LED

3. Wire connection:
   Arduino Pin 10 ──[220Ω Resistor]──> LED1 Long Leg
   LED1 Short Leg ──────────────────> GND Row
```

#### Step 3: Install LED 2 (Red) - Pin 11
```
1. Insert red LED vertically into breadboard (next to green LED):
   - Longer leg (anode, +) → into column for resistor
   - Shorter leg (cathode, -) → into negative row (blue -)

2. Connect 220Ω resistor:
   - One end: from Arduino Pin 11
   - Other end: to the longer leg side of LED

3. Wire connection:
   Arduino Pin 11 ──[220Ω Resistor]──> LED2 Long Leg
   LED2 Short Leg ──────────────────> GND Row
```

#### Step 4: Connect Ground
```
1. Connect Arduino GND pin to negative row (blue -):
   Arduino GND ──────────────────> Negative Row
```

### Final Wiring Checklist:
```
LED Identification:
✓ Green LED in circuit 1
✓ Red LED in circuit 2
✓ Both resistors installed (220Ω)

Polarity Check:
✓ LED longer legs (anodes) toward resistors
✓ LED shorter legs (cathodes) toward GND
✓ No reversed connections

Arduino Connections:
✓ Pin 10 to LED1 circuit
✓ Pin 11 to LED2 circuit
✓ GND to negative rail

Physical Check:
✓ All wires firmly inserted
✓ No loose connections
✓ No wires touching each other
✓ Resistors not overheating (should be cool)
```

---

## Troubleshooting LED Connections

### LED Won't Light Up

**Symptom:** LED doesn't light when Arduino pin goes HIGH

**Causes & Solutions:**

1. **Reverse Polarity** (Most Common)
   - Check: Longer leg of LED should touch power, shorter to GND
   - Fix: Remove LED and reinsert correctly

2. **Bad Resistor**
   - Check: If resistor is too high value (>470Ω)
   - Fix: Replace with 220Ω resistor
   - Test: Measure with multimeter (should show ~220Ω)

3. **Poor Connection**
   - Check: Breadboard holes for bent/dirty contacts
   - Fix: Adjust wires to ensure firm contact
   - Try: Different holes on breadboard

4. **Broken LED**
   - Test: Connect LED directly to battery (with resistor)
   - If no light: LED is burned out, replace

5. **Arduino Pin Not Working**
   - Check: Pin 10/11 actually outputs 5V
   - Test: Connect working LED to different pin
   - Try: Use different Arduino board if available

### Dim LED

**Symptom:** LED lights but very dim

**Possible Causes:**

1. **Resistor Too High**
   - Standard: 220Ω (typical)
   - Check value written on resistor
   - Replace if it's 1kΩ or higher

2. **Arduino Pin Not Fully HIGH**
   - Check: Serial output from Arduino shows PIN_X_ON
   - May be initial connection issue - wait 2 seconds

### Blinking Not Consistent

**Symptom:** LED blinks irregularly

**Possible Causes:**

1. **Bad Breadboard Contact**
   - Reseat all connections
   - Try: Move wires to different holes

2. **Intermittent Connection**
   - Check: Solder joints if using breadboard
   - Try: Use shorter, quality wires

3. **Power Supply Issue**
   - Check: Arduino is getting stable power via USB
   - Try: Different USB port or cable

---

## Advanced: Using Resistor Color Code

### Color bands on resistor show value:

```
For 220Ω resistor:
Red   - Black - Brown = 22 × 10^1 = 220Ω
(2)   - (0)   - (10)

Band order (left to right):
1st digit | 2nd digit | Multiplier
Red(2)    | Black(0)  | Brown(1) = 220Ω
```

### Common Resistor Values:
- 220Ω  ← **USE THIS** (Red-Red-Brown)
- 330Ω  ← (Orange-Orange-Brown)
- 470Ω  ← (Yellow-Purple-Brown)
- 1kΩ   ← (Brown-Black-Red)

---

## Multiple LED Setup (Future Expansion)

### For 3+ LEDs:
```
Arduino Pin 12 ──[220Ω]──> LED3 ──> GND
Arduino Pin 13 ──[220Ω]──> LED4 ──> GND
Arduino Pin A0 ──[220Ω]──> LED5 ──> GND
```

Modify Arduino code:
```cpp
#define LED3_PIN 12
#define LED4_PIN 13
#define LED5_PIN 14  // A0 = 14
```

---

## Safety Notes ⚠️

1. **Power**: Arduino provides safe 5V - no shock hazard
2. **LEDs**: Standard 5mm LEDs work fine, no special handling needed
3. **Resistors**: Don't overheat - they'll be slightly warm but not hot
4. **Arduino**: Can handle multiple GPIO outputs - no special power supply needed

---

## Testing Your Circuit

### Quick Test (No Code Needed):

1. **Visual Inspection**
   - All connections tight?
   - Both LEDs installed correctly?
   - Both resistors in place?

2. **Power-On Test**
   - Connect Arduino via USB
   - Look for LED activity
   - Check if Arduino LED blinks

3. **Manual Test**
   - Open Arduino IDE Serial Monitor
   - Send: `PIN_10_BLINK_2`
   - Green LED should blink
   - Send: `PIN_11_BLINK_2`
   - Red LED should blink

---

**If you're still having issues, check the detailed troubleshooting in `TROUBLESHOOTING.md`**
