from pathlib import Path
from typing import List
from typing_extensions import Self
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
import yaml
from fastapi.encoders import jsonable_encoder


class CustomModel(BaseModel):
    def validate(self):
        return True

    def yaml(self) -> str:
        return yaml.dump(self.encode())

    def encode(self) -> dict:
        return jsonable_encoder(self.dict())

    def save(self):
        path:Path = Path("/src/data") / self.__class__.__name__ / (str(self.uuid) + ".yaml")
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open("w") as fp:
            fp.write(self.yaml())

    @classmethod
    def load(cls, fp) -> Self:
        return cls(**yaml.safe_load(fp))


class Thesis(CustomModel):
    uuid: UUID = Field(default_factory=uuid4)
    title: str
    authors: List[str]
    advisors: List[str]
    keywords: List[str]

    def validate(self):
        if not self.title:
            raise ValueError("El título no puede ser vacío.")

        if len(self.authors) == 0:
            raise ValueError("Debe tener al menos un autor.")

        if len(self.advisors) == 0:
            raise ValueError("Debe tener al menos un tutor.")

        if len(self.keywords) < 3:
            raise ValueError("Debe tener al menos 3 palabras clave.")

        return True
