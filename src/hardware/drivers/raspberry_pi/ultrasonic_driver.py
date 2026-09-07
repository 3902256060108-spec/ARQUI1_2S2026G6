import time


class RaspberryUltrasonic:
    """
    Driver para sensor ultrasónico HC-SR04.

    Genera el pulso TRIGGER, espera la respuesta ECHO
    y calcula la distancia en centímetros.
    """

    SPEED_OF_SOUND_CM_S = 34300.0
    TRIGGER_PULSE_SECONDS = 0.00001
    DEFAULT_TIMEOUT = 0.03

    def __init__(
        self,
        trigger_pin,
        echo_pin,
        gpio_driver,
        time_provider=None,
        sleep_provider=None,
    ):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.gpio = gpio_driver

        self._time = time_provider or time.monotonic
        self._sleep = sleep_provider or time.sleep

        self.gpio.setup_output(self.trigger_pin)
        self.gpio.setup_input(self.echo_pin)

        self.gpio.write_low(self.trigger_pin)

    def calculate_distance(self, echo_time):
        if echo_time < 0:
            raise ValueError(
                "El tiempo de ECHO no puede ser negativo."
            )

        return (
            echo_time * self.SPEED_OF_SOUND_CM_S
        ) / 2.0

    def object_detected(self, distance_cm, threshold_cm):
        if distance_cm < 0:
            raise ValueError(
                "La distancia no puede ser negativa."
            )

        if threshold_cm < 0:
            raise ValueError(
                "El umbral no puede ser negativo."
            )

        return distance_cm <= threshold_cm

    def read_distance(self, timeout=None):
        """
        Realiza una medición completa del HC-SR04.
        """

        timeout = (
            self.DEFAULT_TIMEOUT
            if timeout is None
            else timeout
        )

        if timeout <= 0:
            raise ValueError(
                "El timeout debe ser mayor que cero."
            )

        # Generar pulso TRIGGER de 10 microsegundos.
        self.gpio.write_low(self.trigger_pin)
        self._sleep(0.000002)

        self.gpio.write_high(self.trigger_pin)
        self._sleep(self.TRIGGER_PULSE_SECONDS)
        self.gpio.write_low(self.trigger_pin)

        wait_start = self._time()

        # Esperar inicio del pulso ECHO.
        while self.gpio.read(self.echo_pin) == self.gpio.LOW:
            if self._time() - wait_start >= timeout:
                raise TimeoutError(
                    "Timeout esperando el inicio del pulso ECHO."
                )

        echo_start = self._time()

        # Esperar final del pulso ECHO.
        while self.gpio.read(self.echo_pin) == self.gpio.HIGH:
            if self._time() - echo_start >= timeout:
                raise TimeoutError(
                    "Timeout esperando el final del pulso ECHO."
                )

        echo_end = self._time()

        echo_time = echo_end - echo_start

        return self.calculate_distance(echo_time)