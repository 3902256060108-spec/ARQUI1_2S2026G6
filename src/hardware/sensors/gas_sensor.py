class GasSensor:
    """
    Abstracción para sensor MQ-2 / MQ-135.

    La lectura física dependerá del módulo utilizado
    y de cómo se conecte a la Raspberry Pi.
    """

    def __init__(self, pin=None, sensor_type="MQ-2"):
        self.pin = pin
        self.sensor_type = sensor_type

    def read(self):
        """
        Retorna la lectura del sensor.

        La implementación física se realizará
        en Raspberry Pi.
        """
        raise NotImplementedError(
            "La lectura real del sensor MQ debe ejecutarse en la Raspberry Pi."
        )

    def is_alert(self, value, threshold):
        """
        Determina si la lectura supera el umbral.
        """
        if threshold is None:
            raise ValueError("El umbral de gas no está configurado.")

        if value < 0:
            raise ValueError("La lectura de gas no puede ser negativa.")

        return value >= threshold