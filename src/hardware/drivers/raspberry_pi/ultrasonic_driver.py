class RaspberryUltrasonic:
    """
    Driver para sensor ultrasónico HC-SR04.

    Calcula la distancia a partir del tiempo
    que permanece activo el pulso ECHO.
    """

    SPEED_OF_SOUND_CM_S = 34300.0

    def __init__(self, trigger_pin, echo_pin, gpio_driver):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.gpio = gpio_driver

        self.gpio.setup_output(self.trigger_pin)
        self.gpio.setup_input(self.echo_pin)

        self.gpio.write_low(self.trigger_pin)

    def calculate_distance(self, echo_time):
        """
        Convierte el tiempo de ida y vuelta del sonido
        en distancia expresada en centímetros.
        """

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