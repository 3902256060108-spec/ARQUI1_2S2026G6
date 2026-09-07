class LightingModeControl:
    """
    Controla el cambio de modo de iluminación
    mediante un botón físico.
    """

    def __init__(self, button, lighting_controller):
        self.button = button
        self.lighting_controller = lighting_controller

    def handle_press(self):
        """
        Cambia entre AUTOMATICO y MANUAL
        cuando el botón es presionado.
        """

        self.button.press()

        mode = self.lighting_controller.toggle_mode()

        self.button.release()

        return mode