# 🔌 RFID + LED Wiring Diagram (Detailed)

## Complete Arduino Pin Layout

```
┌─────────────────────────────────────────────────────────┐
│             ARDUINO UNO - ALL CONNECTIONS               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  POWER:                    RFID Module (SPI):           │
│  ├─ 5V                     ├─ SS   → Pin 10            │
│  ├─ GND (multiple)         ├─ RST  → Pin 9             │
│  └─ VCC → 3.3V or 5V       ├─ MOSI → Pin 11 (SPI)      │
│                            ├─ MISO → Pin 12 (SPI)      │
│                            ├─ SCK  → Pin 13 (SPI)      │
│                            └─ GND  → GND               │
│                                                         │
│  LCD Display (I2C):        NEW: LED Control:            │
│  ├─ SDA → A4               ├─ Pin 2 → 🟢 GREEN LED     │
│  ├─ SCL → A5               ├─ Pin 3 → 🔴 RED LED       │
│  ├─ VCC → 5V               └─ GND → Common Ground      │
│  └─ GND → GND                                           │
│                            Audio:                       │
│                            ├─ Pin 7 → Buzzer            │
│                            └─ GND → GND                 │
│                                                         │
│  Serial (USB):                                          │
│  ├─ RX (Pin 0) ← Python script                          │
│  ├─ TX (Pin 1) → Python script                          │
│  └─ GND → GND                                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Simplified Block Diagram

```
         COMPUTER (Python)
              │
              │ USB Serial
              ▼
      ┌──────────────────┐
      │   Arduino UNO    │
      ├──────────────────┤
      │                  │
      │  Pin 2: 🟢 Green ├────[220Ω]────┬──→ Green LED
      │  Pin 3: 🔴 Red   ├────[220Ω]────┬──→ Red LED
      │  GND:   Common   ├──────────────┬──→ Both LEDs
      │                  │              │    (Short legs)
      │  Pin 9-13: RFID  ├──→ RFID      │
      │  A4-A5: LCD      ├──→ LCD       │
      │  Pin 7: Buzzer   ├──→ Buzzer    │
      │                  │              │
      └──────────────────┘              │
                                        │
                                    ┌───┴────┐
                                    │   GND   │
                                    │ (Common)│
                                    └─────────┘
```

---

## LED Connections - Detailed

### Green LED (Pin 2)

```
Arduino Pin 2
     │
     ├──→ [220Ω Resistor]
     │         │
     │         ├──→ Green LED Anode (+) ──┐ Long leg
     │         │                          │
     └─────────┴──→ GND ←─── LED Cathode (-) ──┘ Short leg

Current Path:
Arduino 5V → Pin 2 HIGH → 220Ω Resistor → Green LED → GND
Voltage Drop: ~5V - 0.2V (resistor) - 2V (LED) = ~2.8V
Current: ~18mA (safe for Arduino pin)
```

### Red LED (Pin 3)

```
Arduino Pin 3
     │
     ├──→ [220Ω Resistor]
     │         │
     │         ├──→ Red LED Anode (+) ──┐ Long leg
     │         │                        │
     └─────────┴──→ GND ←─── LED Cathode (-) ──┘ Short leg

Current Path:
Arduino 5V → Pin 3 HIGH → 220Ω Resistor → Red LED → GND
Voltage Drop: ~5V - 0.2V (resistor) - 2V (LED) = ~2.8V
Current: ~18mA (safe for Arduino pin)
```

---

## Breadboard Layout - Top View

```
                   From Arduino
                   │       │       │
                   ▼       ▼       ▼
                  Pin2    Pin3    GND

┌──────────────────────────────────────────────────┐
│          BREADBOARD (830 holes)                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  + Rail (Red)   - Rail (Blue)                   │
│  ▲              ▲                                │
│  │              │                                │
│  A    B    C    D    E  │  F    G    H    I    │
│  ●    ●    ●    ●    ●  │  ●    ●    ●    ●   │
│  ●    ●    ●    ●    ●  │  ●    ●    ●    ●   │
│  ●    ●    ●    ●    ●  │  ●    ●    ●    ●   │
│  ●    ●    ●    ●    ●  │  ●    ●    ●    ●   │
│                                                  │
│ Row 5:                                           │
│  ┌────●    ●────┐  ●    │  ●────●    ●────┐   │
│  │ [220Ω]  🟢   │         From Pin 2 | From    │
│  └────●    ●────┘        resistor   │ Arduino  │
│                                      │          │
│ Row 10:                               │          │
│  ┌────●    ●────┐  ●    │  ●────●    ●────┐   │
│  │ [220Ω]  🔴   │         From Pin 3 | From    │
│  └────●    ●────┘        resistor   │ Arduino  │
│                                      │          │
│ Row 15:                               │          │
│  ┌────●    ●────┐  ●    │  ●────●    ●────┐   │
│  │  GND    GND   │         All GND    | From    │
│  │ Rail   Rail   │         connections │ Arduino│
│  └────●    ●────┘                      │        │
│         ▲         ▲                     ▼        │
│         │         │                Green leg    │
│         │         │                (Cathode)    │
│         │         └────────────────────────     │
│         │            Red leg                    │
│         │            (Cathode)                  │
│         │            ▲                          │
│         └────────────┘                          │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Step-by-Step Assembly

