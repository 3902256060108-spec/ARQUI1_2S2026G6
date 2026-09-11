import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.led import LED
from src.hardware.config.hardware_setup import create_hardware
from src.hardware.core.lighting_controller import LightingController
from src.hardware.core.lighting_controller import (
    LightingController,
    LightingMode,
)


def create_controller():
    light1 = LED(pin=10, name="LUZ_1")
    light2 = LED(pin=11, name="LUZ_2")

    controller = LightingController(
        lights=[light1, light2],
        light_threshold=500,
    )

    return controller, light1, light2


def test_default_mode_is_automatic():
    controller, light1, light2 = create_controller()

    assert controller.mode == LightingMode.AUTOMATIC


def test_dark_environment_turns_lights_on():
    controller, light1, light2 = create_controller()

    controller.update_automatic(light_value=200)

    assert light1.is_on is True
    assert light2.is_on is True


def test_bright_environment_turns_lights_off():
    controller, light1, light2 = create_controller()

    light1.turn_on()
    light2.turn_on()

    controller.update_automatic(light_value=800)

    assert light1.is_on is False
    assert light2.is_on is False


def test_toggle_to_manual_mode():
    controller, light1, light2 = create_controller()

    mode = controller.toggle_mode()

    assert mode == LightingMode.MANUAL


def test_manual_turn_on():
    controller, light1, light2 = create_controller()

    controller.toggle_mode()
    controller.set_manual_state(True)

    assert light1.is_on is True
    assert light2.is_on is True


def test_manual_turn_off():
    controller, light1, light2 = create_controller()

    controller.toggle_mode()

    light1.turn_on()
    light2.turn_on()

    controller.set_manual_state(False)

    assert light1.is_on is False
    assert light2.is_on is False


def test_automatic_update_does_nothing_in_manual_mode():
    controller, light1, light2 = create_controller()

    controller.toggle_mode()
    controller.set_manual_state(True)

    controller.update_automatic(light_value=900)

    assert light1.is_on is True
    assert light2.is_on is True


def test_manual_control_rejected_in_automatic_mode():
    controller, light1, light2 = create_controller()

    try:
        controller.set_manual_state(True)
        assert False, "Se esperaba RuntimeError"
    except RuntimeError:
        assert True


def test_missing_light_threshold():
    controller, light1, light2 = create_controller()

    controller.light_threshold = None

    try:
        controller.update_automatic(light_value=300)
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True


def test_negative_light_value():
    controller, light1, light2 = create_controller()

    try:
        controller.update_automatic(light_value=-1)
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True

def test_automatic_digital_turns_lights_on_when_dark():
    controller, light1, light2 = create_controller()

    controller.update_automatic_digital(True)

    assert light1.is_on is True
    assert light2.is_on is True


def test_automatic_digital_turns_lights_off_when_clear():
    controller, light1, light2 = create_controller()

    controller.update_automatic_digital(True)
    controller.update_automatic_digital(False)

    assert light1.is_on is False
    assert light2.is_on is False


def test_automatic_digital_rejects_non_boolean_value():
    controller, light1, light2 = create_controller()

    try:
        controller.update_automatic_digital(500)
        assert False, "Se esperaba TypeError"

    except TypeError:
        assert True