class DisplayController:
    """
    Controla la rotación de información mostrada
    en la pantalla LCD.
    """

    def __init__(self, lcd):
        self.lcd = lcd
        self._screen_index = 0

    @property
    def screen_index(self):
        return self._screen_index

    def next_screen(
        self,
        temperature,
        humidity,
        gas_value,
        distance_cm,
        light_value,
        door_state,
        system_state,
    ):
        """
        Muestra la siguiente pantalla de información
        y avanza el índice de rotación.
        """

        screens = [
            lambda: self.lcd.show_temperature_humidity(
                temperature,
                humidity,
            ),
            lambda: self.lcd.show_gas(gas_value),
            lambda: self.lcd.show_distance(distance_cm),
            lambda: self.lcd.show_light(light_value),
            lambda: self.lcd.show_door(door_state),
            lambda: self.lcd.show_system_state(system_state),
        ]

        screens[self._screen_index]()

        self._screen_index = (
            self._screen_index + 1
        ) % len(screens)