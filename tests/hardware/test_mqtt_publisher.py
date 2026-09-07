import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.mqtt import topics
from src.hardware.mqtt.publisher import MQTTPublisher
from src.hardware.core.system_state import SystemState


class FakeMQTTClient:
    def __init__(self):
        self.messages = []

    def publish(self, topic, payload):
        self.messages.append(
            {
                "topic": topic,
                "payload": payload,
            }
        )


def create_publisher():
    client = FakeMQTTClient()
    publisher = MQTTPublisher(client)
    return publisher, client


def test_publish_temperature():
    publisher, client = create_publisher()

    publisher.publish_sensor_value(
        topics.TEMPERATURE_TOPIC,
        25,
    )

    assert len(client.messages) == 1
    assert client.messages[0]["topic"] == topics.TEMPERATURE_TOPIC

    payload = json.loads(
        client.messages[0]["payload"]
    )

    assert payload == {
        "valor": 25,
    }


def test_publish_snapshot():
    publisher, client = create_publisher()

    snapshot = {
        "temperature": 25.0,
        "humidity": 60.0,
        "gas_alert": False,
        "distance_cm": 40.0,
        "is_dark": True,
        "state": SystemState.NORMAL,
    }

    publisher.publish_snapshot(snapshot)

    assert len(client.messages) == 6


def test_publish_global_state():
    publisher, client = create_publisher()

    snapshot = {
        "temperature": 25.0,
        "humidity": 60.0,
        "gas_alert": False,
        "distance_cm": 40.0,
        "is_dark": False,
        "state": SystemState.WARNING,
    }

    publisher.publish_snapshot(snapshot)

    state_message = client.messages[-1]

    assert (
        state_message["topic"]
        == topics.GLOBAL_STATE_TOPIC
    )

    payload = json.loads(
        state_message["payload"]
    )

    assert payload == {
        "estado": "ADVERTENCIA",
    }


def test_publish_door_state():
    publisher, client = create_publisher()

    publisher.publish_door_state(
        "ABIERTA"
    )

    payload = json.loads(
        client.messages[0]["payload"]
    )

    assert payload == {
        "estado": "ABIERTA",
    }


def test_publish_arm64_results():
    publisher, client = create_publisher()

    results = {
        "max": 30,
        "min": 20,
        "avg": 25,
        "count": 20,
    }

    publisher.publish_arm64_results(
        results
    )

    assert (
        client.messages[0]["topic"]
        == topics.ARM64_RESULTS_TOPIC
    )

    payload = json.loads(
        client.messages[0]["payload"]
    )

    assert payload == results