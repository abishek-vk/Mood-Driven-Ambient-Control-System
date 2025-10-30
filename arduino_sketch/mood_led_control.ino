/*
  MOOD-DRIVEN AMBIENT CONTROL SYSTEM - Arduino Sketch
  
  Controls 2 LEDs based on emotion detection signals from Python
  
  Connections:
  - LED 1 (Positive Mood - Green): Pin 10 with 220Ω resistor
  - LED 2 (Negative Mood - Red): Pin 11 with 220Ω resistor
  - GND: Ground
  
  Commands from Python (via Serial):
  - ALL_OFF              : Turn off both LEDs
  - PIN_10_ON            : Turn ON LED1 (solid)
  - PIN_10_OFF           : Turn OFF LED1
  - PIN_10_BLINK_2       : Blink LED1 at 2 Hz
  - PIN_11_ON            : Turn ON LED2 (solid)
  - PIN_11_OFF           : Turn OFF LED2
  - PIN_11_BLINK_2       : Blink LED2 at 2 Hz
  - BOTH_BLINK_ALT_1     : Both blink alternately at 1 Hz
*/

#define LED1_PIN 10  // Positive mood LED (Green)
#define LED2_PIN 11  // Negative mood LED (Red)

// Blink states for each LED
struct LEDState {
  int pin;
  bool isOn;
  bool isBlinking;
  int blinkFrequency;  // Hz
  unsigned long lastToggleTime;
  bool currentBlinkState;  // For tracking blink state
};

LEDState led1 = {LED1_PIN, false, false, 0, 0, false};
LEDState led2 = {LED2_PIN, false, false, 0, 0, false};

bool alternateBlink = false;
int alternateFrequency = 1;
unsigned long lastAlternateToggle = 0;

void setup() {
  // Initialize pins
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  
  // Turn off LEDs initially
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);
  
  // Start serial communication
  Serial.begin(9600);
  
  // Send startup message
  Serial.println("READY");
  Serial.println("Arduino Mood-Driven LED Control Ready");
}

void loop() {
  // Handle serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.length() > 0) {
      processCommand(command);
    }
  }
  
  // Update LED states (handle blinking)
  updateLEDs();
  
  delay(10);  // Small delay to prevent overwhelming the loop
}

void processCommand(String command) {
  Serial.print("CMD: ");
  Serial.println(command);
  
  if (command == "ALL_OFF") {
    allLEDsOff();
  }
  else if (command == "PIN_10_ON") {
    setLEDState(&led1, true, false, 0);
  }
  else if (command == "PIN_10_OFF") {
    setLEDState(&led1, false, false, 0);
  }
  else if (command == "PIN_11_ON") {
    setLEDState(&led2, true, false, 0);
  }
  else if (command == "PIN_11_OFF") {
    setLEDState(&led2, false, false, 0);
  }
  else if (command.startsWith("PIN_10_BLINK_")) {
    int frequency = extractFrequency(command);
    setLEDState(&led1, false, true, frequency);
  }
  else if (command.startsWith("PIN_11_BLINK_")) {
    int frequency = extractFrequency(command);
    setLEDState(&led2, false, true, frequency);
  }
  else if (command.startsWith("BOTH_BLINK_ALT_")) {
    int frequency = extractFrequency(command);
    alternateBlink = true;
    alternateFrequency = frequency;
    setLEDState(&led1, false, false, 0);
    setLEDState(&led2, false, false, 0);
    Serial.print("Alternating blink mode at ");
    Serial.print(frequency);
    Serial.println(" Hz");
  }
  else {
    Serial.println("ERR: Unknown command");
  }
}

void setLEDState(LEDState* led, bool on, bool blinking, int frequency) {
  led->isOn = on;
  led->isBlinking = blinking;
  led->blinkFrequency = frequency;
  led->lastToggleTime = millis();
  led->currentBlinkState = false;
  alternateBlink = false;
  
  if (on && !blinking) {
    digitalWrite(led->pin, HIGH);
    Serial.print("LED ");
    Serial.print(led->pin);
    Serial.println(" ON");
  } else if (!on && !blinking) {
    digitalWrite(led->pin, LOW);
    Serial.print("LED ");
    Serial.print(led->pin);
    Serial.println(" OFF");
  }
}

void allLEDsOff() {
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);
  led1.isOn = false;
  led1.isBlinking = false;
  led2.isOn = false;
  led2.isBlinking = false;
  alternateBlink = false;
  Serial.println("All LEDs OFF");
}

void updateLEDs() {
  unsigned long currentTime = millis();
  
  // Handle alternating blink mode (both LEDs blink opposite)
  if (alternateBlink) {
    int toggleInterval = 1000 / alternateFrequency / 2;  // Half period
    
    if (currentTime - lastAlternateToggle >= toggleInterval) {
      led1.currentBlinkState = !led1.currentBlinkState;
      led2.currentBlinkState = !led1.currentBlinkState;  // Opposite
      
      digitalWrite(LED1_PIN, led1.currentBlinkState ? HIGH : LOW);
      digitalWrite(LED2_PIN, led2.currentBlinkState ? HIGH : LOW);
      
      lastAlternateToggle = currentTime;
    }
  } else {
    // Handle individual LED blinking
    updateLEDBlinking(&led1, currentTime);
    updateLEDBlinking(&led2, currentTime);
  }
}

void updateLEDBlinking(LEDState* led, unsigned long currentTime) {
  if (!led->isBlinking || led->blinkFrequency == 0) {
    return;
  }
  
  // Calculate toggle interval in milliseconds
  int toggleInterval = 500 / led->blinkFrequency;  // 500ms per full cycle
  
  if (currentTime - led->lastToggleTime >= toggleInterval) {
    led->currentBlinkState = !led->currentBlinkState;
    digitalWrite(led->pin, led->currentBlinkState ? HIGH : LOW);
    led->lastToggleTime = currentTime;
  }
}

int extractFrequency(String command) {
  // Extract frequency from commands like "PIN_10_BLINK_2" or "BOTH_BLINK_ALT_1"
  int lastUnderscore = command.lastIndexOf('_');
  String freqString = command.substring(lastUnderscore + 1);
  int frequency = freqString.toInt();
  
  // Constrain frequency to reasonable values
  if (frequency < 1) frequency = 1;
  if (frequency > 10) frequency = 10;
  
  return frequency;
}
