class HardwareRuntime:
    """
    Ejecuta una iteración completa del sistema.

    Lee sensores, actualiza la lógica general
    y actualiza el LCD.
    """

    def __init__(
        self,
        system,
        dht_sensor,
        gas_sensor,
        light_sensor,
        ultrasonic_sensor,
    ):
        self.system = system
        self.dht_sensor = dht_sensor
        self.gas_sensor = gas_sensor
        self.light_sensor = light_sensor
        self.ultrasonic_sensor = ultrasonic_sensor

    def run_once(self):
        # ------------------------------------------
        # 1. Leer sensores independientemente
        # ------------------------------------------
        temperature = None
        humidity = None
        gas_alert = None
        is_dark = None
        distance_cm = None

        # DHT11
        try:
            dht_reading = self.dht_sensor.read()
            temperature = dht_reading["temperature"]
            humidity = dht_reading["humidity"]
        except (RuntimeError, TypeError, KeyError):
            pass

        # MQ-2
        try:
            gas_alert = self.gas_sensor.is_alert()
        except RuntimeError:
            pass

        # LDR
        try:
            is_dark = self.light_sensor.is_dark()
        except RuntimeError:
            pass

        # HC-SR04
        try:
            distance_cm = self.ultrasonic_sensor.read_distance()
        except (RuntimeError, TimeoutError, ValueError):
            pass

        # ------------------------------------------
        # 2. Actualizar sistema
        # ------------------------------------------
        state = self.system.update(
            temperature=temperature,
            humidity=humidity,
            gas_alert=gas_alert,
            distance_cm=distance_cm,
        )

        # Solo actualizar iluminación automática
        # cuando existe una lectura válida.
        if is_dark is not None:
            self.system.lighting_controller.update_automatic_digital(
                is_dark=is_dark
            )

        # ------------------------------------------
        # 3. Actualizar LCD
        # ------------------------------------------
        gas_text = (
            "ALERTA"
            if gas_alert is True
            else "OK"
            if gas_alert is False
            else "N/A"
        )

        light_text = (
            "OSCURO"
            if is_dark is True
            else "CLARO"
            if is_dark is False
            else "N/A"
        )

        self.system.display_controller.next_screen(
            temperature=temperature,
            humidity=humidity,
            gas_value=gas_text,
            distance_cm=distance_cm,
            light_value=light_text,
            door_state=self.system.hardware["servo"].door_state.value,
            system_state=state.value,
        )

        # ------------------------------------------
        # 4. Retornar snapshot
        # ------------------------------------------
        return {
            "temperature": temperature,
            "humidity": humidity,
            "gas_alert": gas_alert,
            "is_dark": is_dark,
            "distance_cm": distance_cm,
            "state": state,
        }