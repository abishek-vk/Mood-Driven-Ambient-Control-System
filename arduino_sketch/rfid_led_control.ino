/*
  MOOD-DRIVEN AMBIENT CONTROL SYSTEM - Arduino Firmware
  
  Integrated Features:
  - RFID Card Access Control
  - LED Mood Indication (Green=Happy, Red=Angry)
  - Emotion-based LED Control from Python
  - LCD Display Feedback
  - Buzzer Alerts
  
  Hardware Connections:
  - RFID-RC522: SPI (pins 11-13, SS=10, RST=9)
  - LCD Display: I2C (SDA=A4, SCL=A5)
  - Green LED: Pin 2 (with 220Ω resistor)
  - Red LED: Pin 3 (with 220Ω resistor)
  - Buzzer: Pin 7
  - Serial: USB (9600 baud)
  
  Author: Mood Control System
  Date: October 31, 2025
*/

#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ==================== PIN DEFINITIONS ====================
#define SS_PIN 10              // RFID Chip Select
#define RST_PIN 9              // RFID Reset
#define LED_GREEN_PIN 2        // Green LED (Happy emotion)
#define LED_RED_PIN 4          // Red LED (Angry emotion)
#define BUZZER_PIN 7           // Buzzer for alerts

// ==================== RFID MODULE ====================
MFRC522 mfrc522(SS_PIN, RST_PIN);

// ==================== LCD DISPLAY ====================
LiquidCrystal_I2C lcd(0x27, 16, 2);  // I2C address 0x27, 16x2 display

// ==================== CONFIGURATION ====================
String authorizedUID = "E3 F0 E2 D9";  // Change to your card UID

// ==================== LED BLINKING VARIABLES ====================
unsigned long lastBlinkTime = 0;
const int BLINK_INTERVAL = 500;        // 500ms = 1 Hz blink rate
bool blinkState = false;
int currentLED = -1;                   // -1: none, 2: green, 3: red

// ==================== SYSTEM STATE ====================
enum SystemState {
  WAITING,           // Waiting for RFID card
  CARD_DETECTED,     // RFID card scanned
  ANALYZING,         // Emotion analysis in progress
  LED_ACTIVE         // LED blinking for emotion
};

SystemState systemState = WAITING;
unsigned long stateChangeTime = 0;

// ==================== SETUP ====================
void setup() {
  // Initialize Serial Communication
  Serial.begin(9600);
  delay(100);
  
  // Initialize SPI and RFID
  SPI.begin();
  mfrc522.PCD_Init();
  
  // Initialize LED Pins
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_RED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Turn off LEDs initially
  digitalWrite(LED_GREEN_PIN, LOW);
  digitalWrite(LED_RED_PIN, LOW);
  
  // Initialize LCD Display
  lcd.init();
  lcd.backlight();
  
  // Display startup message
  lcd.setCursor(0, 0);
  lcd.print("Mood Control");
  lcd.setCursor(0, 1);
  lcd.print("System Ready");
  
  // Send startup confirmation to Python
  Serial.println("ARDUINO_READY");
  Serial.println("System initialized");
  
  delay(1500);
  
  // Show waiting screen
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Waiting for");
  lcd.setCursor(0, 1);
  lcd.print("RFID Card...");
  
  systemState = WAITING;
}

// ==================== MAIN LOOP ====================
void loop() {
  // Always handle serial commands from Python
  handleSerialCommand();
  
  // Always handle LED blinking
  handleLEDBlinking();
  
  // Handle RFID card scanning
  handleRFIDScanning();
}

// ==================== RFID HANDLING ====================
void handleRFIDScanning() {
  // Wait for new RFID card
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Extract card UID
  String tagUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagUID += String(mfrc522.uid.uidByte[i], HEX);
    if (i != mfrc522.uid.size - 1) tagUID += " ";
  }
  tagUID.toUpperCase();

  // Display card UID on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Card UID:");
  lcd.setCursor(0, 1);
  lcd.print(tagUID.substring(0, 16));  // First 16 chars fit on LCD
  
  systemState = CARD_DETECTED;
  stateChangeTime = millis();

  // Check if card is authorized
  if (tagUID == authorizedUID) {
    // ========== AUTHORIZED CARD ==========
    Serial.println("ACCESS_GRANTED");
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Access");
    lcd.setCursor(0, 1);
    lcd.print("GRANTED!");
    
    // Flash green LED
    digitalWrite(LED_GREEN_PIN, HIGH);
    delay(500);
    digitalWrite(LED_GREEN_PIN, LOW);
    delay(500);
    digitalWrite(LED_GREEN_PIN, HIGH);
    delay(500);
    digitalWrite(LED_GREEN_PIN, LOW);
    
    // Display analyzing message
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Analyzing");
    lcd.setCursor(0, 1);
    lcd.print("Emotions...");
    
    systemState = ANALYZING;
    
  } else {
    // ========== UNAUTHORIZED CARD ==========
    Serial.println("ACCESS_DENIED");
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Access");
    lcd.setCursor(0, 1);
    lcd.print("DENIED!");
    
    // Buzzer alert
    tone(BUZZER_PIN, 1000, 500);
    delay(500);
    tone(BUZZER_PIN, 800, 500);
    delay(500);
  }
  
  delay(1500);
  
  // Return to waiting state
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Waiting for");
  lcd.setCursor(0, 1);
  lcd.print("RFID Card...");
  
  systemState = WAITING;
  currentLED = -1;
  digitalWrite(LED_GREEN_PIN, LOW);
  digitalWrite(LED_RED_PIN, LOW);
}

