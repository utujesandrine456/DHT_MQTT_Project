#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

String name = "UWASE UTUJE Sandrine  ";
int pos = 0;

unsigned long lastScroll = 0;
unsigned long lastTemp = 0;
float temp = 0;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  dht.begin();
}

void loop() {

  if (millis() - lastTemp > 2000) {
    lastTemp = millis();

    float t = dht.readTemperature();

    if (!isnan(t)) {
      temp = t;
    }

    Serial.println(temp);
  }

  if (name.length() <= 16) {

    lcd.setCursor(0, 0);
    lcd.print(name);

    for (int i = name.length(); i < 16; i++) {
      lcd.print(" ");
    }

  } 
  else {

    if (millis() - lastScroll > 200) {
      lastScroll = millis();

      lcd.setCursor(0, 0);

      String line = "";

      for (int i = 0; i < 16; i++) {
        line += name[(pos + i) % name.length()];
      }

      lcd.print(line);

      pos++;
      if (pos >= name.length()) pos = 0;
    }
  }

  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(temp);
  lcd.print(" C   ");

  delay(500);
}