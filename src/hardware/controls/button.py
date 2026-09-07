class Button:
    """
    Abstracción de un botón físico conectado a la Raspberry Pi.

    La lectura real mediante GPIO se implementará
    cuando se ejecute en la Raspberry Pi.
    """

    def __init__(self, pin, name="BUTTON"):
        self.pin = pin
        self.name = name
        self._pressed = False

    @property
    def is_pressed(self):
        return self._pressed

    def press(self):
        """
        Simula que el botón ha sido presionado.
        """
        self._pressed = True

    def release(self):
        """
        Simula que el botón ha sido liberado.
        """
        self._pressed = False

    def read(self):
        """
        Lee físicamente el botón.

        Se implementará cuando se ejecute
        en Raspberry Pi.
        """
        raise NotImplementedError(
            "La lectura real del botón debe ejecutarse en la Raspberry Pi."
        )