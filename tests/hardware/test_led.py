import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.led import LED


def test_led_configuration():
    led = LED(pin=17, name="Rojo")

    assert led.pin == 17
    assert led.name == "Rojo"
    assert led.is_on is False


def test_turn_on():
    led = LED(pin=17)

    led.turn_on()

    assert led.is_on is True


def test_turn_off():
    led = LED(pin=17)

    led.turn_on()
    led.turn_off()

    assert led.is_on is False


def test_toggle():
    led = LED(pin=17)

    led.toggle()
    assert led.is_on is True

    led.toggle()
    assert led.is_on is False