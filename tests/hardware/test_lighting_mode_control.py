import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.actuators.led import LED
from src.hardware.controls.button import Button
from src.hardware.controls.lighting_mode_control import LightingModeControl
from src.hardware.core.lighting_controller import (
    LightingController,
    LightingMode,
)


def create_control():
    light1 = LED(pin=10)
    light2 = LED(pin=11)

    lighting_controller = LightingController(
        lights=[light1, light2],
        light_threshold=500,
    )

    button = Button(
        pin=5,
        name="LIGHT_MODE",
    )

    control = LightingModeControl(
        button=button,
        lighting_controller=lighting_controller,
    )

    return control, button, lighting_controller


def test_initial_mode_is_automatic():
    control, button, controller = create_control()

    assert controller.mode == LightingMode.AUTOMATIC


def test_button_changes_to_manual():
    control, button, controller = create_control()

    mode = control.handle_press()

    assert mode == LightingMode.MANUAL
    assert controller.mode == LightingMode.MANUAL


def test_second_press_returns_to_automatic():
    control, button, controller = create_control()

    control.handle_press()
    mode = control.handle_press()

    assert mode == LightingMode.AUTOMATIC
    assert controller.mode == LightingMode.AUTOMATIC


def test_button_is_released_after_press():
    control, button, controller = create_control()

    control.handle_press()

    assert button.is_pressed is False