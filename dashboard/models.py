from __future__ import annotations

from pathlib import Path
from typing import List
from uuid import UUID, uuid4

import yaml
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, HttpUrl, EmailStr
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
            if isinstance(value, dict) and "uuid" in value:
                result[key] = value["uuid"]
            elif isinstance(value, list) and all(
                [isinstance(v, dict) and "uuid" in v for v in value]
            ):
                result[key] = [v["uuid"] for v in value]
            elif isinstance(value, HttpUrl):
                result[key] = str(value)
            else:
                result[key] = value

        return result

    def _encode(self, v):
        if isinstance(v, (int, float, str)):
            return v
        if isinstance(v, list):
            return [self._encode(vi) for vi in v]
        if isinstance(v, dict):
            return {ki: self._encode(vi) for ki, vi in v.items()}

        return str(v)

    def save(self):
        path: Path = (
            Path("/src/data") / self.__class__.__name__ / (str(self.uuid) + ".yaml")
        )
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open("w") as fp:
            fp.write(self.yaml())

    @classmethod
    def all(cls) -> List[Self]:
        path: Path = Path("/src/data") / cls.__name__
        items = []

        for fname in path.glob("*.yaml"):
            with open(fname) as fp:
                items.append(cls.load(fp))

        return items

    @classmethod
    def get(cls, uuid: str) -> Self:
        path: Path = Path("/src/data") / cls.__name__ / (str(uuid) + ".yaml")

        with path.open() as fp:
            return cls.load(fp)

    @classmethod
    def load(cls, fp) -> Self:
        data = yaml.safe_load(fp)
        values = {}

        for key, value in data.items():
            field = cls.__fields__[key]

            if issubclass(field.type_, CustomModel):
                if isinstance(value, list):
                    value = [field.type_.get(v) for v in value]
                else:
                    value = field.type_.get(value)

            values[key] = value

        return cls(**values)

    def __hash__(self):
        return hash(str(self.uuid))

    def __eq__(self, other):
        return isinstance(other, CustomModel) and self.uuid == other.uuid


class Thesis(CustomModel):
    title: str
    authors: List[str]
    advisors: List[str]
    keywords: List[str]
    version: int = 0
    balance: int = 2022

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

    def save_thesis_pdf(self, pdf):
        self.version += 1
        name_pdf = f"{self.uuid}_v{self.version}.pdf"
        path: Path = Path(f"/src/data/Thesis/files/{name_pdf}")
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open("wb") as f:
            f.write(pdf.getbuffer())


class Subject(CustomModel):
    subject: str
    career: str
    semester: int
    year: int

    def __str__(self) -> str:
        return self.subject


class Person(CustomModel):
    name: str
    institution: str = None
    faculty: str = None
    department: str = None
    scientific_grade: str = "Licenciado"
    academic_grade: str = "Ninguno"
    orcid: str = None
    emails: List[str] = Field(default_factory=list)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def own(cls):
        return [
            p
            for p in cls.all()
            if p.institution == "Universidad de La Habana"
            and p.faculty == "Matemática y Computación"
        ]


class Classes(CustomModel):
    subject: Subject
    professor: Person
    lecture_hours: int
    practice_hours: int

    def save(self):
        func_check_same_data = (
            lambda c: self.subject == c.subject and self.professor == c.professor
        )
        class_with_same_data = next(filter(func_check_same_data, Classes.all()), None)
        if class_with_same_data:
            self.uuid = class_with_same_data.uuid
        CustomModel.save(self)


class Journal(CustomModel):
    title: str
    publisher: str
    issn: str = ""

    def save(self):
        func_check_same_data = (
            lambda c: self.title == c.title and self.publisher == c.publisher
        )
        class_with_same_data = next(filter(func_check_same_data, Journal.all()), None)
        if class_with_same_data:
            self.uuid = class_with_same_data.uuid
        CustomModel.save(self)

    def __str__(self):
        return f"{self.title} ({self.publisher})"


class JournalPaper(CustomModel):
    title: str
    authors: List[Person]
    corresponding_author: Person = None
    url: HttpUrl = None
    journal: Journal = None
    issue: int = 1
    year: int = 2022
    balance: int = 2022


class ConferencePresentation(CustomModel):
    title: str
    authors: List[Person]
    url: HttpUrl = None
    venue: str = None
    location: str = None
    year: int = 2022
    paper: bool = False
    balance: int = 2022


class Book(CustomModel):
    title: str
    publisher: str
    authors: List[Person]
    pages: int = None
    url: HttpUrl = None
    isbn: str = None
    edition: int = 1
    year: int = 2022


class BookChapter(Book):
    chapter: str
