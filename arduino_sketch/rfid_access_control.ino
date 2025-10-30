#include <LiquidCrystal.h>

#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SS_PIN 10
#define RST_PIN 9
#define LED_PIN 6
#define BUZZER_PIN 7

MFRC522 mfrc522(SS_PIN, RST_PIN);
LiquidCrystal_I2C lcd(0x27, 16, 2); // adjust address if needed

String authorizedUID = "E3 F0 E2 D9";  // change to your card UID

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0,0);
  lcd.print(" Mood Control ");
  lcd.setCursor(0,1);
  lcd.print("  Waiting...  ");
}

void loop() {
  // Wait for new RFID card
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) return;

  String tagUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagUID += String(mfrc522.uid.uidByte[i], HEX);
    if (i != mfrc522.uid.size - 1) tagUID += " ";
  }
  tagUID.toUpperCase();

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Card UID:");
  lcd.setCursor(0,1);
  lcd.print(tagUID);

  if (tagUID == authorizedUID) {
    Serial.println("ACCESS_GRANTED");
    lcd.clear();
    lcd.print("Access Granted!");
    digitalWrite(LED_PIN, HIGH);
    delay(1000);
    digitalWrite(LED_PIN, LOW);
  } else {
    Serial.println("ACCESS_DENIED");
    lcd.clear();
    lcd.print("Access Denied!");
    tone(BUZZER_PIN, 1000);
    delay(1000);
    noTone(BUZZER_PIN);
  }
  delay(1500);
  lcd.clear();
  lcd.print("Waiting...");
}