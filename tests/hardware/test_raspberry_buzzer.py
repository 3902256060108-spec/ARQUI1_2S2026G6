import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.buzzer_driver import RaspberryBuzzer


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


def create_buzzer():
    fake = FakeGPIO()
    gpio_driver = GPIODriver(fake)

    buzzer = RaspberryBuzzer(
        pin=22,
        gpio_driver=gpio_driver,
    )

    return fake, buzzer


def test_buzzer_configures_pin_as_output():
    fake, buzzer = create_buzzer()

    assert fake.configured[22] == fake.OUT


def test_buzzer_starts_off():
    fake, buzzer = create_buzzer()

    assert buzzer.is_on is False
    assert fake.outputs[22] == fake.LOW


def test_buzzer_turns_on():
    fake, buzzer = create_buzzer()

    buzzer.turn_on()

    assert buzzer.is_on is True
    assert fake.outputs[22] == fake.HIGH


def test_buzzer_turns_off():
    fake, buzzer = create_buzzer()

    buzzer.turn_on()
    buzzer.turn_off()

    assert buzzer.is_on is False
    assert fake.outputs[22] == fake.LOW


def test_buzzer_toggle():
    fake, buzzer = create_buzzer()

    buzzer.toggle()

    assert buzzer.is_on is True
    assert fake.outputs[22] == fake.HIGH

    buzzer.toggle()

    assert buzzer.is_on is False
    assert fake.outputs[22] == fake.LOW