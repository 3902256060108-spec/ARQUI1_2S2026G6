class Buzzer:
    """
    Abstracción de un buzzer conectado a la Raspberry Pi.

    La activación física por GPIO se implementará
    cuando se ejecute en la Raspberry Pi.
    """

    def __init__(self, pin):
        self.pin = pin
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self):
        self._is_on = True

    def turn_off(self):
        self._is_on = False

    def toggle(self):
        self._is_on = not self._is_on