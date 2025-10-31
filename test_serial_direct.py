#!/usr/bin/env python
"""
Direct serial test - send commands directly to Arduino
"""
import serial
import serial.tools.list_ports
import time

def find_arduino():
    """Find Arduino COM port"""
    ports = serial.tools.list_ports.comports()
    
    print("Available COM ports:")
    for port in ports:
        print(f"  - {port.device}: {port.description}")
    
    arduino_port = None
    for port in ports:
        desc = port.description.upper()
        if 'ARDUINO' in desc:
            arduino_port = port.device
            print(f"\n✓ Found Arduino at: {port.device}")
            break
        elif 'CH340' in desc and not arduino_port:
            arduino_port = port.device
    
    return arduino_port

# Find and connect to Arduino
port = find_arduino()
if not port:
    print("No Arduino found!")
    exit(1)

print(f"Connecting to {port}...")
try:
    ser = serial.Serial(port, 9600, timeout=1)
    time.sleep(2)
    ser.reset_input_buffer()
    
    print("✓ Connected!\n")
    
    # Test commands
    commands = [
        "LED_GREEN_BLINK",
        "LED_NEUTRAL_BLINK",
        "LED_RED_BLINK",
        "STATUS"
    ]
    
    for cmd in commands:
        print(f"Sending: {cmd}")
        ser.write((cmd + '\n').encode())
        ser.flush()
        time.sleep(0.5)
        
        # Read response
        while ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            if response:
                print(f"  Response: {response}")
        
        time.sleep(1)
    
    ser.close()
    print("\n✓ Test completed!")
    
except Exception as e:
    print(f"Error: {e}")
