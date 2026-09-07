import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.sensors.dht_sensor import DHTSensor


def test_dht_configuration():
    sensor = DHTSensor(pin=4, sensor_type="DHT11")

    assert sensor.pin == 4
    assert sensor.sensor_type == "DHT11"


def test_dht_read_requires_raspberry():
    sensor = DHTSensor(pin=4)

    try:
        sensor.read()
        assert False, "Se esperaba NotImplementedError"
    except NotImplementedError:
        assert True