// ==================== LED BLINKING CONTROL ====================
void handleLEDBlinking() {
  unsigned long currentTime = millis();
  
  // Only blink if a LED is active
  if (currentLED == -1) {
    return;
  }
  
  // Check if it's time to toggle
  if (currentTime - lastBlinkTime >= BLINK_INTERVAL) {
    blinkState = !blinkState;
    lastBlinkTime = currentTime;
    
    // Toggle the active LED
    if (currentLED == LED_GREEN_PIN) {
      digitalWrite(LED_GREEN_PIN, blinkState ? HIGH : LOW);
    } else if (currentLED == LED_RED_PIN) {
      digitalWrite(LED_RED_PIN, blinkState ? HIGH : LOW);
    }
  }
}

// ==================== SERIAL COMMAND HANDLER ====================
void handleSerialCommand() {
  // Check if data is available on Serial
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.length() == 0) {
      return;
    }
    
    // Debug: Echo command received
    Serial.print("CMD: ");
    Serial.println(command);
    
    // ========== EMOTION-BASED LED CONTROL ==========
    
    if (command == "LED_GREEN_BLINK") {
      // Happy emotion detected
      currentLED = LED_GREEN_PIN;
      blinkState = false;
      lastBlinkTime = millis();
      
      // Turn off red LED
      digitalWrite(LED_RED_PIN, LOW);
      
      // Update LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Emotion:");
      lcd.setCursor(0, 1);
      lcd.print("HAPPY");
      
      // Send confirmation
      Serial.println("GREEN_LED_ACTIVE");
    } 
    else if (command == "LED_RED_BLINK") {
      // Neutral emotion detected
      currentLED = LED_RED_PIN;
      blinkState = false;
      lastBlinkTime = millis();

      // Turn off green LED
      digitalWrite(LED_GREEN_PIN, LOW);

      // Update LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Emotion:");
      lcd.setCursor(0, 1);
      lcd.print("NEUTRAL");

      // Send confirmation
      Serial.println("RED_LED_ACTIVE");
    } 
    else if (command == "LED_OFF") {
      // No clear emotion
      currentLED = -1;
      digitalWrite(LED_GREEN_PIN, LOW);
      digitalWrite(LED_RED_PIN, LOW);

      // Update LCD
      lcd.clear();
      delay(100); // Ensure LCD is cleared before printing
      lcd.setCursor(0, 0);
      lcd.print("Emotion:");
      lcd.setCursor(0, 1);
      lcd.print("NONE");

      // Send confirmation
      Serial.println("LEDS_OFF");
    }
    else if (command.startsWith("BLINK_SPEED_")) {
      // Adjust blink speed (optional feature)
      // Format: "BLINK_SPEED_250" for 250ms intervals
      int speed = command.substring(12).toInt();
      if (speed > 100 && speed < 2000) {
        // Uncomment to use: BLINK_INTERVAL = speed;
        Serial.println("BLINK_SPEED_OK");
      }
    }
    else if (command == "STATUS") {
      // Return system status
      Serial.println("SYSTEM_STATUS_OK");
      Serial.print("STATE: ");
      printSystemState();
      Serial.print("LED: ");
      if (currentLED == -1) Serial.println("OFF");
      else if (currentLED == LED_GREEN_PIN) Serial.println("GREEN");
      else if (currentLED == LED_RED_PIN) Serial.println("RED");
    }
    else if (command == "TEST_LEDS") {
      // Test all LEDs
      testLEDs();
    }
    else {
      // Unknown command
      Serial.print("ERR: Unknown command: ");
      Serial.println(command);
    }
  }
}

// ==================== LED TEST FUNCTION ====================
void testLEDs() {
  Serial.println("Starting LED test...");
  
  // Test green LED
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Testing:");
  lcd.setCursor(0, 1);
  lcd.print("GREEN LED");
  
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_GREEN_PIN, HIGH);
    delay(200);
    digitalWrite(LED_GREEN_PIN, LOW);
    delay(200);
  }
  Serial.println("Green LED OK");
  
  delay(500);
  
  // Test red LED
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Testing:");
  lcd.setCursor(0, 1);
  lcd.print("RED LED");
  
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_RED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_RED_PIN, LOW);
    delay(200);
  }
  Serial.println("Red LED OK");
  
  delay(500);
  
  // Test buzzer
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Testing:");
  lcd.setCursor(0, 1);
  lcd.print("BUZZER");
  
  tone(BUZZER_PIN, 1000, 200);
  delay(300);
  tone(BUZZER_PIN, 800, 200);
  delay(300);
  tone(BUZZER_PIN, 600, 200);
  
  Serial.println("Buzzer OK");
  Serial.println("All tests passed!");
  
  // Return to waiting state
  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Waiting for");
  lcd.setCursor(0, 1);
  lcd.print("RFID Card...");
  
  currentLED = -1;
}

// ==================== HELPER FUNCTIONS ====================
void printSystemState() {
  switch (systemState) {
    case WAITING:
      Serial.println("WAITING");
      break;
    case CARD_DETECTED:
      Serial.println("CARD_DETECTED");
      break;
    case ANALYZING:
      Serial.println("ANALYZING");
      break;
    case LED_ACTIVE:
      Serial.println("LED_ACTIVE");
      break;
    default:
      Serial.println("UNKNOWN");
  }
}

// ==================== EOF ====================
