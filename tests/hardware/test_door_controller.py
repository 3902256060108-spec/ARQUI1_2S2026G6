import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.servo import Servo, DoorState
from src.hardware.core.door_controller import DoorController


class FakeClock:
    def __init__(self):
        self.current_time = 0

    def __call__(self):
        return self.current_time

    def advance(self, seconds):
        self.current_time += seconds


def create_door_controller():
    servo = Servo(pin=12)
    clock = FakeClock()

    controller = DoorController(
        servo=servo,
        distance_threshold=30.0,
        open_time=5,
        time_provider=clock,
    )

    return controller, clock


def test_open_door_when_person_detected():
    controller, clock = create_door_controller()

    state = controller.update(distance_cm=20.0)

    assert state == DoorState.OPEN
    assert controller.servo.is_open is True


def test_door_remains_open_before_timeout():
    controller, clock = create_door_controller()

    controller.update(distance_cm=20.0)

    clock.advance(3)

    state = controller.update(distance_cm=50.0)

    assert state == DoorState.OPEN


def test_door_closes_after_timeout():
    controller, clock = create_door_controller()

    controller.update(distance_cm=20.0)

    clock.advance(5)

    state = controller.update(distance_cm=50.0)

    assert state == DoorState.CLOSED
    assert controller.servo.is_open is False


def test_new_detection_restarts_timer():
    controller, clock = create_door_controller()

    controller.update(distance_cm=20.0)

    clock.advance(4)
    controller.update(distance_cm=20.0)

    clock.advance(4)
    state = controller.update(distance_cm=50.0)

    assert state == DoorState.OPEN

    clock.advance(1)
    state = controller.update(distance_cm=50.0)

    assert state == DoorState.CLOSED


def test_exact_threshold_opens_door():
    controller, clock = create_door_controller()

    state = controller.update(distance_cm=30.0)

    assert state == DoorState.OPEN


def test_negative_distance():
    controller, clock = create_door_controller()

    try:
        controller.update(distance_cm=-1)
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True