import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.button_driver import RaspberryButton


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
        # Los botones físicos están activos en LOW:
        # HIGH = suelto, LOW = presionado.
        return self.inputs.get(pin, self.HIGH)

    def cleanup(self):
        pass


def create_button():
    fake = FakeGPIO()
    gpio_driver = GPIODriver(fake)

    button = RaspberryButton(
        pin=16,
        gpio_driver=gpio_driver,
    )

    return fake, button


def test_button_configures_pin_as_input():
    fake, button = create_button()

    assert fake.configured[16] == fake.IN


def test_button_starts_released():
    fake, button = create_button()

    assert button.is_pressed is False


def test_button_detects_press():
    fake, button = create_button()

    fake.inputs[16] = fake.LOW

    assert button.is_pressed is True


def test_button_detects_release():
    fake, button = create_button()

    fake.inputs[16] = fake.LOW
    assert button.is_pressed is True

    fake.inputs[16] = fake.HIGH
    assert button.is_pressed is False


def test_read_returns_button_state():
    fake, button = create_button()

    fake.inputs[16] = fake.LOW

    assert button.read() is True