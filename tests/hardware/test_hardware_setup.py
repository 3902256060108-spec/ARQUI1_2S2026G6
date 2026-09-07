import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.config import pins
from src.hardware.config.hardware_setup import create_hardware


def test_hardware_uses_configured_gpio():
    hardware = create_hardware()

    assert hardware["normal_led"].pin == pins.LED_NORMAL_PIN
    assert hardware["warning_led"].pin == pins.LED_WARNING_PIN
    assert hardware["emergency_led"].pin == pins.LED_EMERGENCY_PIN

    assert hardware["light_1"].pin == pins.LIGHT_1_PIN
    assert hardware["light_2"].pin == pins.LIGHT_2_PIN

    assert hardware["buzzer"].pin == pins.BUZZER_PIN
    assert hardware["servo"].pin == pins.SERVO_PIN
    assert hardware["fan"].pin == pins.FAN_PIN

    assert hardware["door_button"].pin == pins.BUTTON_DOOR_PIN
    assert hardware["light_mode_button"].pin == pins.BUTTON_LIGHT_MODE_PIN
    assert hardware["silence_button"].pin == pins.BUTTON_SILENCE_PIN
    assert hardware["reset_button"].pin == pins.BUTTON_RESET_PIN


def test_hardware_starts_in_safe_state():
    hardware = create_hardware()

    assert hardware["normal_led"].is_on is False
    assert hardware["warning_led"].is_on is False
    assert hardware["emergency_led"].is_on is False

    assert hardware["light_1"].is_on is False
    assert hardware["light_2"].is_on is False

    assert hardware["buzzer"].is_on is False
    assert hardware["fan"].is_on is False
    assert hardware["servo"].is_open is False