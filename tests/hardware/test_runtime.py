import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.core.runtime import HardwareRuntime
from src.hardware.core.system import HardwareSystem
from src.hardware.core.system_state import SystemState


class FakeDHT:
    def read(self):
        return {
            "temperature": 25.0,
            "humidity": 50.0,
        }


class FakeGas:
    def __init__(self, alert=False):
        self.alert = alert

    def is_alert(self):
        return self.alert


class FakeLight:
    def __init__(self, dark=False):
        self.dark = dark

    def is_dark(self):
        return self.dark


class FakeUltrasonic:
    def __init__(self, distance=100.0):
        self.distance = distance

    def read_distance(self):
        return self.distance


def create_runtime(
    gas_alert=False,
    dark=False,
    distance=100.0,
):
    system = HardwareSystem()

    runtime = HardwareRuntime(
        system=system,
        dht_sensor=FakeDHT(),
        gas_sensor=FakeGas(gas_alert),
        light_sensor=FakeLight(dark),
        ultrasonic_sensor=FakeUltrasonic(distance),
    )

    return system, runtime


def test_runtime_reads_all_sensors():
    system, runtime = create_runtime()

    result = runtime.run_once()

    assert result["temperature"] == 25.0
    assert result["humidity"] == 50.0
    assert result["gas_alert"] is False
    assert result["is_dark"] is False
    assert result["distance_cm"] == 100.0


def test_runtime_normal_state():
    system, runtime = create_runtime()

    result = runtime.run_once()

    assert result["state"] == SystemState.NORMAL
    assert system.hardware["normal_led"].is_on is True


def test_runtime_detects_emergency():
    system, runtime = create_runtime(
        gas_alert=True
    )

    result = runtime.run_once()

    assert result["state"] == SystemState.EMERGENCY
    assert system.hardware["emergency_led"].is_on is True
    assert system.hardware["buzzer"].is_on is True
    assert system.hardware["servo"].is_open is True


def test_runtime_opens_door_for_presence():
    system, runtime = create_runtime(
        distance=20.0
    )

    runtime.run_once()

    assert system.hardware["servo"].is_open is True


def test_runtime_turns_lights_on_when_dark():
    system, runtime = create_runtime(
        dark=True
    )

    runtime.run_once()

    assert system.hardware["light_1"].is_on is True
    assert system.hardware["light_2"].is_on is True


def test_runtime_updates_lcd():
    system, runtime = create_runtime()

    runtime.run_once()

    assert (
        system.lcd.line1 != ""
        or system.lcd.line2 != ""
    )