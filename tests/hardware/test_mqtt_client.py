import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.mqtt.mqtt_client import (
    RaspberryMQTTClient,
)


class FakePahoClient:
    def __init__(self):
        self.on_connect = None
        self.on_message = None

        self.connected = None
        self.started = False
        self.stopped = False
        self.disconnected = False

        self.published = []
        self.subscribed = []

    def connect(self, host, port, keepalive):
        self.connected = (
            host,
            port,
            keepalive,
        )

    def loop_start(self):
        self.started = True

    def loop_stop(self):
        self.stopped = True

    def disconnect(self):
        self.disconnected = True

    def publish(self, topic, payload):
        self.published.append(
            (topic, payload)
        )

    def subscribe(self, topic):
        self.subscribed.append(topic)


class FakeMQTTModule:
    def __init__(self):
        self.instance = None

    def Client(self):
        self.instance = FakePahoClient()
        return self.instance


class FakeMessage:
    def __init__(self, payload):
        self.payload = payload


def create_client():
    module = FakeMQTTModule()

    client = RaspberryMQTTClient(
        mqtt_module=module,
        host="localhost",
    )

    return client, module.instance


def test_connect():
    client, fake = create_client()

    client.connect()

    assert fake.connected == (
        "localhost",
        1883,
        60,
    )


def test_start_and_stop():
    client, fake = create_client()

    client.start()
    client.stop()

    assert fake.started is True
    assert fake.stopped is True


def test_disconnect():
    client, fake = create_client()

    client.disconnect()

    assert fake.disconnected is True


def test_publish():
    client, fake = create_client()

    client.publish(
        "test/topic",
        '{"valor":25}',
    )

    assert fake.published == [
        (
            "test/topic",
            '{"valor":25}',
        )
    ]


def test_subscribe():
    client, fake = create_client()

    client.subscribe(
        "test/control"
    )

    assert fake.subscribed == [
        "test/control"
    ]


def test_received_message_calls_handler():
    client, fake = create_client()

    received = []

    client.set_message_handler(
        received.append
    )

    fake.on_message(
        fake,
        None,
        FakeMessage(
            b'{"dispositivo":"puerta"}'
        ),
    )

    assert received == [
        b'{"dispositivo":"puerta"}'
    ]