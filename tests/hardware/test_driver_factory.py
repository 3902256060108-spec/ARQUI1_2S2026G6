import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.config import pins
from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.driver_factory import (
    create_raspberry_drivers,
)


class FakePWM:
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency

    def start(self, duty_cycle):
        pass

    def ChangeDutyCycle(self, duty_cycle):
        pass

    def stop(self):
        pass


class FakeGPIO:
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0

    def __init__(self):
        self.configured = {}
        self.outputs = {}

    def setup(self, pin, mode):
        self.configured[pin] = mode

    def output(self, pin, value):
        self.outputs[pin] = value

    def input(self, pin):
        return self.LOW

    def PWM(self, pin, frequency):
        return FakePWM(pin, frequency)

    def cleanup(self):
        pass


def test_factory_creates_all_gpio_devices():
    fake = FakeGPIO()
    gpio_driver = GPIODriver(fake)

    devices = create_raspberry_drivers(gpio_driver)

    expected = {
        "normal_led",
        "warning_led",
        "emergency_led",
        "light_1",
        "light_2",
        "buzzer",
        "fan",
        "servo",
        "door_button",
        "light_mode_button",
        "silence_button",
        "reset_button",
        "light_sensor",
        "gas_sensor",
        "ultrasonic",
        "lcd",
    }

    assert set(devices.keys()) == expected


def test_factory_uses_centralized_pin_map():
    fake = FakeGPIO()
    gpio_driver = GPIODriver(fake)

    devices = create_raspberry_drivers(gpio_driver)

    assert devices["normal_led"].pin == pins.LED_NORMAL_PIN
    assert devices["servo"].pin == pins.SERVO_PIN
    assert devices["gas_sensor"].pin == pins.GAS_PIN
    assert devices["light_sensor"].pin == pins.LIGHT_SENSOR_PIN

    assert (
        devices["ultrasonic"].trigger_pin
        == pins.ULTRASONIC_TRIGGER_PIN
    )

    assert (
        devices["ultrasonic"].echo_pin
        == pins.ULTRASONIC_ECHO_PIN
    )