from datetime import datetime


class SensorReading:
    def __init__(
        self,
        sensor: str,
        valor: float,
        timestamp: datetime
    ):
        self.sensor = sensor
        self.valor = valor
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "sensor": self.sensor,
            "valor": self.valor,
            "timestamp": self.timestamp
        }