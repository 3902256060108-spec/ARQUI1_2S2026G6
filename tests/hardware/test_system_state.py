import sys
from pathlib import Path

# Permite importar los módulos ubicados en src/
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.core.system_state import (
    SystemState,
    determine_system_state
)


TEMP_MAX = 30.0
HUMIDITY_MIN = 30.0
HUMIDITY_MAX = 70.0


def test_normal_state():
    state = determine_system_state(
        temperature=25.0,
        humidity=50.0,
        gas_alert=False,
        temp_max=TEMP_MAX,
        humidity_min=HUMIDITY_MIN,
        humidity_max=HUMIDITY_MAX
    )

    assert state == SystemState.NORMAL


def test_warning_temperature():
    state = determine_system_state(
        temperature=35.0,
        humidity=50.0,
        gas_alert=False,
        temp_max=TEMP_MAX,
        humidity_min=HUMIDITY_MIN,
        humidity_max=HUMIDITY_MAX
    )

    assert state == SystemState.WARNING


def test_emergency_gas():
    state = determine_system_state(
        temperature=25.0,
        humidity=50.0,
        gas_alert=True,
        temp_max=TEMP_MAX,
        humidity_min=HUMIDITY_MIN,
        humidity_max=HUMIDITY_MAX
    )

    assert state == SystemState.EMERGENCY