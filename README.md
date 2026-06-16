# Temperature Display and MQTT Monitoring

This project is a simple embedded system that reads temperature data from a sensor via an Arduino Uno, displays it locally on an LCD, and sends it to a PC which then publishes the data to an MQTT broker.

## System Architecture

```mermaid
graph LR
    A[Temperature Sensor (LM35)] -->|Analog Voltage| B(Arduino Uno)
    B -->|I2C / Parallel| C[16x2 LCD Display]
    B -->|USB Serial| D[PC Program Python]
    D -->|MQTT Publish| E[(MQTT Broker VPS)]
```

## Communication Details

*   **Serial Communication (Arduino <-> PC):**
    *   Baud Rate: `9600`
    *   Data Format: ASCII text representing the temperature float value followed by a newline (e.g., `25.50\r\n`).
*   **MQTT Topic:**
    *   `candidate/sensor/temperature`

## Project Structure

*   `arduino/temperature_display/temperature_display.ino`: The Arduino code to read the sensor, scroll the candidate name on the LCD, and print the temperature to Serial.
*   `pc_client/mqtt_publisher.py`: The Python script to read from the PC's serial port and publish to the MQTT broker.
*   `pc_client/requirements.txt`: Python dependencies (`pyserial`, `paho-mqtt`).

## Hardware Setup

1.  **Arduino Uno**
2.  **LM35 Temperature Sensor**
    *   VCC to 5V
    *   GND to GND
    *   OUT to Analog Pin A0
3.  **16x2 LCD Display**
    *   RS to Pin 12
    *   EN to Pin 11
    *   D4 to Pin 5
    *   D5 to Pin 4
    *   D6 to Pin 3
    *   D7 to Pin 2

## Software Setup & Execution

### 1. Arduino
1.  Open `arduino/temperature_display/temperature_display.ino` in the Arduino IDE.
2.  Select your Arduino Uno board and COM port.
3.  Compile and upload the code.
4.  Verify the LCD displays the scrolling name and temperature.

### 2. PC Client
1.  Ensure you have Python 3 installed.
2.  Open a terminal in the `pc_client` directory.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Edit `mqtt_publisher.py`:
    *   Change `SERIAL_PORT` to match your Arduino's COM port (e.g., `'COM3'`, `'COM4'`, etc.).
    *   If you have a custom VPS MQTT broker, update the `MQTT_BROKER` variable. It defaults to a public test broker `test.mosquitto.org` for demonstration.
5.  Run the script:
    ```bash
    python mqtt_publisher.py
    ```

## Screenshots of Successful Execution

*(Please replace these placeholders with actual screenshots before submitting)*

1.  **LCD Display:** Showing the scrolling name and temperature.
    *(Add image here)*

2.  **PC Terminal:** Showing the script running, reading serial data, and publishing.
    *(Add image here)*

3.  **MQTT Dashboard:** Showing the incoming data on the broker (using a tool like MQTT Explorer).
    *(Add image here)*
"# DHT_MQTT_Project" 
