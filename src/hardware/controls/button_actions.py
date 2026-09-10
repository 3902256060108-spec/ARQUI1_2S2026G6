class ButtonActions:
    """
    Ejecuta las acciones correspondientes a los botones físicos.
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
        """
        Procesa los botones detectados por ButtonManager.
        """

        results = {}

        for button in pressed_buttons:

            if button == "door":
                results["door"] = (
                    self.door_control.handle_press()
                )

            elif button == "light_mode":
                results["light_mode"] = (
                    self.lighting_mode_control.handle_press()
                )

            elif button == "silence":
                self.buzzer_control.silence()
                results["silence"] = True

            elif button == "reset":
                results["reset"] = (
                    self.reset_control.reset_alert(
                        danger_active=danger_active
                    )
                )

        return results