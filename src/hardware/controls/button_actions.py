class ButtonActions:
    """
    Ejecuta las acciones asociadas a los
    cuatro botones físicos del sistema.
    """

    def __init__(
        self,
        door_control,
        lighting_mode_control,
        buzzer_control,
        reset_control,
    ):
        self.door_control = door_control
        self.lighting_mode_control = lighting_mode_control
        self.buzzer_control = buzzer_control
        self.reset_control = reset_control

    def process(self, pressed_buttons, danger_active=False):
        for button in pressed_buttons:

            if button == "door":
                self.door_control.toggle_door()

            elif button == "light_mode":
                self.lighting_mode_control.toggle_mode()

            elif button == "silence":
                self.buzzer_control.silence()

            elif button == "reset":
                self.reset_control.reset(
                    danger_active=danger_active
                )