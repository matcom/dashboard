from typing import List

from models.db_clients.db_client import DBClient


class CombinedDBClient(DBClient):
    def __init__(self, clients: List[DBClient], use: int = 0):
        if not clients:
            raise ValueError("There must be at least one client.")
        if not 0 <= use < len(clients):
            raise ValueError(f"Invalid client index ({use}) to use.")

        self.clients = clients
        self.use = use

    @property
    def client_in_use(self):
        return self.clients[self.use]

    def save(self, coll_name: str, data: dict):
        for client in self.clients:
            client.save(coll_name, data)

    def get(self, coll_name: str, uuid: str) -> dict:
        return self.client_in_use.get(coll_name, uuid)

    def delete(self, coll_name: str, uuid: str):
        self.client_in_use.delete(coll_name, uuid)

    def find(self, coll_name: str, **kwargs) -> List[dict]:
        return self.client_in_use.find(coll_name, **kwargs)

    def find_one(self, coll_name: str, **kwargs) -> dict:
        return self.client_in_use.find_one(coll_name, **kwargs)

    def all(self, coll_name: str) -> List[dict]:
        return self.client_in_use.all(coll_name)

    def stats(self, coll_name: str) -> dict:
        return self.client_in_use.stats(coll_name)
