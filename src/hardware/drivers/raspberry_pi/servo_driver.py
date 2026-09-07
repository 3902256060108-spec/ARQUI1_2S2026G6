from src.hardware.actuators.servo import DoorState


class RaspberryServo:
    """
    Control del servomotor SG90 mediante PWM.

    Se utiliza PWM de 50 Hz.
    Los ángulos de puerta cerrada y abierta
    pueden ajustarse posteriormente durante
    la calibración física.
    """

    PWM_FREQUENCY = 50

    CLOSED_ANGLE = 0
    OPEN_ANGLE = 90

    def __init__(self, pin, gpio_driver):
        self.pin = pin
        self.gpio = gpio_driver
        self._door_state = DoorState.CLOSED

        self.gpio.setup_output(self.pin)

        self.pwm = self.gpio.create_pwm(
            self.pin,
            self.PWM_FREQUENCY,
        )

        self.pwm.start(0)

    @property
    def door_state(self):
        return self._door_state

    @property
    def is_open(self):
        return self._door_state == DoorState.OPEN

    def _angle_to_duty_cycle(self, angle):
        if angle < 0 or angle > 180:
            raise ValueError(
                "El ángulo del servo debe estar entre 0 y 180 grados."
            )

        return 2.5 + (angle / 180.0) * 10.0

    def set_angle(self, angle):
        duty_cycle = self._angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def open_door(self):
        self.set_angle(self.OPEN_ANGLE)
        self._door_state = DoorState.OPEN

    def close_door(self):
        self.set_angle(self.CLOSED_ANGLE)
        self._door_state = DoorState.CLOSED

    def toggle_door(self):
        if self.is_open:
            self.close_door()
        else:
            self.open_door()

    def stop(self):
        self.pwm.stop()