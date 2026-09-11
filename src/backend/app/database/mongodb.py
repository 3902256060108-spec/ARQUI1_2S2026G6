from pymongo import MongoClient

from src.backend.app.config.settings import settings


class MongoDB:
    def __init__(self):
        self.client = None
        self.database = None

    def connect(self):
        if not settings.MONGODB_URI:
            raise ValueError("MONGODB_URI no está configurada")

        self.client = MongoClient(settings.MONGODB_URI)
        self.database = self.client[settings.MONGODB_DATABASE]

    def close(self):
        if self.client:
            self.client.close()


mongodb = MongoDB()