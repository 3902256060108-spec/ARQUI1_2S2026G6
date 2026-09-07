from src.hardware.core.system_state import (
    SystemState,
    determine_system_state,
)


class SystemController:
    """
    Controlador central del sistema.

    Recibe las lecturas de sensores y actualiza
    los actuadores según el estado global.
    """

    def __init__(
        self,
        normal_led,
        warning_led,
        emergency_led,
        buzzer,
        servo,
        fan,
        temp_max,
        humidity_min,
        humidity_max,
    ):
        self.normal_led = normal_led
        self.warning_led = warning_led
        self.emergency_led = emergency_led
        self.buzzer = buzzer
        self.servo = servo
        self.fan = fan

        self.temp_max = temp_max
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max

        self.state = SystemState.NORMAL

    def update_state(self, temperature, humidity, gas_alert):
        """
        Calcula y aplica el estado global del sistema.
        """

        self.state = determine_system_state(
            temperature=temperature,
            humidity=humidity,
            gas_alert=gas_alert,
            temp_max=self.temp_max,
            humidity_min=self.humidity_min,
            humidity_max=self.humidity_max,
        )

        self._apply_state()

        return self.state

    def _turn_off_state_leds(self):
        self.normal_led.turn_off()
        self.warning_led.turn_off()
        self.emergency_led.turn_off()

    def _apply_state(self):
        """
        Actualiza los actuadores según el estado actual.
        """

        self._turn_off_state_leds()

        if self.state == SystemState.NORMAL:
            self.normal_led.turn_on()
            self.buzzer.turn_off()
            self.fan.turn_off()

        elif self.state == SystemState.WARNING:
            self.warning_led.turn_on()
            self.buzzer.turn_off()
            self.fan.turn_on()

        elif self.state == SystemState.EMERGENCY:
            self.emergency_led.turn_on()
            self.buzzer.turn_on()
            self.fan.turn_on()
            self.servo.open_door()