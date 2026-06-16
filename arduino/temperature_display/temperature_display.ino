#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

const int tempPin = A0;

String candidateName = "John Doe - Embedded Systems Candidate  "; 
int nameLength;
int scrollPosition = 0;

unsigned long previousMillis = 0;
const long scrollInterval = 400;

void setup() {
  // Initialize Serial Communication
  Serial.begin(9600);
  
  // Initialize LCD (16 columns, 2 rows)
  lcd.begin(16, 2);
  
  nameLength = candidateName.length();
  
  // Static display for the second row label if desired, 
  // but we update the whole row in loop to keep it simple.
}

void loop() {
  unsigned long currentMillis = millis();

  // 1. Read Temperature
  // For LM35: 10mV per degree Celsius. 
  // Analog reading (0-1023) * (5.0V / 1024) = Voltage
  // Voltage * 100 = Temp in C
  int rawValue = analogRead(tempPin);
  float voltage = rawValue * (5.0 / 1023.0);
  float temperatureC = voltage * 100.0;

  // 2. Display Candidate Name with Scrolling (First Row)
  if (currentMillis - previousMillis >= scrollInterval) {
    previousMillis = currentMillis;
    
    lcd.setCursor(0, 0);
    // If name is longer than 16 characters, scroll
    if (nameLength > 16) {
      String displayString = "";
      for (int i = 0; i < 16; i++) {
        int charIndex = (scrollPosition + i) % nameLength;
        displayString += candidateName[charIndex];
      }
      lcd.print(displayString);
      scrollPosition = (scrollPosition + 1) % nameLength;
    } else {
      // If it fits, just print it padded with spaces
      lcd.print(candidateName);
      for(int i = nameLength; i < 16; i++) lcd.print(" ");
    }
  }

  // 3. Display Temperature (Second Row)
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(temperatureC);
  lcd.print(" C      "); // Padding spaces to clear leftover characters

  // 4. Send Temperature over Serial
  // Sending only the numeric value for easier parsing on PC side
  // The delay prevents flooding the serial port and gives time for the PC to read
  Serial.println(temperatureC);
  
  delay(100); // Small delay to stabilize readings and serial output
}
