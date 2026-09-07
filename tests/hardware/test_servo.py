import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.servo import Servo, DoorState


def test_servo_configuration():
    servo = Servo(pin=12)

    assert servo.pin == 12
    assert servo.door_state == DoorState.CLOSED
    assert servo.is_open is False


def test_open_door():
    servo = Servo(pin=12)

    servo.open_door()

    assert servo.door_state == DoorState.OPEN
    assert servo.is_open is True


def test_close_door():
    servo = Servo(pin=12)

    servo.open_door()
    servo.close_door()

    assert servo.door_state == DoorState.CLOSED
    assert servo.is_open is False


def test_toggle_door():
    servo = Servo(pin=12)

    servo.toggle_door()
    assert servo.is_open is True

    servo.toggle_door()
    assert servo.is_open is False