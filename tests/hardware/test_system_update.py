import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.core.system import HardwareSystem
from src.hardware.core.system_state import SystemState
from src.hardware.core.thresholds import (
    TEMP_MAX,
    HUMIDITY_MIN,
    HUMIDITY_MAX,
    DISTANCE_THRESHOLD,
)


TEMP_NORMAL = TEMP_MAX - 1.0
TEMP_WARNING = TEMP_MAX + 1.0

HUMIDITY_NORMAL = (HUMIDITY_MIN + HUMIDITY_MAX) / 2

DISTANCE_PRESENT = DISTANCE_THRESHOLD * 0.5
DISTANCE_ABSENT = DISTANCE_THRESHOLD + 10.0


def test_complete_normal_update():
    system = HardwareSystem()

    state = system.update(
        temperature=TEMP_NORMAL,
        humidity=HUMIDITY_NORMAL,
        gas_alert=False,
        distance_cm=DISTANCE_ABSENT,
        light_value=800,
    )

    assert state == SystemState.NORMAL

    assert system.hardware["normal_led"].is_on is True
    assert system.hardware["warning_led"].is_on is False
    assert system.hardware["emergency_led"].is_on is False

    assert system.hardware["buzzer"].is_on is False
    assert system.hardware["fan"].is_on is False

    assert system.hardware["servo"].is_open is False

    assert system.hardware["light_1"].is_on is False
    assert system.hardware["light_2"].is_on is False


def test_complete_warning_update():
    system = HardwareSystem()

    state = system.update(
        temperature=TEMP_WARNING,
        humidity=HUMIDITY_NORMAL,
        gas_alert=False,
        distance_cm=DISTANCE_ABSENT,
        light_value=200,
    )

    assert state == SystemState.WARNING

    assert system.hardware["warning_led"].is_on is True
    assert system.hardware["fan"].is_on is True

    assert system.hardware["light_1"].is_on is True
    assert system.hardware["light_2"].is_on is True


def test_complete_emergency_update():
    system = HardwareSystem()

    state = system.update(
        temperature=TEMP_NORMAL,
        humidity=HUMIDITY_NORMAL,
        gas_alert=True,
        distance_cm=DISTANCE_ABSENT,
        light_value=800,
    )

    assert state == SystemState.EMERGENCY

    assert system.hardware["emergency_led"].is_on is True
    assert system.hardware["buzzer"].is_on is True
    assert system.hardware["fan"].is_on is True

    assert system.hardware["servo"].is_open is True


def test_presence_opens_door():
    system = HardwareSystem()

    system.update(
        temperature=TEMP_NORMAL,
        humidity=HUMIDITY_NORMAL,
        gas_alert=False,
        distance_cm=DISTANCE_PRESENT,
        light_value=800,
    )

    assert system.hardware["servo"].is_open is True