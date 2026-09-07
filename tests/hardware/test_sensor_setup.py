import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.config import pins
from src.hardware.config.sensor_setup import create_sensors


def test_sensors_use_configured_gpio():
    sensors = create_sensors()

    assert sensors["dht"].pin == pins.DHT_PIN
    assert sensors["dht"].sensor_type == "DHT11"

    assert sensors["gas"].pin == pins.GAS_PIN
    assert sensors["gas"].sensor_type == "MQ-2"

    assert sensors["light"].pin == pins.LIGHT_SENSOR_PIN

    assert (
        sensors["ultrasonic"].trigger_pin
        == pins.ULTRASONIC_TRIGGER_PIN
    )

    assert (
        sensors["ultrasonic"].echo_pin
        == pins.ULTRASONIC_ECHO_PIN
    )