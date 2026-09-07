class RaspberryLCD:
    """
    Driver base para LCD 1602A en modo paralelo de 4 bits.

    Utiliza:
    - RS
    - E (Enable)
    - D4, D5, D6, D7

    El pin RW del LCD se conectará físicamente a GND.
    """

    def __init__(
        self,
        rs_pin,
        enable_pin,
        d4_pin,
        d5_pin,
        d6_pin,
        d7_pin,
        gpio_driver,
    ):
        self.rs_pin = rs_pin
        self.enable_pin = enable_pin
        self.data_pins = [
            d4_pin,
            d5_pin,
            d6_pin,
            d7_pin,
        ]

        self.gpio = gpio_driver

        self._line1 = ""
        self._line2 = ""

        self.gpio.setup_output(self.rs_pin)
        self.gpio.setup_output(self.enable_pin)

        for pin in self.data_pins:
            self.gpio.setup_output(pin)

        self._set_all_low()

    @property
    def line1(self):
        return self._line1

    @property
    def line2(self):
        return self._line2

    def _set_all_low(self):
        self.gpio.write_low(self.rs_pin)
        self.gpio.write_low(self.enable_pin)

        for pin in self.data_pins:
            self.gpio.write_low(pin)

    def show(self, line1="", line2=""):
        """
        Guarda el contenido que posteriormente
        será enviado físicamente al LCD.
        """

        self._line1 = str(line1)[:16]
        self._line2 = str(line2)[:16]

    def clear(self):
        self._line1 = ""
        self._line2 = ""