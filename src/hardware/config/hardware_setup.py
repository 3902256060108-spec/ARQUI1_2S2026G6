from src.hardware.config import pins

from src.hardware.actuators.led import LED
from src.hardware.actuators.buzzer import Buzzer
from src.hardware.actuators.servo import Servo
from src.hardware.actuators.fan import Fan

from src.hardware.controls.button import Button


def create_hardware():
    """
    Crea los actuadores y controles usando el
    mapa GPIO centralizado de pins.py.
    """

    hardware = {
        # LEDs de estado
        "normal_led": LED(
            pin=pins.LED_NORMAL_PIN,
            name="NORMAL",
        ),
        "warning_led": LED(
            pin=pins.LED_WARNING_PIN,
            name="WARNING",
        ),
        "emergency_led": LED(
            pin=pins.LED_EMERGENCY_PIN,
            name="EMERGENCY",
        ),

        # Luces
        "light_1": LED(
            pin=pins.LIGHT_1_PIN,
            name="LIGHT_1",
        ),
        "light_2": LED(
            pin=pins.LIGHT_2_PIN,
            name="LIGHT_2",
        ),

        # Actuadores
        "buzzer": Buzzer(
            pin=pins.BUZZER_PIN,
        ),
        "servo": Servo(
            pin=pins.SERVO_PIN,
        ),
        "fan": Fan(
            pin=pins.FAN_PIN,
        ),

        # Botones
        "door_button": Button(
            pin=pins.BUTTON_DOOR_PIN,
            name="DOOR",
        ),
        "light_mode_button": Button(
            pin=pins.BUTTON_LIGHT_MODE_PIN,
            name="LIGHT_MODE",
        ),
        "silence_button": Button(
            pin=pins.BUTTON_SILENCE_PIN,
            name="SILENCE",
        ),
        "reset_button": Button(
            pin=pins.BUTTON_RESET_PIN,
            name="RESET",
        ),
    }

    return hardware