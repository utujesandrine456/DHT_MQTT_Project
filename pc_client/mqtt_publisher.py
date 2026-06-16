import serial
import time
import paho.mqtt.client as mqtt

# --- Configuration ---
# Serial Port Configuration
# Change 'COM3' to the port your Arduino is connected to (e.g., '/dev/ttyUSB0' on Linux)
SERIAL_PORT = 'COM3' 
BAUD_RATE = 9600

# MQTT Broker Configuration
# We are using a public test broker. For your VPS, change this to your VPS IP/domain.
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "candidate/sensor/temperature"

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker: {MQTT_BROKER}")
    else:
        print(f"Failed to connect to MQTT Broker, return code: {rc}")

def on_publish(client, userdata, mid):
    # This callback is fired when a message is successfully published
    pass

# --- Setup ---
# Setup MQTT Client
client = mqtt.Client("PC_Temperature_Publisher")
client.on_connect = on_connect
client.on_publish = on_publish

print(f"Connecting to MQTT Broker {MQTT_BROKER}...")
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    # Start the background thread for MQTT network traffic
    client.loop_start() 
except Exception as e:
    print(f"Error connecting to MQTT Broker: {e}")
    exit(1)

# Setup Serial Connection
print(f"Connecting to Serial Port {SERIAL_PORT}...")
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Wait for connection to establish
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error connecting to Serial Port: {e}")
    print("Please check if the Arduino is connected and the COM port is correct.")
    client.loop_stop()
    exit(1)

# --- Main Loop ---
print("-" * 30)
print(f"Listening for data on {SERIAL_PORT} and publishing to {MQTT_TOPIC}...")
print("Press Ctrl+C to stop.")
print("-" * 30)

try:
    while True:
        if ser.in_waiting > 0:
            # Read line from serial and decode
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                try:
                    # Attempt to parse as float to ensure it's a valid temperature reading
                    temperature = float(line)
                    print(f"Received Temperature: {temperature} °C")
                    
                    # Publish to MQTT
                    result = client.publish(MQTT_TOPIC, str(temperature))
                    status = result[0]
                    if status == 0:
                        print(f"  -> Successfully published to {MQTT_TOPIC}")
                    else:
                        print(f"  -> Failed to publish to {MQTT_TOPIC}")
                        
                except ValueError:
                    # If it's not a float, it might be an initialization message or noise
                    print(f"Received non-numeric data: {line}")
                    
        time.sleep(0.1) # Small delay to prevent high CPU usage

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
    client.loop_stop()
    client.disconnect()
    print("Connections closed.")
