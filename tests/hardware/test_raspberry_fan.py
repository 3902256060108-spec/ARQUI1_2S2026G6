import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.fan_driver import RaspberryFan


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


def create_fan():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    fan = RaspberryFan(
        pin=25,
        gpio_driver=driver,
    )

    return fake, fan


def test_fan_configures_pin_as_output():
    fake, fan = create_fan()

    assert fake.configured[25] == fake.OUT


def test_fan_starts_off():
    fake, fan = create_fan()

    assert fan.is_on is False
    assert fake.outputs[25] == fake.LOW


def test_fan_turns_on():
    fake, fan = create_fan()

    fan.turn_on()

    assert fan.is_on is True
    assert fake.outputs[25] == fake.HIGH


def test_fan_turns_off():
    fake, fan = create_fan()

    fan.turn_on()
    fan.turn_off()

    assert fan.is_on is False
    assert fake.outputs[25] == fake.LOW


def test_fan_toggle():
    fake, fan = create_fan()

    fan.toggle()

    assert fan.is_on is True
    assert fake.outputs[25] == fake.HIGH

    fan.toggle()

    assert fan.is_on is False
    assert fake.outputs[25] == fake.LOW