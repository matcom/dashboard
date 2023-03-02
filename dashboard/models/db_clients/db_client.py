import abc
from typing import List


class DBClient(abc.ABC):
    @abc.abstractmethod
    def save(self, coll_name: str, data: dict):
        pass

    @abc.abstractmethod
    def get(self, coll_name: str, uuid: str) -> dict:
        pass

    @abc.abstractmethod
    def delete(self, coll_name: str, uuid: str) -> dict:
        pass

    @abc.abstractmethod
    def find(self, coll_name: str, **kwargs) -> List[dict]:
        pass

    @abc.abstractmethod
    def find_one(self, coll_name: str, **kwargs) -> dict:
        pass

    @abc.abstractmethod
    def all(self, coll_name: str) -> List[dict]:
        pass

    @abc.abstractmethod
    def stats(self, coll_name: str) -> dict:
        pass
