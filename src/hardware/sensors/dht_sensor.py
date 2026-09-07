class DHTSensor:
    """
    Abstracción del sensor DHT11/DHT22.

    Por ahora esta clase separa la lógica del proyecto
    del acceso físico al GPIO. La lectura real se
    implementará cuando probemos en la Raspberry Pi.
    """

    def __init__(self, pin, sensor_type="DHT11"):
        self.pin = pin
        self.sensor_type = sensor_type

    def read(self):
        """
        Retorna:
            tuple: (temperatura, humedad)

        La lectura física se implementará en Raspberry Pi.
        """
        raise NotImplementedError(
            "La lectura real del DHT debe ejecutarse en la Raspberry Pi."
        )