class BuzzerControl:
    """
    Controla el silenciamiento manual del buzzer.

    Silenciar el buzzer no modifica el estado global
    del sistema.
    """

    def __init__(self, button, buzzer):
        self.button = button
        self.buzzer = buzzer
        self._silenced = False

    @property
    def is_silenced(self):
        return self._silenced

    def silence(self):
        """
        Silencia el buzzer.
        """
        self.button.press()

        self._silenced = True
        self.buzzer.turn_off()

        self.button.release()

    def reset_silence(self):
        """
        Permite que el buzzer pueda volver a activarse.
        """
        self._silenced = False

    def activate_alarm(self):
        """
        Activa el buzzer solamente si no ha sido silenciado.
        """
        if not self._silenced:
            self.buzzer.turn_on()