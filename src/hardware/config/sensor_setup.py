from src.hardware.config import pins

from src.hardware.sensors.dht_sensor import DHTSensor
from src.hardware.sensors.gas_sensor import GasSensor
from src.hardware.sensors.light_sensor import LightSensor
from src.hardware.sensors.ultrasonic_sensor import UltrasonicSensor


def create_sensors():
    """
    Crea los sensores usando el mapa GPIO
    centralizado de pins.py.
    """

    sensors = {
        "dht": DHTSensor(
            pin=pins.DHT_PIN,
            sensor_type="DHT11",
        ),

        "gas": GasSensor(
            pin=pins.GAS_PIN,
            sensor_type="MQ-2",
        ),

        "light": LightSensor(
            pin=pins.LIGHT_SENSOR_PIN,
        ),

        "ultrasonic": UltrasonicSensor(
            trigger_pin=pins.ULTRASONIC_TRIGGER_PIN,
            echo_pin=pins.ULTRASONIC_ECHO_PIN,
        ),
    }

    return sensors