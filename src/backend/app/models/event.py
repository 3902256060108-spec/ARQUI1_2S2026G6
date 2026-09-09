from datetime import datetime


class Event:
    def __init__(
        self,
        tipo: str,
        estado: str,
        descripcion: str,
        timestamp: datetime
    ):
        self.tipo = tipo
        self.estado = estado
        self.descripcion = descripcion
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "estado": self.estado,
            "descripcion": self.descripcion,
            "timestamp": self.timestamp
        }