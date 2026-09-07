import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver


class FakeGPIO:
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0

    def __init__(self):
        self.configured = {}
        self.outputs = {}
        self.inputs = {}
        self.cleaned = False

    def setup(self, pin, mode):
        self.configured[pin] = mode

    def output(self, pin, value):
        self.outputs[pin] = value

    def input(self, pin):
        return self.inputs.get(pin, 0)

    def cleanup(self):
        self.cleaned = True


def test_setup_output():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    driver.setup_output(5)

    assert fake.configured[5] == fake.OUT


def test_setup_input():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    driver.setup_input(16)

    assert fake.configured[16] == fake.IN


def test_write_high():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    driver.write_high(5)

    assert fake.outputs[5] == fake.HIGH


def test_write_low():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    driver.write_low(5)

    assert fake.outputs[5] == fake.LOW


def test_read_input():
    fake = FakeGPIO()
    fake.inputs[16] = 1

    driver = GPIODriver(fake)

    assert driver.read(16) == 1


def test_cleanup():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    driver.cleanup()

    assert fake.cleaned is True