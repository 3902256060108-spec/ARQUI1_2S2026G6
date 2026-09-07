import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.servo_driver import RaspberryServo
from src.hardware.actuators.servo import DoorState


class FakePWM:
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency
        self.started_with = None
        self.duty_cycle = None
        self.stopped = False

    def start(self, duty_cycle):
        self.started_with = duty_cycle

    def ChangeDutyCycle(self, duty_cycle):
        self.duty_cycle = duty_cycle

    def stop(self):
        self.stopped = True


class FakeGPIO:
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0

    def __init__(self):
        self.configured = {}
        self.pwm = None

    def setup(self, pin, mode):
        self.configured[pin] = mode

    def output(self, pin, value):
        pass

    def input(self, pin):
        return self.LOW

    def PWM(self, pin, frequency):
        self.pwm = FakePWM(pin, frequency)
        return self.pwm

    def cleanup(self):
        pass


def create_servo():
    fake = FakeGPIO()
    driver = GPIODriver(fake)

    servo = RaspberryServo(
        pin=18,
        gpio_driver=driver,
    )

    return fake, servo


def test_servo_configures_output():
    fake, servo = create_servo()

    assert fake.configured[18] == fake.OUT


def test_servo_uses_50hz_pwm():
    fake, servo = create_servo()

    assert fake.pwm.frequency == 50
    assert fake.pwm.started_with == 0


def test_servo_starts_closed():
    fake, servo = create_servo()

    assert servo.door_state == DoorState.CLOSED
    assert servo.is_open is False


def test_servo_opens_door():
    fake, servo = create_servo()

    servo.open_door()

    assert servo.is_open is True
    assert servo.door_state == DoorState.OPEN
    assert fake.pwm.duty_cycle == pytest.approx(7.5)


def test_servo_closes_door():
    fake, servo = create_servo()

    servo.open_door()
    servo.close_door()

    assert servo.is_open is False
    assert servo.door_state == DoorState.CLOSED
    assert fake.pwm.duty_cycle == pytest.approx(2.5)


def test_servo_toggle():
    fake, servo = create_servo()

    servo.toggle_door()
    assert servo.is_open is True

    servo.toggle_door()
    assert servo.is_open is False


def test_servo_rejects_invalid_angle():
    fake, servo = create_servo()

    with pytest.raises(ValueError):
        servo.set_angle(181)

    with pytest.raises(ValueError):
        servo.set_angle(-1)


def test_servo_can_stop_pwm():
    fake, servo = create_servo()

    servo.stop()

    assert fake.pwm.stopped is True