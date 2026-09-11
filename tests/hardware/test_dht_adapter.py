import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import builtins
import pytest

from src.hardware.drivers.raspberry_pi.dht_adapter import (
    load_dht_modules,
)


def test_load_dht_modules_raises_error_when_library_missing(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name in ("board", "adafruit_dht"):
            raise ImportError("Librería simulada como ausente.")

        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(
        builtins,
        "__import__",
        fake_import,
    )

    with pytest.raises(
        RuntimeError,
        match="DHT11",
    ):
        load_dht_modules()