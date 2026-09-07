class RaspberryDHT:
    """
    Driver para sensor DHT11.

    La librería física se inyecta para permitir
    pruebas en Windows sin Raspberry Pi.
    """

    def __init__(self, pin, dht_device):
        self.pin = pin
        self.device = dht_device

    def read(self):
        """
        Retorna temperatura y humedad.

        Formato:
        {
            "temperature": float,
            "humidity": float
        }
        """

        temperature = self.device.temperature
        humidity = self.device.humidity

        if temperature is None or humidity is None:
            raise RuntimeError(
                "No se pudo obtener una lectura válida del DHT11."
            )

        return {
            "temperature": float(temperature),
            "humidity": float(humidity),
        }