import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.core.system import HardwareSystem
from src.hardware.core.lighting_controller import LightingMode


def test_system_can_be_created():
    system = HardwareSystem()

    assert system is not None


def test_system_contains_sensors():
    system = HardwareSystem()

    assert "dht" in system.sensors
    assert "gas" in system.sensors
    assert "light" in system.sensors
    assert "ultrasonic" in system.sensors


def test_system_contains_hardware():
    system = HardwareSystem()

    assert "normal_led" in system.hardware
    assert "warning_led" in system.hardware
    assert "emergency_led" in system.hardware
    assert "buzzer" in system.hardware
    assert "servo" in system.hardware
    assert "fan" in system.hardware


def test_system_starts_with_automatic_lighting():
    system = HardwareSystem()

    assert (
        system.lighting_controller.mode
        == LightingMode.AUTOMATIC
    )


def test_system_starts_with_door_closed():
    system = HardwareSystem()

    assert system.hardware["servo"].is_open is False


def test_system_starts_with_buzzer_off():
    system = HardwareSystem()

    assert system.hardware["buzzer"].is_on is False