### Step 1: Place Resistors

```
Row 1:  ├─ [220Ω Resistor #1]
        ├─ One end: Hole A1
        └─ Other end: Hole B1 (connect to Green LED)

Row 5:  ├─ [220Ω Resistor #2]
        ├─ One end: Hole A5
        └─ Other end: Hole B5 (connect to Red LED)
```

### Step 2: Insert LEDs

```
Green LED (Row 1-2):
  ├─ Long leg (+): Hole B1 (from resistor)
  └─ Short leg (-): Hole C1 (to GND rail)

Red LED (Row 5-6):
  ├─ Long leg (+): Hole B5 (from resistor)
  └─ Short leg (-): Hole C5 (to GND rail)
```

### Step 3: Connect Wires

```
Arduino → Breadboard:
  ├─ Pin 2 → Hole A1 (Green resistor input)
  ├─ Pin 3 → Hole A5 (Red resistor input)
  ├─ GND → GND Rail (both columns C1 and C5)
  └─ Secure with jumper wires
```

### Step 4: Verify Connections

```
✓ All resistors firmly in breadboard
✓ LEDs upright with correct orientation
✓ No loose wires or connections
✓ GND rail connected to Arduino GND
✓ Pin 2 and Pin 3 connected to resistor inputs
✓ LED cathodes connected to GND rail
```

---

## Electrical Specifications

### Per-LED Specifications

```
Component         Value/Rating
─────────────────────────────
Resistor          220Ω ± 5%
LED Forward Voltage ~2.0V
LED Max Current   20mA
Resistor Power    1/4W (0.25W)
Arduino Pin Max   40mA per pin

Calculation:
  V_resistor = 5V - 2V (LED) = 3V
  I = V / R = 3V / 220Ω = 13.6mA
  P = V × I = 3V × 0.0136A = 0.041W ✓ (< 0.25W)
```

### Safety Margin

```
Arduino Pin Rating    : 40mA
LED Current           : 13.6mA
Safety Margin         : 26.4mA (66% headroom) ✓

Total for Both LEDs:
  Combined Current    : 27.2mA
  Arduino Total       : 200mA (all pins)
  Safe Operation      : Yes ✓
```

---

## Troubleshooting Connections

### Test Points

```
When LED is ON:
┌─────────────────────────────────────┐
│ Test Point        Expected Voltage   │
├─────────────────────────────────────┤
│ Arduino Pin 2     5V (HIGH)          │
│ Before Resistor   ~4.8V              │
│ After Resistor    ~3.0V              │
│ LED Anode         ~3.0V              │
│ LED Cathode       0V (GND)           │
│ GND Rail          0V                 │
└─────────────────────────────────────┘

Use Multimeter to Check:
  Red probe at test point
  Black probe at GND
  Should match expected voltage
```

### If LED Doesn't Light

```
Check (in order):
1. Is Arduino Pin 2/3 actually HIGH?
   → Use Serial.print(digitalRead(2));
   → Should print 1 when blinking

2. Is resistor value correct?
   → Use multimeter (should be ~220Ω)
   → Check for burns/damage

3. Is LED polarity correct?
   → Long leg should be connected to resistor
   → Short leg should be connected to GND

4. Is GND connection secure?
   → Check continuity between:
     Arduino GND ↔ Breadboard GND rail
     LED cathode ↔ Breadboard GND rail

5. Is LED burned out?
   → Swap with working LED
   → If new LED works, old one is bad
```

---

## Serial Communication Diagram

```
┌──────────────┐                    ┌──────────────┐
│   COMPUTER   │ USB Serial (9600)  │  ARDUINO UNO │
│   (Python)   │◄────────────────►│              │
│              │                    │              │
│ Sends:       │                    │ Processes:   │
│ LED_GREEN_   │  ─────────────►   │              │
│ BLINK        │                    │ Sets Pin 2   │
│              │                    │ to HIGH      │
│              │                    │              │
│              │                    │ Timer loops: │
│              │                    │  500ms: HIGH │
│              │                    │  500ms: LOW  │
│              │                    │  Repeat...   │
│              │                    │              │
│ Receives:    │                    │ Sends:       │
│ GREEN_LED_   │  ◄─────────────   │ "GREEN_LED_  │
│ ACTIVE       │                    │ ACTIVE"      │
│              │                    │              │
└──────────────┘                    └──────────────┘
```

---

## Power Flow Diagram

```
USB Power ──→ Arduino 5V Pin ──┐
                               │
Arduino GND ◄─ USB Power GND   │
                               │
        ┌──────────────────────┘
        │
        ├─→ Pin 2 (Green LED)
        │   │
        │   ├─→ [220Ω] ──→ 🟢 LED ──→ GND ──→ Arduino GND
        │   │
        ├─→ Pin 3 (Red LED)
        │   │
        │   ├─→ [220Ω] ──→ 🔴 LED ──→ GND ──→ Arduino GND
        │
        ├─→ All other components
        │
        └─→ Returns to GND (completes circuit)
```

---

**Your RFID + LED setup is now complete!** 🎉
