# 🎭 Mood-Driven Ambient Control System

An intelligent IoT system that detects human emotions in real-time using facial recognition and controls ambient LED lighting through Arduino, creating an interactive mood-responsive environment.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

This project combines computer vision, deep learning, and IoT to create an ambient control system that responds to human emotions. The system:
- Detects faces using advanced computer vision techniques
- Recognizes emotions using a pre-trained deep learning model
- Controls LED lighting via Arduino based on detected mood
- Supports RFID integration for access control
- Provides real-time feedback with minimal latency

## ✨ Features

### 🎯 Core Capabilities
- **Real-time Emotion Detection**: Detects 7 emotions (Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral)
- **Smart LED Control**: Two-LED system responds to positive/negative moods
- **RFID Integration**: Optional access control and user identification
- **Multiple Execution Modes**: Simple, synchronous, and asynchronous operation
- **Arduino Integration**: Serial communication for hardware control
- **Configurable Settings**: Easy customization via config file

### 🔧 Technical Features
- Advanced face detection (MTCNN/OpenCV Haar Cascades)
- Pre-trained emotion recognition model (mini_XCEPTION on FER2013)
- Optimized for performance with minimal dependencies
- Cross-platform compatibility (Windows/Linux/macOS)

## 🏗️ System Architecture

```
┌─────────────────┐
│   Webcam Input  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Face Detection  │
│   (OpenCV/      │
│    MTCNN)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Emotion Model   │
│ (TensorFlow/    │
│  Keras)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Mood Mapping   │
│ (Positive/      │
│  Negative)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────┐
│ Serial Comm     │────▶│   Arduino   │
│ (Python-Arduino)│     └──────┬──────┘
└─────────────────┘            │
                               ▼
                         ┌─────────────┐
                         │  LED Control│
                         │ (2 LEDs)    │
                         └─────────────┘
```

## 🔌 Hardware Requirements

### Essential Components
- **Webcam**: Built-in or USB webcam for facial capture
- **Arduino Board**: Arduino Uno/Nano/Mega (recommended: Uno R3)
- **LEDs**: 2x LEDs (suggested: Green for positive, Red for negative)
- **Resistors**: 2x 220Ω resistors (for LED protection)
- **Connecting Wires**: Jumper wires for breadboard connections
- **Breadboard**: For prototyping (optional but recommended)

### Optional Components
- **RFID Reader**: MFRC522 module for access control
- **RFID Tags/Cards**: For user identification
- **USB Cable**: For Arduino-PC connection

### Wiring Guide
```
Arduino Pin Layout:
- Pin 10 → Positive Mood LED (Green) + 220Ω Resistor → GND
- Pin 11 → Negative Mood LED (Red) + 220Ω Resistor → GND
- GND → Common Ground
```

## 💻 Software Requirements

### Python Environment
- **Python**: 3.7 - 3.11 (recommended: 3.9)
- **Operating System**: Windows 10/11, Linux, macOS

### Key Dependencies
- `opencv-python`: Computer vision and face detection
- `tensorflow`: Deep learning framework for emotion recognition
- `numpy`: Numerical computing
- `pyserial`: Arduino serial communication
- `mtcnn`: Advanced face detection (optional)

See `requirements.txt` for complete dependency list.

## 🚀 Installation

### Step 1: Clone the Repository
```powershell
git clone https://github.com/abishek-vk/Mood-Driven-Ambient-Control-System.git
cd Mood-Driven-Ambient-Control-System
```

### Step 2: Set Up Python Environment
```powershell
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Download Emotion Model
Download the pre-trained emotion model:
- **Model**: `emotion_model.h5` (mini_XCEPTION trained on FER2013)
- **Source**: [oarriaga/face_classification](https://github.com/oarriaga/face_classification)
- **Location**: Place in `models/` directory

### Step 4: Arduino Setup
1. Open Arduino IDE
2. Upload the appropriate sketch:
   - **LED Only**: `arduino_sketch/mood_led_control.ino`
   - **RFID + LED**: `arduino_sketch/rfid_led_control.ino`
   - **Test Sketch**: `arduino_sketch/simple_led_test/simple_led_test.ino`
3. Note the COM port (e.g., COM3, /dev/ttyUSB0)

### Step 5: Configure Serial Port
Edit `config.ini`:
```ini
[Serial]
port = COM3          # Change to your Arduino port
baudrate = 9600
timeout = 1
```

## 🎮 Usage

### Quick Start
```powershell
# Simple emotion detection (no Arduino)
python src/main.py

