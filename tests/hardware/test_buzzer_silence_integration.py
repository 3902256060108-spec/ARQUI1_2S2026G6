import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.controls.buzzer_control import BuzzerControl
from src.hardware.core.system_controller import SystemController


class FakeLED:
    def turn_on(self):
        pass

    def turn_off(self):
        pass


class FakeBuzzer:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False


class FakeServo:
    def open_door(self):
        pass


class FakeFan:
    def turn_on(self):
        pass

    def turn_off(self):
        pass


class FakeButton:
    pass


def create_controller():
    buzzer = FakeBuzzer()

    buzzer_control = BuzzerControl(
        button=FakeButton(),
        buzzer=buzzer,
    )

    controller = SystemController(
        normal_led=FakeLED(),
        warning_led=FakeLED(),
        emergency_led=FakeLED(),
        buzzer=buzzer,
        servo=FakeServo(),
        fan=FakeFan(),
        temp_max=30.0,
        humidity_min=30.0,
        humidity_max=70.0,
        buzzer_control=buzzer_control,
    )

    return controller, buzzer_control, buzzer


def test_buzzer_stays_silent_during_persistent_emergency():
    controller, buzzer_control, buzzer = create_controller()

    controller.update_state(
        temperature=25.0,
        humidity=50.0,
        gas_alert=True,
    )

    assert buzzer.is_on is True

    buzzer_control.silence()

    assert buzzer.is_on is False

    controller.update_state(
        temperature=25.0,
        humidity=50.0,
        gas_alert=True,
    )

    assert buzzer.is_on is False