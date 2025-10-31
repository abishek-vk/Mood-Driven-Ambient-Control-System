# 🔌 Two LED Connection Diagram

## Detailed Physical Connection Diagram

```
                          ┌──────────────────┐
                          │   ARDUINO UNO    │
                          │                  │
                       GND│                  │VCC (5V)
                          │  [Digital Pins]  │
                          │                  │
                          │  10 ┌─  ┌─ 11   │
                          │  │     │        │
                          │  GND ─┤ GND    │
                          └──┬────────┬──────┘
                             │        │
                ┌────────────┴┐       │
                │             │       │
                │    Arduino GND ────┐
                │             │      │
                │    ┌────────┘      │
                │    │               │
         ┌──────────┐│               │
         │          ││               │
         │  Pin 10  ├─┼─[220Ω]──┬───┤
         │          │ │          │   │
         └──────────┘ │          │   │
                      │      ┌───────────┐
                      │      │🟢 GREEN   │
                      │      │ LED       │
                      │      │  (+)──────┼─── To 220Ω Resistor
                      │      │  (-)      │
                      │      └───────────┘
                      │          │
                      │          │ (Short Leg)
                      │          │
                      │   ┌──────┴─────┐
                      │   │ GND Row    │
                      │   │ (Breadboard)
                      │   └─────┬──────┘
                      │         │
         ┌──────────┐ │         │
         │          │ │         │
         │  Pin 11  ├─┼─[220Ω]──┼──┬───┐
         │          │ │         │  │   │
         └──────────┘ │         │  │   │
                      │    ┌────────────┐
                      │    │ 🔴 RED     │
                      │    │ LED        │
                      │    │  (+)───────┼─── To 220Ω Resistor
                      │    │  (-)       │
                      │    └────────────┘
                      │        │
                      │        │ (Short Leg)
                      │        │
                      └────────┴─────────────→ All connect to GND Rail
```

## Simple Point-to-Point Wiring

### Green LED (Positive Mood)

```
Arduino Pin 10 
        │
        ├──→ [220Ω Resistor]
        │        │
        │        └──→ Green LED Anode (+)
        │                    │
        │                    └──→ Green LED Cathode (-)
        │                            │
        │                            └──→ GND Rail
        │
        └──→ GND (Reference)
```

### Red LED (Negative Mood)

```
Arduino Pin 11
        │
        ├──→ [220Ω Resistor]
        │        │
        │        └──→ Red LED Anode (+)
        │                  │
        │                  └──→ Red LED Cathode (-)
        │                          │
        │                          └──→ GND Rail
        │
        └──→ GND (Reference)
```

## Breadboard Configuration (Top View)

```
╔════════════════════════════════════════════════════╗
║             BREADBOARD LAYOUT (TOP VIEW)           ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  POSITIVE RAIL (Red)    NEGATIVE RAIL (Blue)     ║
║  +  +  +  +  +  +  +    -  -  -  -  -  -  -      ║
║  │  │  │  │  │  │  │    │  │  │  │  │  │  │      ║
║  ──────────────────────────────────────────────   ║
║                                                    ║
║  a  b  c  d  e  f  g    h  i  j  k  l  m  n      ║
║  ─────────────────────────────────────────────── ║
║                                                    ║
║ A│ ●  ●  ●  ●  ●  ●  ● │ ●  ●  ●  ●  ●  ●  ●  │
║  │                      │                        │
║ B│ ●──●──●  ●  ●  ●  ● │ ●  ●  ●  ●  ●  ●  ●  │
║  │                      │                        │
║ C│ ●  ●  ●  ●  ●  ●  ● │ ●  ●  ●  ●  ●  ●  ●  │
║  │                      │                        │
║ D│ ●  ●  ●──●  ●  ●  ● │ ●  ●  ●  ●  ●  ●  ●  │
║  │                      │                        │
║ E│ ●  ●  ●  ●  ●  ●  ● │ ●  ●  ●  ●  ●  ●  ●  │
║  │                      │                        │
║ F│ ●  ●  ●  ●  ●  ●  ● │ ●  ●  ●  ●  ●  ●  ●  │
║  │                      │                        │
║ G│ ●  ●  ●  ●  ●  ●  ● │ ●  ●  ●  ●  ●  ●  ●  │
║  │                      │                        │
║ H│ ●  ●  ●  ●  ●  ●  ● │ ●  ●  ●  ●  ●  ●  ●  │
║  ──────────────────────────────────────────────── ║
║                                                    ║
║ Legend:                                            ║
║ ● = Hole                                           ║
║ ─ = Wire Connection                                ║
║ ──● = Connection Made                              ║
║                                                    ║
╠════════════════════════════════════════════════════╣
║           CONNECTIONS TO MAKE:                     ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║ 1. Arduino Pin 10 ─→ Resistor (Row A-b)          ║
║    Resistor ─→ Green LED Anode (+)                ║
║    Green LED Cathode (-) ─→ GND Rail              ║
║                                                    ║
║ 2. Arduino Pin 11 ─→ Resistor (Row D-b)          ║
║    Resistor ─→ Red LED Anode (+)                  ║
║    Red LED Cathode (-) ─→ GND Rail                ║
║                                                    ║
║ 3. Arduino GND ─→ GND Rail (Blue -)               ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

## Photo-Style Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  TOP VIEW - Breadboard with Arduino                        │
│                                                             │
│     ARDUINO UNO (at top, connected via jumpers)            │
│     ┌──────────────────────────┐                           │
│     │ GND │ Pin 10 │ Pin 11 │  │                           │
│     └──┬──────┬─────────┬────┘  │                           │
│        │      │         │                                   │
│        │      │         │                                   │
│  ┌─────┴──────┴────┬────┴────────────────────┐             │
│  │                │                         │             │
│  │  BREADBOARD    │                         │             │
│  │                │                         │             │
│  │  Row A         │                         │             │
│  │  (220Ω)    ┌───┴───┐                     │             │
│  │     →      │🟢     │ Green LED            │             │
│  │            │       │                     │             │
│  │  Row D     │       ├─→ GND                │             │
│  │  (220Ω)    └───────┘                     │             │
│  │     →      ┌───────┐                     │             │
│  │            │🔴     │ Red LED              │             │
│  │            │       │                     │             │
│  │            │       ├─→ GND                │             │
│  │            └───────┘                     │             │
│  │                                          │             │
│  │  GND Rail ←── GND from both LEDs ← Arduino GND         │
│  │                                          │             │
│  └──────────────────────────────────────────┘             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Resistor Placement Detail

```
How to insert 220Ω resistor properly:

    [Wire from Arduino]
            │
            └──┬────┐
               │ R  │ ← 220Ω Resistor
            ┌──┴────┴──┐
            │ Breadboard│
            └───────────┘
                 │
         ┌───────┘
         │
         └─→ [Wire to LED Anode]


