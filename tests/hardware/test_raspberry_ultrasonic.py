import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.ultrasonic_driver import (
    RaspberryUltrasonic,
)


class FakeGPIO:
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0

    def __init__(self):
        self.configured = {}
        self.outputs = {}

    def setup(self, pin, mode):
        self.configured[pin] = mode

    def output(self, pin, value):
        self.outputs[pin] = value

    def input(self, pin):
        return self.LOW

    def cleanup(self):
        pass


def create_sensor():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    sensor = RaspberryUltrasonic(
        trigger_pin=23,
        echo_pin=24,
        gpio_driver=driver,
    )

    return fake, sensor


def test_ultrasonic_configures_trigger_as_output():
    fake, sensor = create_sensor()

    assert fake.configured[23] == fake.OUT


def test_ultrasonic_configures_echo_as_input():
    fake, sensor = create_sensor()

    assert fake.configured[24] == fake.IN


def test_trigger_starts_low():
    fake, sensor = create_sensor()

    assert fake.outputs[23] == fake.LOW


def test_calculates_distance():
    fake, sensor = create_sensor()

    # Aproximadamente 1 ms de viaje total.
    distance = sensor.calculate_distance(0.001)

    assert distance == pytest.approx(17.15)


def test_calculates_zero_distance():
    fake, sensor = create_sensor()

    assert sensor.calculate_distance(0) == 0


def test_rejects_negative_echo_time():
    fake, sensor = create_sensor()

    with pytest.raises(ValueError):
        sensor.calculate_distance(-0.001)


def test_detects_near_object():
    fake, sensor = create_sensor()

    assert sensor.object_detected(
        distance_cm=20,
        threshold_cm=30,
    ) is True


def test_does_not_detect_far_object():
    fake, sensor = create_sensor()

    assert sensor.object_detected(
        distance_cm=50,
        threshold_cm=30,
    ) is False


def test_threshold_boundary_counts_as_detected():
    fake, sensor = create_sensor()

    assert sensor.object_detected(
        distance_cm=30,
        threshold_cm=30,
    ) is True


def test_rejects_negative_distance():
    fake, sensor = create_sensor()

    with pytest.raises(ValueError):
        sensor.object_detected(
            distance_cm=-1,
            threshold_cm=30,
        )

class FakeSequenceGPIO:
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0

    def __init__(self, echo_values):
        self.configured = {}
        self.outputs = {}
        self.echo_values = list(echo_values)

    def setup(self, pin, mode):
        self.configured[pin] = mode

    def output(self, pin, value):
        self.outputs[pin] = value

    def input(self, pin):
        if self.echo_values:
            return self.echo_values.pop(0)

        return self.LOW

    def cleanup(self):
        pass


class FakeClock:
    def __init__(self, values):
        self.values = list(values)

    def time(self):
        if self.values:
            return self.values.pop(0)

        return 0.0

    def sleep(self, seconds):
        pass


def test_read_distance_generates_measurement():
    fake_gpio = FakeSequenceGPIO(
        [
            FakeSequenceGPIO.LOW,
            FakeSequenceGPIO.HIGH,
            FakeSequenceGPIO.HIGH,
            FakeSequenceGPIO.LOW,
        ]
    )

    driver = GPIODriver(fake_gpio)

    clock = FakeClock(
        [
            0.0000,
            0.0001,
            0.0010,
            0.0020,
            0.0030,
        ]
    )

    sensor = RaspberryUltrasonic(
        trigger_pin=23,
        echo_pin=24,
        gpio_driver=driver,
        time_provider=clock.time,
        sleep_provider=clock.sleep,
    )

    distance = sensor.read_distance()

    assert distance == pytest.approx(34.3)


def test_read_distance_rejects_invalid_timeout():
    fake, sensor = create_sensor()

    with pytest.raises(ValueError):
        sensor.read_distance(timeout=0)


def test_trigger_finishes_low():
    fake_gpio = FakeSequenceGPIO(
        [
            FakeSequenceGPIO.HIGH,
            FakeSequenceGPIO.LOW,
        ]
    )

    driver = GPIODriver(fake_gpio)

    clock = FakeClock(
        [
            0.0,
            0.001,
            0.002,
        ]
    )

    sensor = RaspberryUltrasonic(
        trigger_pin=23,
        echo_pin=24,
        gpio_driver=driver,
        time_provider=clock.time,
        sleep_provider=clock.sleep,
    )

    sensor.read_distance()

    assert fake_gpio.outputs[23] == fake_gpio.LOW