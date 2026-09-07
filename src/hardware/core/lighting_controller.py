from enum import Enum


class LightingMode(Enum):
    AUTOMATIC = "AUTOMATICO"
    MANUAL = "MANUAL"


class LightingController:
    """
    Controlador del sistema de iluminación.

    En modo AUTOMATICO:
        - La iluminación depende del valor del sensor LDR.

    En modo MANUAL:
        - El usuario controla directamente las luces.
    """

    def __init__(
        self,
        lights,
        light_threshold,
        mode=LightingMode.AUTOMATIC,
    ):
        self.lights = lights
        self.light_threshold = light_threshold
        self.mode = mode

    def toggle_mode(self):
        """
        Alterna entre modo AUTOMATICO y MANUAL.
        """
        if self.mode == LightingMode.AUTOMATIC:
            self.mode = LightingMode.MANUAL
        else:
            self.mode = LightingMode.AUTOMATIC

        return self.mode

    def set_manual_state(self, turn_on):
        """
        En modo manual, enciende o apaga todas las luces.
        """

        if self.mode != LightingMode.MANUAL:
            raise RuntimeError(
                "El control manual solo está disponible en modo MANUAL."
            )

        if turn_on:
            self._turn_on_lights()
        else:
            self._turn_off_lights()

    def update_automatic(self, light_value):
        """
        Actualiza las luces según la lectura del LDR.

        Solo actúa cuando el sistema está en modo AUTOMATICO.
        """

        if self.mode != LightingMode.AUTOMATIC:
            return

        if self.light_threshold is None:
            raise ValueError(
                "El umbral de iluminación no está configurado."
            )

        if light_value < 0:
            raise ValueError(
                "La lectura de iluminación no puede ser negativa."
            )

        if light_value < self.light_threshold:
            self._turn_on_lights()
        else:
            self._turn_off_lights()

    def _turn_on_lights(self):
        for light in self.lights:
            light.turn_on()

    def _turn_off_lights(self):
        for light in self.lights:
            light.turn_off()

    def update_automatic_digital(self, is_dark):
        """
        Actualiza la iluminación automática usando
        directamente la salida digital del sensor LDR.

        is_dark:
            True  -> oscuridad detectada
            False -> suficiente iluminación
        """

        if self.mode != LightingMode.AUTOMATIC:
            return

        if not isinstance(is_dark, bool):
            raise TypeError(
                "is_dark debe ser un valor booleano."
            )

        if is_dark:
            self._turn_on_lights()
        else:
            self._turn_off_lights()