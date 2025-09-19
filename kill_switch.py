"""MQTT-based kill switch listener."""

import time

try:
    import paho.mqtt.client as mqtt
except ImportError:  # pragma: no cover - optional dependency
    mqtt = None

# Constants
MQTT_BROKER = "your_mqtt_broker_address"  # <-- IMPORTANT: CONFIGURE THIS
MQTT_PORT = 1883
KILL_SWITCH_TOPIC = "ra7/commands/AGI_HALT"  # As per spec
GPIO_PIN = 21  # Hardware kill-switch pin on Raspberry Pi


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    # QoS 2 for "exactly once" delivery.
    client.subscribe(KILL_SWITCH_TOPIC, qos=2)


def on_message(client, userdata, msg):
    if msg.topic == KILL_SWITCH_TOPIC:
        print("!!! KILL SWITCH COMMAND RECEIVED !!!")
        print("!!! System halt initiated. Latency target: <1s. !!!")
        # On a real node:
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(GPIO_PIN, GPIO.OUT)
        # GPIO.output(GPIO_PIN, GPIO.LOW)  # Trigger pull-down resistor
        print("Simulating GPIO-21 pull-down. System terminating.")
        exit()


def mock_listener():
    """Mock loop for environments without MQTT."""
    print("Kill Switch Listener Initialized.")
    print(f"Subscribed to topic: {KILL_SWITCH_TOPIC}")
    print("Waiting for AGI HALT command...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nListener stopped.")


def live_listener():
    """Start the MQTT listener or fall back to the mock."""
    if mqtt is None:
        print("paho-mqtt not installed; running mock listener.")
        mock_listener()
        return

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to MQTT broker at {MQTT_BROKER}...")
    # client.connect(MQTT_BROKER, MQTT_PORT, 60)
    # client.loop_forever()
    print("MQTT client is commented out. Running mock listener instead.")
    mock_listener()


if __name__ == "__main__":
    live_listener()