# With LED control (requires Arduino)
python run_simple.py

# With emotion detection and LED control
python run_with_emotions.py

# Asynchronous mode (best performance)
python run_with_emotions_async.py
```

### Testing Components

#### Test Arduino Connection
```powershell
python test_arduino.py
```

#### Test LED Control
```powershell
python test_mood_led.py
```

#### Test Serial Communication
```powershell
python test_serial_direct.py
```

#### System Integration Test
```powershell
python test_system.py
```

#### Troubleshoot Arduino
```powershell
python troubleshoot_arduino.py
```

### Controls
- **'q'**: Quit the application
- **'s'**: Take screenshot (if enabled)
- **ESC**: Emergency exit

## 📁 Project Structure

```
Mood-Driven-Ambient-Control-System/
├── src/                              # Source code
│   ├── main.py                       # Main application entry
│   ├── face_detector_advanced.py     # Face detection module
│   ├── emotion_detector.py           # Emotion recognition module
│   ├── led_control.py                # LED controller
│   ├── rfid_emotion_integration.py   # RFID integration
│   └── rfid_emotion_led_control.py   # Combined RFID+LED control
│
├── arduino_sketch/                   # Arduino firmware
│   ├── mood_led_control.ino          # LED control sketch
│   ├── rfid_led_control.ino          # RFID + LED sketch
│   ├── rfid_access_control.ino       # RFID only sketch
│   └── simple_led_test/              # LED test sketch
│
├── models/                           # ML models
│   └── emotion_model.h5              # Pre-trained emotion model
│
├── music/                            # Optional audio files
│
├── run_simple.py                     # Simple execution mode
├── run_with_emotions.py              # Standard execution
├── run_with_emotions_async.py        # Async execution (fastest)
│
├── test_arduino.py                   # Arduino connectivity test
├── test_mood_led.py                  # LED functionality test
├── test_serial_direct.py             # Serial communication test
├── test_system.py                    # Full system test
├── troubleshoot_arduino.py           # Diagnostic tool
│
├── config.ini                        # Configuration file
├── requirements.txt                  # Python dependencies
├── LICENSE                           # MIT License
└── README.md                         # This file
```

## ⚙️ Configuration

### config.ini Settings
```ini
[Serial]
port = COM3                # Arduino serial port
baudrate = 9600           # Communication speed
timeout = 1               # Read timeout (seconds)

[Detection]
cascade = haarcascade_frontalface_default.xml
scale_factor = 1.1
min_neighbors = 5
min_size = 30

[LED]
positive_pin = 10         # Pin for positive mood LED
negative_pin = 11         # Pin for negative mood LED
```

### Emotion-to-Mood Mapping
- **Positive Mood**: Happy, Surprise → Green LED
- **Negative Mood**: Sad, Angry, Fear, Disgust → Red LED
- **Neutral**: Alternating pattern or both OFF

## 🔧 Troubleshooting

### Camera Issues
- Ensure webcam is connected and not in use by other applications
- Check camera permissions in system settings
- Try changing camera index in code (0, 1, 2)

### Arduino Connection Issues
- Verify correct COM port in `config.ini`
- Close Arduino IDE Serial Monitor (conflicts with Python)
- Check USB cable and try different ports
- Ensure Arduino drivers are installed

### Model Loading Issues
- Verify `emotion_model.h5` is in `models/` directory
- Check TensorFlow installation: `pip install tensorflow`
- Ensure compatible Python version (3.7-3.11)

### LED Not Responding
- Check wiring connections
- Verify correct pin numbers in code and Arduino sketch
- Test LEDs with `test_mood_led.py`
- Measure voltage across LED (should be ~2-3V)

### Performance Issues
- Use `run_with_emotions_async.py` for better performance
- Reduce camera resolution in code
- Close unnecessary background applications
- Consider using GPU acceleration for TensorFlow

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit changes**: `git commit -m 'Add AmazingFeature'`
4. **Push to branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Emotion Model**: Pre-trained model from [oarriaga/face_classification](https://github.com/oarriaga/face_classification)
- **Dataset**: FER2013 emotion recognition dataset
- **Libraries**: OpenCV, TensorFlow, PySerial communities

## 📧 Contact

**Project Author**: Abishek VK  
**Repository**: [Mood-Driven-Ambient-Control-System](https://github.com/abishek-vk/Mood-Driven-Ambient-Control-System)

---

**⭐ If you find this project useful, please consider giving it a star!**