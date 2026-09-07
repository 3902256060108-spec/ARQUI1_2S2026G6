import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.sensors.light_sensor import LightSensor


def test_light_sensor_configuration():
    sensor = LightSensor(pin=27)

    assert sensor.pin == 27


def test_dark_condition():
    sensor = LightSensor()

    assert sensor.is_dark(
        value=200,
        threshold=500
    ) is True


def test_light_condition():
    sensor = LightSensor()

    assert sensor.is_dark(
        value=700,
        threshold=500
    ) is False


def test_light_threshold_not_configured():
    sensor = LightSensor()

    try:
        sensor.is_dark(
            value=300,
            threshold=None
        )
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True


def test_negative_light_value():
    sensor = LightSensor()

    try:
        sensor.is_dark(
            value=-1,
            threshold=500
        )
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True


def test_light_read_requires_raspberry():
    sensor = LightSensor()

    try:
        sensor.read()
        assert False, "Se esperaba NotImplementedError"
    except NotImplementedError:
        assert True