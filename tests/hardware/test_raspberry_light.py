import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.light_driver import RaspberryLightSensor


class FakeGPIO:
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0

    def __init__(self):
        self.configured = {}
        self.inputs = {}

    def setup(self, pin, mode):
        self.configured[pin] = mode

    def output(self, pin, value):
        pass

    def input(self, pin):
        return self.inputs.get(pin, self.HIGH)

    def cleanup(self):
        pass


def create_sensor(active_low=True):
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    sensor = RaspberryLightSensor(
        pin=27,
        gpio_driver=driver,
        active_low=active_low,
    )

    return fake, sensor


def test_light_sensor_configures_input():
    fake, sensor = create_sensor()

    assert fake.configured[27] == fake.IN


def test_active_low_detects_darkness_when_low():
    fake, sensor = create_sensor(active_low=True)

    fake.inputs[27] = fake.LOW

    assert sensor.is_dark() is True


def test_active_low_detects_light_when_high():
    fake, sensor = create_sensor(active_low=True)

    fake.inputs[27] = fake.HIGH

    assert sensor.is_dark() is False


def test_active_high_detects_darkness_when_high():
    fake, sensor = create_sensor(active_low=False)

    fake.inputs[27] = fake.HIGH

    assert sensor.is_dark() is True


def test_read_returns_boolean():
    fake, sensor = create_sensor()

    result = sensor.read()

    assert isinstance(result, bool)