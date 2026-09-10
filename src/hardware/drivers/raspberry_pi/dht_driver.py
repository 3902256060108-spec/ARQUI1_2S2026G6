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

        Si el DHT11 no entrega una lectura válida,
        retorna None en ambos valores sin detener
        el resto del sistema.

        Formato:
        {
            "temperature": float | None,
            "humidity": float | None
        }
        """

        try:
            temperature = self.device.temperature
            humidity = self.device.humidity

            if temperature is None or humidity is None:
                return {
                    "temperature": None,
                    "humidity": None,
                }

            return {
                "temperature": float(temperature),
                "humidity": float(humidity),
            }

        except RuntimeError:
            return {
                "temperature": None,
                "humidity": None,
            }