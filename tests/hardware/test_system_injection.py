import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.config.hardware_setup import create_hardware
from src.hardware.config.sensor_setup import create_sensors
from src.hardware.core.system import HardwareSystem
from src.hardware.display.lcd_display import LCDDisplay


def test_system_uses_injected_hardware():
    hardware = create_hardware()

    system = HardwareSystem(
        hardware=hardware
    )

    assert system.hardware is hardware


def test_system_uses_injected_sensors():
    sensors = create_sensors()

    system = HardwareSystem(
        sensors=sensors
    )

    assert system.sensors is sensors


def test_system_keeps_default_behavior():
    system = HardwareSystem()

    assert system.hardware is not None
    assert system.sensors is not None
    assert isinstance(system.lcd, LCDDisplay)