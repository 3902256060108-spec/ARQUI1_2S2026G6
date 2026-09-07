class LED:
    """
    Abstracción de un LED conectado a la Raspberry Pi.

    La activación física mediante GPIO se implementará
    cuando se ejecute en la Raspberry Pi.
    """

    def __init__(self, pin, name="LED"):
        self.pin = pin
        self.name = name
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self):
        """
        Cambia el estado lógico del LED a encendido.
        """
        self._is_on = True

    def turn_off(self):
        """
        Cambia el estado lógico del LED a apagado.
        """
        self._is_on = False

    def toggle(self):
        """
        Invierte el estado actual del LED.
        """
        self._is_on = not self._is_on