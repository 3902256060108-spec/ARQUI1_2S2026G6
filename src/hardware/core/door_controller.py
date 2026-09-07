import time


class DoorController:
    """
    Controlador de apertura automática de la puerta.

    La puerta se abre cuando se detecta presencia y
    permanece abierta durante un tiempo configurable
    después de la última detección.
    """

    def __init__(
        self,
        servo,
        distance_threshold,
        open_time=5,
        time_provider=None,
    ):
        self.servo = servo
        self.distance_threshold = distance_threshold
        self.open_time = open_time

        # Permite usar tiempo real en Raspberry Pi
        # y tiempo simulado durante las pruebas.
        self._time = time_provider or time.monotonic

        self._last_detection_time = None

    def update(self, distance_cm):
        """
        Actualiza el estado de la puerta según la distancia.

        Si detecta presencia:
            - abre la puerta;
            - reinicia el temporizador.

        Si deja de detectar presencia:
            - mantiene la puerta abierta hasta que
              transcurra open_time;
            - luego la cierra.
        """

        if distance_cm < 0:
            raise ValueError("La distancia no puede ser negativa.")

        current_time = self._time()

        if distance_cm <= self.distance_threshold:
            self.servo.open_door()
            self._last_detection_time = current_time

        elif self._last_detection_time is not None:
            elapsed_time = current_time - self._last_detection_time

            if elapsed_time >= self.open_time:
                self.servo.close_door()
                self._last_detection_time = None

        else:
            self.servo.close_door()

        return self.servo.door_state