import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.mqtt.remote_control import (
    RemoteControlHandler,
)


class FakeSubscriber:
    def __init__(self, result):
        self.result = result
        self.payload = None

    def process_payload(self, payload):
        self.payload = payload
        return self.result


class FakePublisher:
    def __init__(self):
        self.door = None
        self.lights = None
        self.fan = None
        self.alarm = None

    def publish_door_state(self, state):
        self.door = state

    def publish_lights_state(self, state):
        self.lights = state

    def publish_fan_state(self, state):
        self.fan = state

    def publish_alarm_state(self, state):
        self.alarm = state


def create_handler(result):
    subscriber = FakeSubscriber(result)
    publisher = FakePublisher()

    handler = RemoteControlHandler(
        subscriber=subscriber,
        publisher=publisher,
    )

    return handler, subscriber, publisher


def test_door_command_publishes_confirmation():
    handler, _, publisher = create_handler(
        "ABIERTA"
    )

    result = handler.process(
        '{"dispositivo":"puerta","accion":"ABRIR"}'
    )

    assert result == "ABIERTA"
    assert publisher.door == "ABIERTA"


def test_lights_command_publishes_confirmation():
    handler, _, publisher = create_handler(
        "ENCENDIDAS"
    )

    handler.process(
        '{"dispositivo":"luces","accion":"ENCENDER"}'
    )

    assert publisher.lights == "ENCENDIDAS"


def test_fan_command_publishes_confirmation():
    handler, _, publisher = create_handler(
        "ENCENDIDO"
    )

    handler.process(
        '{"dispositivo":"ventilador","accion":"ENCENDER"}'
    )

    assert publisher.fan == "ENCENDIDO"


def test_alarm_command_publishes_confirmation():
    handler, _, publisher = create_handler(
        "INACTIVA"
    )

    handler.process(
        '{"dispositivo":"alarma","accion":"SILENCIAR"}'
    )

    assert publisher.alarm == "INACTIVA"


def test_bytes_payload_is_supported():
    handler, _, publisher = create_handler(
        "CERRADA"
    )

    result = handler.process(
        b'{"dispositivo":"puerta","accion":"CERRAR"}'
    )

    assert result == "CERRADA"
    assert publisher.door == "CERRADA"