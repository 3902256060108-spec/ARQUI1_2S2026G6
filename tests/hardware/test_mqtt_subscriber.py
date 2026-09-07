import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.mqtt import topics
from src.hardware.mqtt.subscriber import MQTTSubscriber


class FakeClient:
    def __init__(self):
        self.subscriptions = []

    def subscribe(self, topic):
        self.subscriptions.append(topic)


class FakeServo:
    def __init__(self):
        self.open_calls = 0
        self.close_calls = 0

    def open_door(self):
        self.open_calls += 1

    def close_door(self):
        self.close_calls += 1


class FakeLightingController:
    def __init__(self):
        self.states = []

    def set_manual_state(self, turn_on):
        self.states.append(turn_on)


class FakeFan:
    def __init__(self):
        self.on_calls = 0
        self.off_calls = 0

    def turn_on(self):
        self.on_calls += 1

    def turn_off(self):
        self.off_calls += 1


class FakeBuzzerControl:
    def __init__(self):
        self.silence_calls = 0
        self.reset_calls = 0
        self.activate_calls = 0

    def silence(self):
        self.silence_calls += 1

    def reset_silence(self):
        self.reset_calls += 1

    def activate_alarm(self):
        self.activate_calls += 1


def create_subscriber():
    client = FakeClient()
    servo = FakeServo()
    lighting = FakeLightingController()
    fan = FakeFan()
    buzzer = FakeBuzzerControl()

    subscriber = MQTTSubscriber(
        client=client,
        servo=servo,
        lighting_controller=lighting,
        fan=fan,
        buzzer_control=buzzer,
    )

    return (
        subscriber,
        client,
        servo,
        lighting,
        fan,
        buzzer,
    )


def test_subscribes_to_remote_control_topic():
    subscriber, client, _, _, _, _ = (
        create_subscriber()
    )

    subscriber.subscribe()

    assert client.subscriptions == [
        topics.REMOTE_CONTROL_TOPIC
    ]


def test_remote_door_open():
    subscriber, _, servo, _, _, _ = (
        create_subscriber()
    )

    result = subscriber.process_payload(
        '{"dispositivo":"puerta","accion":"ABRIR"}'
    )

    assert servo.open_calls == 1
    assert result == "ABIERTA"


def test_remote_door_close():
    subscriber, _, servo, _, _, _ = (
        create_subscriber()
    )

    result = subscriber.process_payload(
        '{"dispositivo":"puerta","accion":"CERRAR"}'
    )

    assert servo.close_calls == 1
    assert result == "CERRADA"


def test_remote_lights_on():
    subscriber, _, _, lighting, _, _ = (
        create_subscriber()
    )

    result = subscriber.process_payload(
        '{"dispositivo":"luces","accion":"ENCENDER"}'
    )

    assert lighting.states == [True]
    assert result == "ENCENDIDAS"


def test_remote_fan_on():
    subscriber, _, _, _, fan, _ = (
        create_subscriber()
    )

    result = subscriber.process_payload(
        '{"dispositivo":"ventilador","accion":"ENCENDER"}'
    )

    assert fan.on_calls == 1
    assert result == "ENCENDIDO"


def test_remote_alarm_silence():
    subscriber, _, _, _, _, buzzer = (
        create_subscriber()
    )

    result = subscriber.process_payload(
        '{"dispositivo":"alarma","accion":"SILENCIAR"}'
    )

    assert buzzer.silence_calls == 1
    assert result == "INACTIVA"


def test_accepts_bytes_payload():
    subscriber, _, servo, _, _, _ = (
        create_subscriber()
    )

    result = subscriber.process_payload(
        b'{"dispositivo":"puerta","accion":"ABRIR"}'
    )

    assert servo.open_calls == 1
    assert result == "ABIERTA"


def test_invalid_device_raises_error():
    subscriber, _, _, _, _, _ = (
        create_subscriber()
    )

    with pytest.raises(ValueError):
        subscriber.process_payload(
            '{"dispositivo":"cafetera","accion":"ENCENDER"}'
        )


def test_missing_action_raises_error():
    subscriber, _, _, _, _, _ = (
        create_subscriber()
    )

    with pytest.raises(ValueError):
        subscriber.process_payload(
            '{"dispositivo":"puerta"}'
        )