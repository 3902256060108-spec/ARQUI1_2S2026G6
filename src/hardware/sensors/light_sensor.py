class LightSensor:
    """
    Abstracción para sensor LDR o sensor de luz equivalente.

    La forma de lectura física dependerá del circuito
    utilizado en la Raspberry Pi.
    """

    def __init__(self, pin=None):
        self.pin = pin

    def read(self):
        """
        Retorna el nivel de iluminación.

        La implementación física se realizará
        en Raspberry Pi.
        """
        raise NotImplementedError(
            "La lectura real del sensor de luz debe ejecutarse en la Raspberry Pi."
        )

    def is_dark(self, value, threshold):
        """
        Determina si el nivel de luz está por debajo
        del umbral configurado.
        """
        if threshold is None:
            raise ValueError("El umbral de luz no está configurado.")

        if value < 0:
            raise ValueError("La lectura de luz no puede ser negativa.")

        return value < threshold