from datetime import datetime


class Command:
    def __init__(
        self,
        dispositivo: str,
        accion: str,
        origen: str,
        timestamp: datetime
    ):
        self.dispositivo = dispositivo
        self.accion = accion
        self.origen = origen
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "dispositivo": self.dispositivo,
            "accion": self.accion,
            "origen": self.origen,
            "timestamp": self.timestamp
        }