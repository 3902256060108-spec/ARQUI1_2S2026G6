class LCDDisplay:
    """
    Abstracción de la pantalla LCD del sistema.

    Permite preparar los mensajes que posteriormente
    serán enviados al LCD físico de la Raspberry Pi.
    """

    def __init__(self, columns=16, rows=2):
        self.columns = columns
        self.rows = rows
        self._line1 = ""
        self._line2 = ""

    @property
    def line1(self):
        return self._line1

    @property
    def line2(self):
        return self._line2

    def show(self, line1="", line2=""):
        """
        Guarda el contenido que debe mostrarse en pantalla.
        """
        self._line1 = str(line1)[:self.columns]
        self._line2 = str(line2)[:self.columns]

    def clear(self):
        """
        Limpia el contenido lógico de la pantalla.
        """
        self._line1 = ""
        self._line2 = ""

    def show_temperature_humidity(self, temperature, humidity):
        temperature_text = (
            f"{temperature:.1f}C"
            if temperature is not None
            else "N/A"
        )

        humidity_text = (
            f"{humidity:.1f}%"
            if humidity is not None
            else "N/A"
        )

        self.show(
            f"Temp: {temperature_text}",
            f"Humedad: {humidity_text}",
        )

    def show_gas(self, value):
        self.show(
            "Gas/Humo:",
            str(value)
        )

    def show_distance(self, distance_cm):
        distance_text = (
            f"{distance_cm:.1f} cm"
            if distance_cm is not None
            else "N/A"
        )

        self.show(
            "Distancia:",
            distance_text,
        )

    def show_light(self, value):
        self.show(
            "Luz:",
            str(value)
        )

    def show_door(self, state):
        self.show(
            "Puerta:",
            str(state)
        )

    def show_system_state(self, state):
        self.show(
            "Estado:",
            str(state)
        )