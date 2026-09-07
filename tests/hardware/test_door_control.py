import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.servo import Servo, DoorState
from src.hardware.controls.button import Button
from src.hardware.controls.door_control import DoorControl


def create_control():
    servo = Servo(pin=12)

    button = Button(
        pin=5,
        name="DOOR",
    )

    control = DoorControl(
        button=button,
        servo=servo,
    )

    return control, button, servo


def test_door_initially_closed():
    control, button, servo = create_control()

    assert servo.door_state == DoorState.CLOSED


def test_first_press_opens_door():
    control, button, servo = create_control()

    state = control.handle_press()

    assert state == DoorState.OPEN
    assert servo.is_open is True


def test_second_press_closes_door():
    control, button, servo = create_control()

    control.handle_press()
    state = control.handle_press()

    assert state == DoorState.CLOSED
    assert servo.is_open is False


def test_button_released_after_press():
    control, button, servo = create_control()

    control.handle_press()

    assert button.is_pressed is False