import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.dht_driver import RaspberryDHT


class FakeDHTDevice:
    def __init__(self, temperature=25.0, humidity=50.0):
        self.temperature = temperature
        self.humidity = humidity


def test_dht_stores_pin():
    device = FakeDHTDevice()

    sensor = RaspberryDHT(
        pin=4,
        dht_device=device,
    )

    assert sensor.pin == 4


def test_dht_reads_temperature():
    device = FakeDHTDevice(
        temperature=26.5,
        humidity=55.0,
    )

    sensor = RaspberryDHT(
        pin=4,
        dht_device=device,
    )

    reading = sensor.read()

    assert reading["temperature"] == 26.5


def test_dht_reads_humidity():
    device = FakeDHTDevice(
        temperature=26.5,
        humidity=63.2,
    )

    sensor = RaspberryDHT(
        pin=4,
        dht_device=device,
    )

    reading = sensor.read()

    assert reading["humidity"] == 63.2


def test_dht_returns_floats():
    device = FakeDHTDevice(
        temperature=25,
        humidity=50,
    )

    sensor = RaspberryDHT(
        pin=4,
        dht_device=device,
    )

    reading = sensor.read()

    assert isinstance(reading["temperature"], float)
    assert isinstance(reading["humidity"], float)


def test_dht_rejects_missing_temperature():
    device = FakeDHTDevice(
        temperature=None,
        humidity=50.0,
    )

    sensor = RaspberryDHT(
        pin=4,
        dht_device=device,
    )

    with pytest.raises(RuntimeError):
        sensor.read()


def test_dht_rejects_missing_humidity():
    device = FakeDHTDevice(
        temperature=25.0,
        humidity=None,
    )

    sensor = RaspberryDHT(
        pin=4,
        dht_device=device,
    )

    with pytest.raises(RuntimeError):
        sensor.read()