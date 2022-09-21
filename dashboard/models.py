from __future__ import annotations

from pathlib import Path
from typing import List
from uuid import UUID, uuid4

import yaml
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing_extensions import Self


class CustomModel(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)

    def check(self):
        return True

    def yaml(self) -> str:
        return yaml.dump(self.encode(), allow_unicode=True)

    def encode(self) -> dict:
        data = jsonable_encoder(self.dict())
        result = {}

        for key, value in data.items():
            if isinstance(value, dict) and 'uuid' in value:
                result[key] = value['uuid']
            else:
                result[key] = value

        return result

    def _encode(self, v):
        if isinstance(v, (int, float, str)):
            return v
        if isinstance(v, list):
            return [self._encode(vi) for vi in v]
        if isinstance(v, dict):
            return { ki: self._encode(vi) for ki,vi in v.items() }

        return str(v)

    def save(self):
        path:Path = Path("/src/data") / self.__class__.__name__ / (str(self.uuid) + ".yaml")
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open("w") as fp:
            fp.write(self.yaml())

    @classmethod
    def all(cls) -> List[Self]:
        path:Path = Path("/src/data") / cls.__name__
        items = []

        for fname in path.glob("*.yaml"):
            with open(fname) as fp:
                items.append(cls.load(fp))

        return items

    @classmethod
    def get(cls, uuid:str) -> Self:
        path:Path = Path("/src/data") / cls.__name__ / (str(uuid) + ".yaml")

        with path.open() as fp:
            return cls.load(fp)

    @classmethod
    def load(cls, fp) -> Self:
        data = yaml.safe_load(fp)
        values = {}

        for key,value in data.items():
            field = cls.__fields__[key]

            if issubclass(field.type_, CustomModel):
                value = field.type_.get(value)

            values[key] = value

        return cls(**values)


class Thesis(CustomModel):
    title: str
    authors: List[str]
    advisors: List[str]
    keywords: List[str]

    def check(self):
        if not self.title:
            raise ValueError("El título no puede ser vacío.")

        if len(self.authors) == 0:
            raise ValueError("Debe tener al menos un autor.")

        if len(self.advisors) == 0:
            raise ValueError("Debe tener al menos un tutor.")

        if len(self.keywords) < 3:
            raise ValueError("Debe tener al menos 3 palabras clave.")

        return True


class Subject(CustomModel):
    subject: str
    career: str
    semester: int
    year: int

    def __str__(self) -> str:
        return self.subject


class Person(CustomModel):
    name: str
    institution: str
    faculty: str = None
    department: str = None

    def __str__(self) -> str:
        return self.name


class Classes(CustomModel):
    subject: Subject
    professor: Person
    lecture_hours: int
    practice_hours: int
