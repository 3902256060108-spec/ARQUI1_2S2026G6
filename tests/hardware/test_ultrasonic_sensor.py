import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.sensors.ultrasonic_sensor import UltrasonicSensor


def test_ultrasonic_configuration():
    sensor = UltrasonicSensor(
        trigger_pin=23,
        echo_pin=24
    )

    assert sensor.trigger_pin == 23
    assert sensor.echo_pin == 24


def test_object_detected():
    sensor = UltrasonicSensor(23, 24)

    assert sensor.object_detected(
        distance_cm=15,
        threshold_cm=30
    ) is True


def test_object_not_detected():
    sensor = UltrasonicSensor(23, 24)

    assert sensor.object_detected(
        distance_cm=50,
        threshold_cm=30
    ) is False


def test_negative_distance():
    sensor = UltrasonicSensor(23, 24)

    try:
        sensor.object_detected(
            distance_cm=-5,
            threshold_cm=30
        )
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True


def test_ultrasonic_read_requires_raspberry():
    sensor = UltrasonicSensor(23, 24)

    try:
        sensor.read_distance()
        assert False, "Se esperaba NotImplementedError"
    except NotImplementedError:
        assert True