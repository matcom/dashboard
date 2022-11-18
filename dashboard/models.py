from __future__ import annotations

from pathlib import Path
from typing import List
from uuid import UUID, uuid4
from datetime import timedelta, datetime as Datetime

import yaml
import streamlit as st
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
    def find(cls, **kwargs):
        for item in cls.all():
            if all(getattr(item,k,None) == v for k,v in kwargs.items()):
                return item

        raise KeyError(str(kwargs))

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

    def format(self):
        try:
            name = self.name.split()

            if len(name) > 2:
                last_names = f"{name[-2]}-{name[-1]}"
                names = ".".join([n[0] for n in name[:-2]])
            else:
                last_names = name[-1]
                names = ".".join([n[0] for n in name[:-1]])

            fmt = f"{last_names} {names}"
        except:
            fmt = self.name

        if self.institution == "Universidad de La Habana":
            fmt = f"**{fmt} ({self.faculty})**"

        if self.orcid:
            fmt = f"{fmt} [↩️](https://orcid.org/{self.orcid})"

        return fmt

    @classmethod
    def own(cls):
        return [
            p
            for p in cls.all()
            if p.institution == "Universidad de La Habana"
            and p.faculty == "MatCom"
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
    indices: List[str] = Field(default_factory=list)
    url: HttpUrl = None

    def save(self):
        func_check_same_data = (
            lambda c: self.title == c.title and self.publisher == c.publisher
        )
        class_with_same_data = next(filter(func_check_same_data, Journal.all()), None)
        if class_with_same_data:
            self.uuid = class_with_same_data.uuid
        CustomModel.save(self)

    def format(self):
        indices = ", ".join(f"_{index}_" for index in self.indices)
        title = f"**{self.title}**"

        if self.url:
            title = f"[{title}]({self.url})"

        return f"🗞️ {title}, {self.publisher}. ISSN: {self.issn}. Indexado en: {indices}."

    def __str__(self):
        return f"{self.title} ({self.publisher})"


class Publication(CustomModel):
    authors: List[Person]

    @classmethod
    def from_authors(cls, authors: List[Person]):
        authors = set(authors)

        for item in cls.all():
            if set(item.authors) & authors:
                yield item


class JournalPaper(Publication):
    title: str
    corresponding_author: Person = None
    url: HttpUrl = None
    journal: Journal = None
    issue: int = 1
    volume: int = 1
    year: int = 2022
    balance: int = 2022

    def format(self):
        text = [f"📃 {self.title}."]

        for author in self.authors:
            text.append(author.format() + ", ")

        text.append(
            f"En _{self.journal.title}_, {self.journal.publisher}. ISSN: {self.journal.issn}."
        )
        text.append(f"Volumen {self.volume}, Número {self.issue}, {self.year}.")
        return " ".join(text)


class ConferencePresentation(Publication):
    title: str
    url: HttpUrl = None
    venue: str = None

    location: str = None
    year: int = 2022
    paper: bool = False
    balance: int = 2022
    event_type: str = "Internacional"

    def format(self):
        if self.paper:
            text = ["📃"]
        else:
            text = ["📢"]

        text.append(f"_{self.title}_.")

        for author in self.authors:
            text.append(author.format() + ", ")

        text.append(
            f"En _{self.venue}_, {self.location}, {self.year}"
        )

        return " ".join(text)


class Book(Publication):
    title: str
    publisher: str
    pages: int = None
    url: HttpUrl = None
    isbn: str = None
    edition: int = 1
    year: int = 2022

    def format(self):
        text = [f"📕 {self.title}."]

        for author in self.authors:
            text.append(author.format() + ", ")

        text.append(
            f"{self.publisher}, ISBN: {self.isbn}, Edición: {self.edition}, Páginas: {self.pages}."
        )

        return " ".join(text)


class BookChapter(Book):
    chapter: str

    def format(self):
        text = [f"📑 _{self.chapter}_."]

        for author in self.authors:
            text.append(author.format() + ", ")

        text.append(
            f"**Capítulo en el libro:** {self.title}, {self.publisher}, ISBN: {self.isbn}, Edición: {self.edition}, Páginas: {self.pages}."
        )

        return " ".join(text)


class ResearchGroup(CustomModel):
    name: str
    head: Person = None
    members: List[Person]
    collaborators: List[Person]
    keywords: List[str]


class Project(CustomModel):
    code: str = ""
    title: str
    project_type: str
    program: str = ""
    head: Person
    members: List[Person]
    main_entity: str
    entities: List[str]
    funding: List[str]
    funds_total: int = 0
    funds_collected: int = 0
    aproved: bool = False
    aproval_date: date = None
    start_date: date = None
    end_date: date = None
    status: str = "Normal"

    @classmethod
    def from_members(cls, people:List[Person]):
        people = set(people)

        for project in cls.all():
            if set(project.members) & people:
                yield project


    def format(self):
        lines = [f"⚗️ _{self.title}_"]

        if self.code:
            lines.append(f"[{self.code}]")

        lines.append(f"Proyecto {self.project_type}")

        if self.program:
            lines.append(f"En _{self.program}_")

        lines.append(f"**Coordinador:** {self.head.name}")

        lines.append(f"**Entidad ejecutora:** {self.main_entity}")

        if self.entities:
            lines.append(f"**Entidades participantes:** {', '.join(self.entities)}")

        lines.append(f"**Fecha de aprobación:** {self.aproval_date}")

        duration = (self.end_date - self.start_date).days // 30
        lines.append(f"**Duración**: {self.start_date} a {self.end_date} ({duration} meses)")

        lines.append(f"**Estado**: {self.status}")

        return ". ".join(lines)


    @classmethod
    def create(cls, key, obj=None):
        code = st.text_input("Código (si tiene)", key=f"{key}_code").strip()
        title = st.text_input("🔹Título del proyecto", key=f"{key}_title").strip()
        project_type = st.selectbox(
            "Tipo de proyecto",
            key=f"{key}_type",
            options=[
                "Nacional",
                "Sectorial",
                "Territorial",
                "Institucional",
                "Con Entidad no Empresarial",
                "Internacional",
                "Empresarial",
                "Desarrollo Local",
            ],
        )

        if project_type in ["Nacional", "Sectorial", "Territorial"]:
            program = st.text_input(
                f"🔹Nombre del Programa {project_type}", key=f"{key}_program"
            ).strip()
        else:
            program = ""

        main_entity = st.text_input(
            "🔹Entidad ejecutora (principal)", key=f"{key}_entity"
        ).strip()
        entities = [
            s.strip()
            for s in st.text_area(
                "Entidades participantes adicionales (una por línea)",
                key=f"{key}_entities",
            ).split("\n")
        ]
        funding = [
            s.strip()
            for s in st.text_area(
                "Entidades que financian (una por línea)", key=f"{key}_funding"
            ).split("\n")
        ]

        people = Person.all()
        people.sort(key=lambda p: p.name)

        head = st.selectbox(
            "Jefe / coordinador",
            people,
            key=f"{key}_head",
            format_func=lambda p: f"{p.name} ({p.institution})",
        )
        members = st.multiselect("Miembros", people, key=f"{key}_members")

        aproved = st.checkbox(
            "¿El proyecto está en ejecución? (No marque si está enviado pero no aprobado)",
            key=f"{key}_aproved",
        )

        if aproved:
            aproval_date = st.date_input("Fecha de aprobación", key=f"{key}_aproval")
            start_date = st.date_input("Fecha de inicio", key=f"{key}_start")
            end_date = st.date_input("Fecha de fin (tentativa)", key=f"{key}_end")
            state = st.selectbox(
                "Estado de la ejecución",
                ["Normal", "Atrasado", "Detenido", "Finalizado"],
                key=f"{key}_state",
            )
        else:
            aproval_date = None
            start_date = None
            end_date = None
            state = ""

        if not title:
            return

        if project_type in ["Nacional", "Sectorial", "Territorial"] and not program:
            return

        if not main_entity:
            return

        return Project(
            uuid=key,
            code=code,
            title=title,
            project_type=project_type,
            program=program,
            main_entity=main_entity,
            entities=entities,
            funding=funding,
            head=head,
            members=members,
            aproved=aproved,
            aproval_date=aproval_date,
            start_date=start_date,
            end_date=end_date,
            status=state,
        )


class Award(CustomModel):
    name: str
    institution: str
    title: str = ""
    participants: List[Person]
    awarded: bool = False
    date: date = None

    @classmethod
    def create(cls, key, obj=None):
        people = Person.all()
        people.sort(key=lambda p: p.name)

        name = st.text_input("🔹Nombre del premio", key=f"{key}_award_name")
        institution = st.text_input("🔹Institución que otorga el premio", key=f"{key}_award_institution")
        title = st.text_input("Título del artículo, proyecto, etc., que se premia (si aplica)", key=f"{key}_award_title")
        participants = st.multiselect("🔹Participantes", people, key=f"{key}_award_participants")
        awarded = st.checkbox("El premio ha sido otorgado (no marque si es todavía una propuesta)", key=f"{key}_award_awarded")

        if awarded:
            date = st.date_input("Fecha de otorgamiento", key=f"{key}_award_date")
        else:
            date = None

        if not name:
            return

        if not institution:
            return

        if not participants:
            return

        return Award(
            name=name,
            institution=institution,
            title=title,
            participants=participants,
            awarded=awarded,
            date=date,
        )

class Court(CustomModel):
    thesis: Thesis = None
    members: List[Person]
    date: Datetime = None
    minutes_duration: int
    place: str
    
    def check(self):
        if len(self.members) < 1:
            raise ValueError("Se debe agregar los miembros del tribunal")
        
        for court in Court.all():
            if court.thesis == self.thesis:
                raise ValueError("Ya existe un tribual para esta tesis")

            end_time = court.date + timedelta(minutes=court.minutes_duration)
            self_end_time = self.date + timedelta(minutes=self.minutes_duration)
        
            if court.date.date() == self.date.date():
                if court.date.time() <= self.date.time() <= end_time.time() or self.date.time() <= court.date.time() <= self_end_time.time():
                    
                    # two theses in the same place and the same hour
                    if self.place == court.place:
                        raise ValueError(f"Ya existe una discusión de una tesis en __{court.place}__ a esa hora")

                    # a peron in two places in the same moment
                    for member in self.members:
                        if member in court.members:
                            raise ValueError(f"__{member.name}__ ya está en otro tribunal en ese momento")

        return True