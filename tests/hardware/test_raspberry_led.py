import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.led_driver import RaspberryLED


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
        return 0

    def cleanup(self):
        pass


def create_led():
    fake = FakeGPIO()
    gpio_driver = GPIODriver(fake)
    led = RaspberryLED(
        pin=5,
        gpio_driver=gpio_driver,
    )
    return fake, led


def test_led_configures_pin_as_output():
    fake, led = create_led()

    assert fake.configured[5] == fake.OUT


def test_led_starts_off():
    fake, led = create_led()

    assert led.is_on is False
    assert fake.outputs[5] == fake.LOW


def test_led_turns_on():
    fake, led = create_led()

    led.turn_on()

    assert led.is_on is True
    assert fake.outputs[5] == fake.HIGH


def test_led_turns_off():
    fake, led = create_led()

    led.turn_on()
    led.turn_off()

    assert led.is_on is False
    assert fake.outputs[5] == fake.LOW


def test_led_toggle():
    fake, led = create_led()

    led.toggle()

    assert led.is_on is True
    assert fake.outputs[5] == fake.HIGH

    led.toggle()

    assert led.is_on is False
    assert fake.outputs[5] == fake.LOW