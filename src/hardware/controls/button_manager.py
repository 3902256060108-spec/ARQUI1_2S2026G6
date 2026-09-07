class ButtonManager:
    """
    Detecta nuevas pulsaciones de los botones.

    Una acción se genera solamente cuando el botón
    cambia de NO presionado a presionado.
    """

    def __init__(
        self,
        door_button,
        light_mode_button,
        silence_button,
        reset_button,
    ):
        self.buttons = {
            "door": door_button,
            "light_mode": light_mode_button,
            "silence": silence_button,
            "reset": reset_button,
        }

        self._previous_states = {
            name: False
            for name in self.buttons
        }

    def _read_button(self, button):
        """
        Permite trabajar tanto con el driver físico,
        donde is_pressed es una propiedad, como con
        botones simulados usados en las pruebas.
        """

        value = button.is_pressed

        if callable(value):
            value = value()

        return bool(value)

    def read_pressed(self):
        """
        Retorna los botones que acaban de ser presionados.
        """

        pressed = []

        for name, button in self.buttons.items():
            current = self._read_button(button)

            if current and not self._previous_states[name]:
                pressed.append(name)

            self._previous_states[name] = current

        return pressed