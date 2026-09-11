import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.lcd_driver import RaspberryLCD


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


def create_lcd():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    lcd = RaspberryLCD(
        rs_pin=7,
        enable_pin=8,
        d4_pin=9,
        d5_pin=10,
        d6_pin=11,
        d7_pin=14,
        gpio_driver=driver,
    )

    return fake, lcd


def test_lcd_configures_all_pins_as_output():
    fake, lcd = create_lcd()

    for pin in [7, 8, 9, 10, 11, 14]:
        assert fake.configured[pin] == fake.OUT


def test_lcd_pins_start_low():
    fake, lcd = create_lcd()

    for pin in [7, 8, 9, 10, 11, 14]:
        assert fake.outputs[pin] == fake.LOW


def test_lcd_starts_empty():
    fake, lcd = create_lcd()

    assert lcd.line1 == ""
    assert lcd.line2 == ""


def test_lcd_can_show_text():
    fake, lcd = create_lcd()

    lcd.show(
        "Hola Raspberry",
        "Sistema NORMAL",
    )

    assert lcd.line1 == "Hola Raspberry"
    assert lcd.line2 == "Sistema NORMAL"


def test_lcd_limits_text_to_16_characters():
    fake, lcd = create_lcd()

    lcd.show(
        "12345678901234567890",
        "abcdefghijklmnopqrst",
    )

    assert lcd.line1 == "1234567890123456"
    assert lcd.line2 == "abcdefghijklmnop"


def test_lcd_can_clear():
    fake, lcd = create_lcd()

    lcd.show("Temperatura", "25 C")
    lcd.clear()

    assert lcd.line1 == ""
    assert lcd.line2 == ""

def test_lcd_initialize_sends_commands():
    fake, lcd = create_lcd()

    lcd.initialize()

    # Después de inicializar, el pin RS debe terminar
    # en modo comando (LOW) al enviar el último comando.
    assert fake.outputs[lcd.rs_pin] == fake.LOW


def test_lcd_show_updates_internal_lines():
    fake, lcd = create_lcd()

    lcd.show(
        "Temp 25C",
        "Estado NORMAL",
    )

    assert lcd.line1 == "Temp 25C"
    assert lcd.line2 == "Estado NORMAL"


def test_lcd_clear_resets_internal_lines():
    fake, lcd = create_lcd()

    lcd.show(
        "Gas detectado",
        "EMERGENCIA",
    )

    lcd.clear()

    assert lcd.line1 == ""
    assert lcd.line2 == ""