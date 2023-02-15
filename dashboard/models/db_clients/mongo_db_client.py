from typing import List

import pymongo
from models.db_clients.db_client import DBClient

MAIN_DB_NAME = "dashboardDB"


class MongoDBClient(DBClient):
    def __init__(self, user: str, password: str):
        self.mongo_client = pymongo.MongoClient(
            f"mongodb://{user}:{password}@mongo:27017/"
        )
        self.main_db = self.mongo_client[MAIN_DB_NAME]

    def save(self, coll_name: str, data: dict):
        coll = self.main_db[coll_name]
        coll.update_one({"uuid": data["uuid"]}, data, upsert=True)

    def get(self, coll_name: str, uuid: str) -> dict:
        coll = self.main_db[coll_name]
        data = coll.find_one({"uuid": uuid})
        if data is None:
            raise Exception(f"Entry {uuid} not found in {coll_name}")
        return data

    def find(self, coll_name: str, **kwargs) -> List[dict]:
        coll = self.main_db[coll_name]
        return list(coll.find(**kwargs))

    def find_one(self, coll_name: str, **kwargs) -> dict:
        coll = self.main_db[coll_name]
        data = coll.find_one(**kwargs)
        if data is None:
            raise KeyError(str(kwargs))
        return data

    def all(self, coll_name: str) -> List[dict]:
        coll = self.main_db[coll_name]
        return list(coll.find())
