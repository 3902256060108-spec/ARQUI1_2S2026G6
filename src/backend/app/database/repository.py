from datetime import datetime, timezone

from src.backend.app.database.mongodb import mongodb


class Repository:
    def _collection(self, name: str):
        if mongodb.database is None:
            raise RuntimeError("MongoDB no está conectado")

        return mongodb.database[name]

    def insert_sensor_reading(
        self,
        sensor: str,
        valor: float
    ):
        document = {
            "sensor": sensor,
            "valor": valor,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("sensor_readings").insert_one(document)

    def insert_event(
        self,
        tipo: str,
        estado: str,
        descripcion: str
    ):
        document = {
            "tipo": tipo,
            "estado": estado,
            "descripcion": descripcion,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("events").insert_one(document)

    def insert_command(
        self,
        dispositivo: str,
        accion: str,
        origen: str = "dashboard"
    ):
        document = {
            "dispositivo": dispositivo,
            "accion": accion,
            "origen": origen,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("commands").insert_one(document)

    def insert_arm64_result(
        self,
        max_value: float,
        min_value: float,
        avg: float,
        count: int
    ):
        document = {
            "max": max_value,
            "min": min_value,
            "avg": avg,
            "count": count,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("arm64_results").insert_one(document)

    def insert_system_status(
        self,
        estado: str
    ):
        document = {
            "estado": estado,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("system_status").insert_one(document)


repository = Repository()