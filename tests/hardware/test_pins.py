import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.config import pins


def test_gpio_assignments_are_unique():
    gpio_pins = [
        pins.DHT_PIN,
        pins.GAS_PIN,
        pins.LIGHT_SENSOR_PIN,
        pins.ULTRASONIC_TRIGGER_PIN,
        pins.ULTRASONIC_ECHO_PIN,

        pins.SERVO_PIN,
        pins.BUZZER_PIN,
        pins.FAN_PIN,

        pins.LED_NORMAL_PIN,
        pins.LED_WARNING_PIN,
        pins.LED_EMERGENCY_PIN,

        pins.LIGHT_1_PIN,
        pins.LIGHT_2_PIN,

        pins.BUTTON_DOOR_PIN,
        pins.BUTTON_LIGHT_MODE_PIN,
        pins.BUTTON_SILENCE_PIN,
        pins.BUTTON_RESET_PIN,

        pins.LCD_RS_PIN,
        pins.LCD_ENABLE_PIN,
        pins.LCD_D4_PIN,
        pins.LCD_D5_PIN,
        pins.LCD_D6_PIN,
        pins.LCD_D7_PIN,
    ]

    assert len(gpio_pins) == len(set(gpio_pins))