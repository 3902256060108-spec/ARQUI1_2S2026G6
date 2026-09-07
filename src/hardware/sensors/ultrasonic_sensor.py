class UltrasonicSensor:
    """
    Abstracción del sensor ultrasónico HC-SR04.

    La lectura física mediante GPIO se implementará
    cuando el código se ejecute en la Raspberry Pi.
    """

    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

    def read_distance(self):
        """
        Retorna la distancia medida en centímetros.

        La lectura real requiere GPIO de Raspberry Pi.
        """
        raise NotImplementedError(
            "La lectura real del HC-SR04 debe ejecutarse en la Raspberry Pi."
        )

    def object_detected(self, distance_cm, threshold_cm):
        """
        Determina si hay un objeto dentro del rango configurado.
        """
        if distance_cm < 0:
            raise ValueError("La distancia no puede ser negativa.")

        return distance_cm <= threshold_cm