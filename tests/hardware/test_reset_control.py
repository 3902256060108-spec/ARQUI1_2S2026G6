import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.buzzer import Buzzer
from src.hardware.controls.button import Button
from src.hardware.controls.buzzer_control import BuzzerControl
from src.hardware.controls.reset_control import ResetControl


def create_control():
    buzzer = Buzzer(pin=18)

    silence_button = Button(
        pin=6,
        name="SILENCE",
    )

    reset_button = Button(
        pin=7,
        name="RESET",
    )

    buzzer_control = BuzzerControl(
        button=silence_button,
        buzzer=buzzer,
    )

    reset_control = ResetControl(
        button=reset_button,
        buzzer_control=buzzer_control,
    )

    return reset_control, reset_button, buzzer_control, buzzer


def test_reset_rejected_when_danger_is_active():
    reset_control, button, buzzer_control, buzzer = create_control()

    buzzer_control.silence()

    result = reset_control.reset_alert(
        danger_active=True
    )

    assert result is False
    assert buzzer_control.is_silenced is True


def test_reset_accepted_when_danger_disappears():
    reset_control, button, buzzer_control, buzzer = create_control()

    buzzer_control.silence()

    result = reset_control.reset_alert(
        danger_active=False
    )

    assert result is True
    assert buzzer_control.is_silenced is False


def test_button_is_released_after_successful_reset():
    reset_control, button, buzzer_control, buzzer = create_control()

    reset_control.reset_alert(
        danger_active=False
    )

    assert button.is_pressed is False


def test_button_is_released_after_rejected_reset():
    reset_control, button, buzzer_control, buzzer = create_control()

    reset_control.reset_alert(
        danger_active=True
    )

    assert button.is_pressed is False