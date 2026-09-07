class RaspberryBuzzer:
    """
    Control de buzzer activo mediante GPIO.

    No importa directamente RPi.GPIO para permitir
    pruebas desde Windows usando un GPIO falso.
    """

    def __init__(self, pin, gpio_driver):
        self.pin = pin
        self.gpio = gpio_driver
        self._is_on = False

        self.gpio.setup_output(self.pin)
        self.gpio.write_low(self.pin)

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self):
        self.gpio.write_high(self.pin)
        self._is_on = True

    def turn_off(self):
        self.gpio.write_low(self.pin)
        self._is_on = False

    def toggle(self):
        if self._is_on:
            self.turn_off()
        else:
            self.turn_on()