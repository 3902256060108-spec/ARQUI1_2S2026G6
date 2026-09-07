import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.controls.button import Button


def test_button_configuration():
    button = Button(
        pin=5,
        name="DOOR"
    )

    assert button.pin == 5
    assert button.name == "DOOR"
    assert button.is_pressed is False


def test_button_press():
    button = Button(pin=5)

    button.press()

    assert button.is_pressed is True


def test_button_release():
    button = Button(pin=5)

    button.press()
    button.release()

    assert button.is_pressed is False


def test_button_read_requires_raspberry():
    button = Button(pin=5)

    try:
        button.read()
        assert False, "Se esperaba NotImplementedError"
    except NotImplementedError:
        assert True