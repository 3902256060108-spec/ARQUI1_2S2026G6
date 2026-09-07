import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.buzzer import Buzzer


def test_buzzer_configuration():
    buzzer = Buzzer(pin=18)

    assert buzzer.pin == 18
    assert buzzer.is_on is False


def test_buzzer_turn_on():
    buzzer = Buzzer(pin=18)

    buzzer.turn_on()

    assert buzzer.is_on is True


def test_buzzer_turn_off():
    buzzer = Buzzer(pin=18)

    buzzer.turn_on()
    buzzer.turn_off()

    assert buzzer.is_on is False


def test_buzzer_toggle():
    buzzer = Buzzer(pin=18)

    buzzer.toggle()
    assert buzzer.is_on is True

    buzzer.toggle()
    assert buzzer.is_on is False