from pathlib import Path
from typing import List

import yaml
from models.db_clients.db_client import DBClient


class YamlDBClient(DBClient):
    def __init__(self, data_path: Path):
        self.data_path = data_path

    def save(self, coll_name: str, data: dict):
        path: Path = self.data_path / coll_name / (str(data["uuid"]) + ".yaml")
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open("w") as data_file:
            yaml_data = yaml.dump(data, allow_unicode=True)
            data_file.write(yaml_data)

    def get(self, coll_name: str, uuid: str) -> dict:
        path: Path = self.data_path / coll_name / (uuid + ".yaml")

        with path.open() as data_file:
            return yaml.safe_load(data_file)

    def all(self, coll_name: str) -> List[dict]:
        path: Path = self.data_path / coll_name
        items = []

        for fname in path.glob("*.yaml"):
            with open(fname, encoding="utf-8") as data_file:
                data = yaml.safe_load(data_file)
                items.append(data)

        return items
