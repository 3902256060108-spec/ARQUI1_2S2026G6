from src.python import arm64_runner


class TemperatureARM64:
    """
    Recolecta temperaturas obtenidas del DHT11
    y las entrega al módulo ARM64.

    Python solamente recolecta y transfiere datos.
    Los cálculos estadísticos corresponden a ARM64.
    """

    def __init__(
        self,
        dht_sensor,
        sample_count=20,
        runner=None,
    ):
        if sample_count < 20:
            raise ValueError(
                "Se requieren al menos 20 temperaturas."
            )

        self.dht_sensor = dht_sensor
        self.sample_count = sample_count
        self.runner = runner or arm64_runner
        self.temperatures = []

    def collect_temperatures(self):
        temperatures = []

        while len(temperatures) < self.sample_count:
            try:
                reading = self.dht_sensor.read()

                temperature = reading["temperature"]

                if temperature is None:
                    continue

                temperatures.append(
                    int(temperature)
                )

            except RuntimeError:
                continue

        return temperatures

    def process(self):
        temperatures = self.collect_temperatures()

        self.runner.generar_datos(
            temperatures
        )

        self.runner.ejecutar_arm64()

        results = self.runner.leer_resultados()

        return {
            "temperatures": temperatures,
            "results": results,
        }

    def add_temperature(self, temperature):
        """
        Agrega una temperatura obtenida durante
        el ciclo normal del sistema.
        """

        if temperature is None:
            return False

        self.temperatures.append(
            int(temperature)
        )

        return len(self.temperatures) >= self.sample_count


    def is_ready(self):
        return len(self.temperatures) >= self.sample_count


    def process_collected(self):
        """
        Envía a ARM64 las temperaturas ya recolectadas.
        No realiza cálculos estadísticos en Python.
        """

        if not self.is_ready():
            return None

        temperatures = self.temperatures[
            :self.sample_count
        ]

        self.runner.generar_datos(
            temperatures
        )

        self.runner.ejecutar_arm64()

        results = self.runner.leer_resultados()

        # Quitamos solamente las muestras procesadas.
        self.temperatures = self.temperatures[
            self.sample_count:
        ]

        return {
            "temperatures": temperatures,
            "results": results,
        }