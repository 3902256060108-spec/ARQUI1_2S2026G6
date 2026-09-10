class DoorControl:
    """
    Control manual de la puerta mediante un botón físico.
    """

    def __init__(self, button, servo):
        self.button = button
        self.servo = servo

    def handle_press(self):
        """
        Alterna manualmente el estado de la puerta.
        """

        self.servo.toggle_door()

        return self.servo.door_state