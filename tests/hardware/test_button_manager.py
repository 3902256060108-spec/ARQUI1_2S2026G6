import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.controls.button_manager import ButtonManager


class FakeButton:
    def __init__(self):
        self.pressed = False

    def is_pressed(self):
        return self.pressed


def create_manager():
    door = FakeButton()
    light_mode = FakeButton()
    silence = FakeButton()
    reset = FakeButton()

    manager = ButtonManager(
        door_button=door,
        light_mode_button=light_mode,
        silence_button=silence,
        reset_button=reset,
    )

    return manager, door, light_mode, silence, reset


def test_no_button_pressed():
    manager, *_ = create_manager()

    assert manager.read_pressed() == []


def test_detects_door_press():
    manager, door, *_ = create_manager()

    door.pressed = True

    assert manager.read_pressed() == ["door"]


def test_held_button_is_not_repeated():
    manager, door, *_ = create_manager()

    door.pressed = True

    assert manager.read_pressed() == ["door"]
    assert manager.read_pressed() == []


def test_button_can_be_pressed_again_after_release():
    manager, door, *_ = create_manager()

    door.pressed = True
    assert manager.read_pressed() == ["door"]

    door.pressed = False
    assert manager.read_pressed() == []

    door.pressed = True
    assert manager.read_pressed() == ["door"]


def test_detects_multiple_buttons():
    manager, door, light_mode, silence, reset = create_manager()

    door.pressed = True
    silence.pressed = True

    pressed = manager.read_pressed()

    assert "door" in pressed
    assert "silence" in pressed
    assert len(pressed) == 2