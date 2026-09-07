class RaspberryButton:
    """
    Botón conectado a un GPIO de Raspberry Pi.

    La lectura física se realiza mediante GPIODriver,
    permitiendo usar un GPIO falso durante las pruebas.
    """

    def __init__(self, pin, gpio_driver):
        self.pin = pin
        self.gpio = gpio_driver

        self.gpio.setup_input(self.pin)

    @property
    def is_pressed(self):
        return self.gpio.read(self.pin) == self.gpio.HIGH

    def read(self):
        return self.is_pressed