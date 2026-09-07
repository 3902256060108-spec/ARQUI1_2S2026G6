import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.controls.button_actions import ButtonActions


class FakeDoorControl:
    def __init__(self):
        self.calls = 0

    def toggle_door(self):
        self.calls += 1


class FakeLightingModeControl:
    def __init__(self):
        self.calls = 0

    def toggle_mode(self):
        self.calls += 1


class FakeBuzzerControl:
    def __init__(self):
        self.calls = 0

    def silence(self):
        self.calls += 1


class FakeResetControl:
    def __init__(self):
        self.calls = 0
        self.last_danger_active = None

    def reset(self, danger_active=False):
        self.calls += 1
        self.last_danger_active = danger_active


def create_actions():
    door = FakeDoorControl()
    lighting = FakeLightingModeControl()
    buzzer = FakeBuzzerControl()
    reset = FakeResetControl()

    actions = ButtonActions(
        door_control=door,
        lighting_mode_control=lighting,
        buzzer_control=buzzer,
        reset_control=reset,
    )

    return actions, door, lighting, buzzer, reset


def test_door_button_executes_door_action():
    actions, door, _, _, _ = create_actions()

    actions.process(["door"])

    assert door.calls == 1


def test_light_mode_button_executes_action():
    actions, _, lighting, _, _ = create_actions()

    actions.process(["light_mode"])

    assert lighting.calls == 1


def test_silence_button_executes_action():
    actions, _, _, buzzer, _ = create_actions()

    actions.process(["silence"])

    assert buzzer.calls == 1


def test_reset_button_receives_danger_state():
    actions, _, _, _, reset = create_actions()

    actions.process(
        ["reset"],
        danger_active=True,
    )

    assert reset.calls == 1
    assert reset.last_danger_active is True


def test_multiple_actions_can_be_processed():
    actions, door, lighting, buzzer, reset = create_actions()

    actions.process(
        [
            "door",
            "light_mode",
            "silence",
            "reset",
        ],
        danger_active=False,
    )

    assert door.calls == 1
    assert lighting.calls == 1
    assert buzzer.calls == 1
    assert reset.calls == 1