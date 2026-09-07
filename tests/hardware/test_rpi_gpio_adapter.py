import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.rpi_gpio_adapter import (
    load_rpi_gpio,
)


def test_windows_without_rpi_gpio_gives_clear_error():
    try:
        gpio = load_rpi_gpio()
    except RuntimeError as error:
        assert "RPi.GPIO no está disponible" in str(error)
        return

    # Si algún día esta prueba se ejecuta realmente
    # en Raspberry Pi, RPi.GPIO sí puede existir.
    assert gpio is not None