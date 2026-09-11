import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.config import pins
from src.hardware.drivers.raspberry_pi.dht_factory import (
    create_dht_sensor,
)


class FakeBoard:
    D4 = "GPIO4"


class FakeDHTDevice:
    def __init__(self, pin, use_pulseio=True):
        self.pin = pin
        self.use_pulseio = use_pulseio
        self.temperature = 25.0
        self.humidity = 50.0


class FakeDHTModule:
    DHT11 = FakeDHTDevice


def test_dht_factory_uses_configured_pin():
    sensor = create_dht_sensor(
        FakeDHTModule,
        FakeBoard,
    )

    assert sensor.pin == pins.DHT_PIN
    assert sensor.device.pin == "GPIO4"


def test_dht_factory_disables_pulseio():
    sensor = create_dht_sensor(
        FakeDHTModule,
        FakeBoard,
    )

    assert sensor.device.use_pulseio is False


def test_created_dht_can_read():
    sensor = create_dht_sensor(
        FakeDHTModule,
        FakeBoard,
    )

    reading = sensor.read()

    assert reading["temperature"] == 25.0
    assert reading["humidity"] == 50.0