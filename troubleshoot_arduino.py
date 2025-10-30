#!/usr/bin/env python
"""
Arduino Connection Troubleshooter
Helps diagnose Arduino connection issues
"""

import serial
import serial.tools.list_ports
import time

print("="*70)
print("ARDUINO CONNECTION TROUBLESHOOTER")
print("="*70)

print("\n[Step 1] Checking available COM ports...")
ports = serial.tools.list_ports.comports()

if not ports:
    print("❌ NO COM PORTS FOUND!")
    print("\nPossible solutions:")
    print("  1. Connect Arduino via USB cable")
    print("  2. Install Arduino drivers (CH340, FTDI, etc.)")
    print("  3. Check Device Manager for unknown devices")
    print("  4. Try different USB cable")
    exit()

print(f"Found {len(ports)} COM port(s):\n")
for i, port in enumerate(ports, 1):
    print(f"{i}. {port.device}")
    print(f"   Description: {port.description}")
    print(f"   Hardware ID: {port.hwid}")
    print()

print("[Step 2] Attempting to connect to each port...")
print()

for port in ports:
    print(f"Trying {port.device}...")
    try:
        ser = serial.Serial(port.device, 9600, timeout=2)
        time.sleep(2)  # Wait for Arduino to initialize
        
        # Try to read data
        if ser.in_waiting > 0:
            data = ser.readline()
            print(f"  ✅ Connected!")
            print(f"  Data received: {data}")
            ser.close()
            
            print(f"\n✅ SUCCESS! Arduino is on {port.device}")
            print(f"Use this port in your configuration")
            exit()
        else:
            print(f"  ⚠️  Connected but no data received")
            print(f"  (Arduino might be in idle state)")
            ser.close()
    
    except serial.SerialException as e:
        print(f"  ❌ Connection failed: {e}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "="*70)
print("TROUBLESHOOTING CHECKLIST:")
print("="*70)
print("□ Arduino is connected via USB cable")
print("□ Arduino driver is installed (check Device Manager)")
print("□ No other program is using the COM port")
print("□ Arduino sketch is uploaded and running")
print("□ Arduino is powered on")
print("□ Try a different USB cable")
print("□ Try a different USB port on your computer")
print("□ Restart the Arduino (press reset button)")
print("\n" + "="*70)
