class RaspberryLightSensor:
    """
    Driver para módulo LDR usando la salida digital DO.

    La sensibilidad física se ajustará con el
    potenciómetro del módulo.
    """

    def __init__(self, pin, gpio_driver, active_low=True):
        self.pin = pin
        self.gpio = gpio_driver
        self.active_low = active_low

        self.gpio.setup_input(self.pin)

    def read(self):
        """
        Retorna True cuando se detecta oscuridad
        y False cuando hay suficiente luz.
        """

        value = self.gpio.read(self.pin)

        if self.active_low:
            return value == self.gpio.LOW

        return value == self.gpio.HIGH

    def is_dark(self):
        return self.read()