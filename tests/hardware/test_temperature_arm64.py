import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pytest

from src.hardware.integration.temperature_arm64 import (
    TemperatureARM64,
)


class FakeDHT:
    def __init__(self):
        self.value = 20

    def read(self):
        temperature = self.value
        self.value += 1

        return {
            "temperature": temperature,
            "humidity": 50,
        }


class FakeRunner:
    def __init__(self):
        self.received = None
        self.executed = False
        self.results_read = False

    def generar_datos(self, temperatures):
        self.received = temperatures

    def ejecutar_arm64(self):
        self.executed = True

    def leer_resultados(self):
        self.results_read = True

        return {
            "MAX": 39,
            "MIN": 20,
            "AVG": 29,
            "COUNT": 20,
        }


def test_requires_at_least_twenty_samples():
    with pytest.raises(
        ValueError,
        match="20",
    ):
        TemperatureARM64(
            dht_sensor=FakeDHT(),
            sample_count=19,
            runner=FakeRunner(),
        )


def test_collects_twenty_temperatures():
    integration = TemperatureARM64(
        dht_sensor=FakeDHT(),
        sample_count=20,
        runner=FakeRunner(),
    )

    temperatures = integration.collect_temperatures()

    assert len(temperatures) == 20
    assert temperatures[0] == 20
    assert temperatures[-1] == 39


def test_converts_temperature_to_integer():
    class DecimalDHT:
        def read(self):
            return {
                "temperature": 25.8,
                "humidity": 50,
            }

    integration = TemperatureARM64(
        dht_sensor=DecimalDHT(),
        sample_count=20,
        runner=FakeRunner(),
    )

    temperatures = integration.collect_temperatures()

    assert all(
        isinstance(value, int)
        for value in temperatures
    )


def test_process_sends_temperatures_to_arm64():
    runner = FakeRunner()

    integration = TemperatureARM64(
        dht_sensor=FakeDHT(),
        sample_count=20,
        runner=runner,
    )

    output = integration.process()

    assert runner.executed is True
    assert runner.results_read is True

    assert runner.received == output["temperatures"]

    assert output["results"] == {
        "MAX": 39,
        "MIN": 20,
        "AVG": 29,
        "COUNT": 20,
    }

def test_retries_when_dht_read_fails():
    class FlakyDHT:
        def __init__(self):
            self.calls = 0

        def read(self):
            self.calls += 1

            if self.calls <= 3:
                raise RuntimeError(
                    "Lectura DHT fallida"
                )

            return {
                "temperature": 25,
                "humidity": 50,
            }

    sensor = FlakyDHT()

    integration = TemperatureARM64(
        dht_sensor=sensor,
        sample_count=20,
        runner=FakeRunner(),
    )

    temperatures = integration.collect_temperatures()

    assert len(temperatures) == 20
    assert sensor.calls == 23


def test_ignores_none_temperature():
    class NoneDHT:
        def __init__(self):
            self.calls = 0

        def read(self):
            self.calls += 1

            if self.calls == 1:
                return {
                    "temperature": None,
                    "humidity": 50,
                }

            return {
                "temperature": 25,
                "humidity": 50,
            }

    sensor = NoneDHT()

    integration = TemperatureARM64(
        dht_sensor=sensor,
        sample_count=20,
        runner=FakeRunner(),
    )

    temperatures = integration.collect_temperatures()

    assert len(temperatures) == 20
    assert sensor.calls == 21

def test_add_temperature_accumulates_samples():
    integration = TemperatureARM64(
        dht_sensor=FakeDHT(),
        sample_count=20,
        runner=FakeRunner(),
    )

    for temperature in range(20, 39):
        ready = integration.add_temperature(
            temperature
        )

        assert ready is False

    ready = integration.add_temperature(39)

    assert ready is True
    assert integration.is_ready() is True
    assert len(integration.temperatures) == 20


def test_process_collected_waits_for_twenty_samples():
    integration = TemperatureARM64(
        dht_sensor=FakeDHT(),
        sample_count=20,
        runner=FakeRunner(),
    )

    for _ in range(19):
        integration.add_temperature(25)

    result = integration.process_collected()

    assert result is None


def test_process_collected_sends_samples_and_clears_buffer():
    runner = FakeRunner()

    integration = TemperatureARM64(
        dht_sensor=FakeDHT(),
        sample_count=20,
        runner=runner,
    )

    for temperature in range(20, 40):
        integration.add_temperature(
            temperature
        )

    result = integration.process_collected()

    assert runner.executed is True
    assert runner.results_read is True
    assert len(runner.received) == 20

    assert result["temperatures"] == runner.received

    assert result["results"] == {
        "MAX": 39,
        "MIN": 20,
        "AVG": 29,
        "COUNT": 20,
    }

    assert integration.temperatures == []