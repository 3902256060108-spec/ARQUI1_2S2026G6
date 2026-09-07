import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.led import LED
from src.hardware.actuators.buzzer import Buzzer
from src.hardware.actuators.servo import Servo
from src.hardware.actuators.fan import Fan

from src.hardware.core.system_state import SystemState
from src.hardware.core.system_controller import SystemController


def create_controller():
    normal_led = LED(pin=1, name="NORMAL")
    warning_led = LED(pin=2, name="WARNING")
    emergency_led = LED(pin=3, name="EMERGENCY")

    buzzer = Buzzer(pin=4)
    servo = Servo(pin=5)
    fan = Fan(pin=6)

    controller = SystemController(
        normal_led=normal_led,
        warning_led=warning_led,
        emergency_led=emergency_led,
        buzzer=buzzer,
        servo=servo,
        fan=fan,
        temp_max=30.0,
        humidity_min=30.0,
        humidity_max=70.0,
    )

    return controller


def test_normal_state():
    controller = create_controller()

    state = controller.update_state(
        temperature=25.0,
        humidity=50.0,
        gas_alert=False,
    )

    assert state == SystemState.NORMAL
    assert controller.normal_led.is_on is True
    assert controller.warning_led.is_on is False
    assert controller.emergency_led.is_on is False
    assert controller.buzzer.is_on is False
    assert controller.fan.is_on is False


def test_warning_state():
    controller = create_controller()

    state = controller.update_state(
        temperature=35.0,
        humidity=50.0,
        gas_alert=False,
    )

    assert state == SystemState.WARNING
    assert controller.normal_led.is_on is False
    assert controller.warning_led.is_on is True
    assert controller.emergency_led.is_on is False
    assert controller.buzzer.is_on is False
    assert controller.fan.is_on is True


def test_emergency_state():
    controller = create_controller()

    state = controller.update_state(
        temperature=25.0,
        humidity=50.0,
        gas_alert=True,
    )

    assert state == SystemState.EMERGENCY
    assert controller.normal_led.is_on is False
    assert controller.warning_led.is_on is False
    assert controller.emergency_led.is_on is True
    assert controller.buzzer.is_on is True
    assert controller.fan.is_on is True
    assert controller.servo.is_open is True