from src.hardware.config import pins

from src.hardware.drivers.raspberry_pi.led_driver import RaspberryLED
from src.hardware.drivers.raspberry_pi.buzzer_driver import RaspberryBuzzer
from src.hardware.drivers.raspberry_pi.fan_driver import RaspberryFan
from src.hardware.drivers.raspberry_pi.servo_driver import RaspberryServo
from src.hardware.drivers.raspberry_pi.button_driver import RaspberryButton
from src.hardware.drivers.raspberry_pi.light_driver import RaspberryLightSensor
from src.hardware.drivers.raspberry_pi.gas_driver import RaspberryGasSensor
from src.hardware.drivers.raspberry_pi.ultrasonic_driver import RaspberryUltrasonic
from src.hardware.drivers.raspberry_pi.lcd_driver import RaspberryLCD


def create_raspberry_drivers(gpio_driver):
    """
    Crea los dispositivos que dependen de GPIO.

    No importa RPi.GPIO directamente, por lo que esta
    función también puede probarse desde Windows.
    """

    return {
        # LEDs de estado
        "normal_led": RaspberryLED(
            pins.LED_NORMAL_PIN,
            gpio_driver,
        ),
        "warning_led": RaspberryLED(
            pins.LED_WARNING_PIN,
            gpio_driver,
        ),
        "emergency_led": RaspberryLED(
            pins.LED_EMERGENCY_PIN,
            gpio_driver,
        ),

        # Iluminación
        "light_1": RaspberryLED(
            pins.LIGHT_1_PIN,
            gpio_driver,
        ),
        "light_2": RaspberryLED(
            pins.LIGHT_2_PIN,
            gpio_driver,
        ),

        # Actuadores
        "buzzer": RaspberryBuzzer(
            pins.BUZZER_PIN,
            gpio_driver,
        ),
        "fan": RaspberryFan(
            pins.FAN_PIN,
            gpio_driver,
        ),
        "servo": RaspberryServo(
            pins.SERVO_PIN,
            gpio_driver,
        ),

        # Botones
        "door_button": RaspberryButton(
            pins.BUTTON_DOOR_PIN,
            gpio_driver,
        ),
        "light_mode_button": RaspberryButton(
            pins.BUTTON_LIGHT_MODE_PIN,
            gpio_driver,
        ),
        "silence_button": RaspberryButton(
            pins.BUTTON_SILENCE_PIN,
            gpio_driver,
        ),
        "reset_button": RaspberryButton(
            pins.BUTTON_RESET_PIN,
            gpio_driver,
        ),

        # Sensores digitales
        "light_sensor": RaspberryLightSensor(
            pins.LIGHT_SENSOR_PIN,
            gpio_driver,
        ),
        "gas_sensor": RaspberryGasSensor(
            pins.GAS_PIN,
            gpio_driver,
        ),

        # Ultrasónico
        "ultrasonic": RaspberryUltrasonic(
            trigger_pin=pins.ULTRASONIC_TRIGGER_PIN,
            echo_pin=pins.ULTRASONIC_ECHO_PIN,
            gpio_driver=gpio_driver,
        ),

        # LCD
        "lcd": RaspberryLCD(
            rs_pin=pins.LCD_RS_PIN,
            enable_pin=pins.LCD_ENABLE_PIN,
            d4_pin=pins.LCD_D4_PIN,
            d5_pin=pins.LCD_D5_PIN,
            d6_pin=pins.LCD_D6_PIN,
            d7_pin=pins.LCD_D7_PIN,
            gpio_driver=gpio_driver,
        ),
    }