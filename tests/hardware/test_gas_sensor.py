import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.sensors.gas_sensor import GasSensor


def test_gas_sensor_configuration():
    sensor = GasSensor(
        pin=17,
        sensor_type="MQ-2"
    )

    assert sensor.pin == 17
    assert sensor.sensor_type == "MQ-2"


def test_gas_alert():
    sensor = GasSensor()

    assert sensor.is_alert(
        value=700,
        threshold=500
    ) is True


def test_gas_no_alert():
    sensor = GasSensor()

    assert sensor.is_alert(
        value=300,
        threshold=500
    ) is False


def test_gas_threshold_not_configured():
    sensor = GasSensor()

    try:
        sensor.is_alert(
            value=300,
            threshold=None
        )
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True


def test_negative_gas_value():
    sensor = GasSensor()

    try:
        sensor.is_alert(
            value=-1,
            threshold=500
        )
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True


def test_gas_read_requires_raspberry():
    sensor = GasSensor()

    try:
        sensor.read()
        assert False, "Se esperaba NotImplementedError"
    except NotImplementedError:
        assert True