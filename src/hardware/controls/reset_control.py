class ResetControl:
    """
    Controla el reinicio manual de una alerta.

    El sistema solo puede restablecerse cuando
    la condición peligrosa ya no está presente.
    """

    def __init__(self, button, buzzer_control):
        self.button = button
        self.buzzer_control = buzzer_control

    def reset_alert(self, danger_active):
        """
        Intenta restablecer la alerta.

        Retorna:
            True  -> si el reset fue aceptado.
            False -> si todavía existe peligro.
        """

        if danger_active:
            return False

        self.buzzer_control.reset_silence()

        return True