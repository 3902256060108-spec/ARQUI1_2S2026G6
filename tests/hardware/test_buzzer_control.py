import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.buzzer import Buzzer
from src.hardware.controls.button import Button
from src.hardware.controls.buzzer_control import BuzzerControl


def create_control():
    buzzer = Buzzer(pin=18)

    button = Button(
        pin=6,
        name="SILENCE",
    )

    control = BuzzerControl(
        button=button,
        buzzer=buzzer,
    )

    return control, button, buzzer


def test_initially_not_silenced():
    control, button, buzzer = create_control()

    assert control.is_silenced is False


def test_alarm_can_activate():
    control, button, buzzer = create_control()

    control.activate_alarm()

    assert buzzer.is_on is True


def test_silence_turns_buzzer_off():
    control, button, buzzer = create_control()

    buzzer.turn_on()

    control.silence()

    assert buzzer.is_on is False
    assert control.is_silenced is True


def test_alarm_does_not_activate_when_silenced():
    control, button, buzzer = create_control()

    control.silence()
    control.activate_alarm()

    assert buzzer.is_on is False


def test_reset_allows_alarm_again():
    control, button, buzzer = create_control()

    control.silence()
    control.reset_silence()
    control.activate_alarm()

    assert control.is_silenced is False
    assert buzzer.is_on is True


def test_button_is_released_after_silence():
    control, button, buzzer = create_control()

    control.silence()

    assert button.is_pressed is False