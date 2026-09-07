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
        # 1. Leer sensores
        # ------------------------------------------
        dht_reading = self.dht_sensor.read()

        temperature = dht_reading["temperature"]
        humidity = dht_reading["humidity"]

        gas_alert = self.gas_sensor.is_alert()
        is_dark = self.light_sensor.is_dark()

        distance_cm = self.ultrasonic_sensor.read_distance()

        # ------------------------------------------
        # 2. Actualizar sistema
        # ------------------------------------------
        state = self.system.update(
            temperature=temperature,
            humidity=humidity,
            gas_alert=gas_alert,
            distance_cm=distance_cm,
        )

        self.system.lighting_controller.update_automatic_digital(
            is_dark=is_dark
        )

        # ------------------------------------------
        # 3. Actualizar LCD
        # ------------------------------------------
        self.system.display_controller.next_screen(
            temperature=temperature,
            humidity=humidity,
            gas_value="ALERTA" if gas_alert else "OK",
            distance_cm=distance_cm,
            light_value="OSCURO" if is_dark else "CLARO",
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