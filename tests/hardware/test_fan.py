import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.fan import Fan


def test_fan_configuration():
    fan = Fan(pin=22)

    assert fan.pin == 22
    assert fan.is_on is False


def test_fan_turn_on():
    fan = Fan(pin=22)

    fan.turn_on()

    assert fan.is_on is True


def test_fan_turn_off():
    fan = Fan(pin=22)

    fan.turn_on()
    fan.turn_off()

    assert fan.is_on is False


def test_fan_toggle():
    fan = Fan(pin=22)

    fan.toggle()
    assert fan.is_on is True

    fan.toggle()
    assert fan.is_on is False