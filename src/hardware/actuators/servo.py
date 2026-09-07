from enum import Enum


class DoorState(Enum):
    CLOSED = "CERRADA"
    OPEN = "ABIERTA"


class Servo:
    """
    Abstracción del servomotor encargado de controlar
    la puerta del sistema.

    El movimiento físico mediante GPIO/PWM se
    implementará cuando se ejecute en Raspberry Pi.
    """

    def __init__(self, pin):
        self.pin = pin
        self._door_state = DoorState.CLOSED

    @property
    def door_state(self):
        return self._door_state

    @property
    def is_open(self):
        return self._door_state == DoorState.OPEN

    def open_door(self):
        """
        Cambia el estado lógico de la puerta a abierta.
        """
        self._door_state = DoorState.OPEN

    def close_door(self):
        """
        Cambia el estado lógico de la puerta a cerrada.
        """
        self._door_state = DoorState.CLOSED

    def toggle_door(self):
        """
        Alterna entre puerta abierta y cerrada.
        """
        if self.is_open:
            self.close_door()
        else:
            self.open_door()