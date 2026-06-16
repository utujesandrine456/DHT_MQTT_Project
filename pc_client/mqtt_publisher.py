import json
import time
from datetime import datetime, timezone

import serial
import paho.mqtt.client as mqtt

SERIAL_PORT = "COM9"       

BAUD_RATE = 9600                 

MQTT_BROKER_HOST = "broker.benax.rw" 
MQTT_BROKER_PORT = 1883         
MQTT_USERNAME = None            
MQTT_PASSWORD = None
MQTT_USE_TLS = False
MQTT_TOPIC_PREFIX = "exam/uwase_utuje_sandrine"   
MQTT_CLIENT_ID = "arduino-temp-bridge"


def sanitize_topic_part(text: str) -> str:
    """MQTT topics shouldn't contain spaces or '/'; turn the name into a safe slug."""
    return text.strip().replace(" ", "_").replace("/", "_")


def connect_serial() -> serial.Serial:
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
            print(f"[Serial] Connected to {SERIAL_PORT} @ {BAUD_RATE} baud")
            return ser
        except serial.SerialException as e:
            print(f"[Serial] Could not open {SERIAL_PORT}: {e}. Retrying in 3s...")
            time.sleep(3)


def build_mqtt_client() -> mqtt.Client:
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    if MQTT_USERNAME:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    if MQTT_USE_TLS:
        client.tls_set()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[MQTT] Connected to {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
        else:
            print(f"[MQTT] Connection failed with result code {rc}")

    def on_disconnect(client, userdata, rc):
        print(f"[MQTT] Disconnected (rc={rc}). Will retry on next loop.")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=30)
    client.loop_start()   # background thread handles the network loop + auto-reconnect
    return client


def main():
    ser = connect_serial()
    mqtt_client = build_mqtt_client()

    print("Listening for temperature readings (Ctrl+C to stop)...\n")
    try:
        while True:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                continue

            parts = raw.split(",")
            if len(parts) == 2:
                candidate_name, temp_str = parts
            elif len(parts) == 1:
                candidate_name = "UWASE UTUJE Sandrine"
                temp_str = parts[0]
            else:
                print(f"[WARN] Unexpected line, skipping: {raw!r}")
                continue
            try:
                temperature = float(temp_str)
            except ValueError:
                print(f"[WARN] Could not parse temperature, skipping: {raw!r}")
                continue

            timestamp = datetime.now(timezone.utc).isoformat()
            payload = json.dumps({
                "candidate": candidate_name,
                "temperature": temperature,
                "timestamp": timestamp,
            })
            topic = f"{MQTT_TOPIC_PREFIX}/{sanitize_topic_part(candidate_name)}"

            mqtt_client.publish(topic, payload, qos=0, retain=False)

            print(f"[{timestamp}] {candidate_name}: {temperature:.2f} C  -> published to '{topic}'")

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        ser.close()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Closed serial port and MQTT connection.")


if __name__ == "__main__":
    main()