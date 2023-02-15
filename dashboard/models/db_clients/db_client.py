import abc
from typing import List
from uuid import UUID


class DBClient(abc.ABC):
    @abc.abstractmethod
    def save(self, coll_name: str, data: dict):
        pass

    @abc.abstractmethod
    def get(self, coll_name: str, uuid: str) -> dict:
        pass

    @abc.abstractmethod
    def all(self, coll_name: str) -> List[dict]:
        pass