Visual on Breadboard:

     Hole A    Hole B    Hole C    Hole D
     ────      ────      ────      ────
    |  ●  |  |  ●  |  |  ●  |  |  ●  |
    
    Connect:  A ─ B  (Resistor)
              B ─ C  (Wire to LED +)
              C ─ LED Anode


Correct LED Orientation:

    🟢 Green LED              Red LED 🔴
    
    Long Leg (+) ─ Anode      Long Leg (+) ─ Anode
    Short Leg (-) ─ Cathode   Short Leg (-) ─ Cathode
    
    Must be inserted upright with:
    - Long leg toward resistor (anode)
    - Short leg toward GND (cathode)
```

## Current Flow Diagram

```
POSITIVE EMOTION (Green LED Active):

Arduino (5V) → Pin 10 → [220Ω Resistor] → Green LED Anode (+)
                                           ↓
                                     Green LED Interior
                                           ↓
                                    Green LED Cathode (-)
                                           ↓
                                   Breadboard GND Rail
                                           ↓
                                   Arduino GND (Reference)

Result: Electron flow causes green light to emit


NEGATIVE EMOTION (Red LED Active):

Arduino (5V) → Pin 11 → [220Ω Resistor] → Red LED Anode (+)
                                           ↓
                                     Red LED Interior
                                           ↓
                                    Red LED Cathode (-)
                                           ↓
                                   Breadboard GND Rail
                                           ↓
                                   Arduino GND (Reference)

Result: Electron flow causes red light to emit


NEUTRAL EMOTION (Both LEDs Alternating):

Pin 10 & Pin 11 alternate on/off pattern:
- Phase 1: Pin 10 ON, Pin 11 OFF   → 🟢 Green
- Phase 2: Pin 10 OFF, Pin 11 ON   → 🔴 Red
- Phase 3: Pin 10 ON, Pin 11 OFF   → 🟢 Green
- Repeat at specified frequency (default 1 Hz)
```

## Pin Voltage Levels

```
Arduino Pin Logic States:

PIN STATE          VOLTAGE    LED BEHAVIOR
────────────────────────────────────────
digitalRead(10) = HIGH   5V → Green LED ON
digitalRead(10) = LOW    0V → Green LED OFF

digitalRead(11) = HIGH   5V → Red LED ON
digitalRead(11) = LOW    0V → Red LED OFF


Typical Operating Conditions:

Component              Voltage    Current
────────────────────────────────────────
Arduino Pin Output     5V         40mA (max)
220Ω Resistor          ~1.8V      ~18mA
LED Forward Voltage    ~2V        ~18mA (typical)
Total Voltage Drop     ~3.8V ✓ (within 5V)

⚠️ Important: Never exceed 20mA per LED!
             220Ω resistor ensures this limit.
```

## Troubleshooting Connection Points

```
Check these connections if LED doesn't work:

1. Arduino Pin → Resistor
   ├─ Use multimeter (should read ~5V when ON)
   ├─ Check for loose jumper wire
   └─ Verify pin number (10 or 11)

2. Resistor → LED Anode
   ├─ Resistor should touch LED long leg
   ├─ Use multimeter (should read ~3.2V when ON)
   └─ Check resistor value (220Ω ± 5%)

3. LED Cathode → GND
   ├─ LED short leg must touch GND rail
   ├─ Use multimeter (should read 0V)
   └─ Verify continuity to Arduino GND

4. Arduino GND → Breadboard GND
   ├─ Critical reference point
   ├─ Use multimeter between both grounds (should read 0Ω)
   └─ Ensure solid connection

5. Power Supply
   ├─ Check USB cable connection
   ├─ Verify Arduino power light is on
   └─ Monitor Serial output for errors
```

## Safety Notes

```
⚠️ IMPORTANT PRECAUTIONS:

1. Power OFF Arduino before making connections
2. Check polarity of LEDs before inserting
3. Do NOT exceed 20mA per LED
4. Use correct resistor value (220Ω minimum)
5. Do NOT connect Pin to GND directly (short circuit)
6. Do NOT apply reverse voltage to LEDs
7. Do NOT touch components during operation
8. Do NOT exceed Arduino 5V rating
9. Use USB power only (not external power)
10. Test each connection before full system power-on

✅ Safe Operation Verified:
   └─ 220Ω resistor limits current to ~18mA ✓
   └─ 5V Arduino supply is safe ✓
   └─ Breadboard provides safe testing ✓
```

---

This completes your two-LED implementation with detailed connection guidance!
