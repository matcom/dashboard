from datetime import date
from typing import List

import streamlit as st

from models.custom_model import CustomModel, Ref, RefList, collection_name, with_refs
from models.data_models.person_model import Person


@with_refs
@collection_name("projects")
class Project(CustomModel):
    code: str = ""
    title: str
    project_type: str
    program: str = ""
    head: Ref[Person]
    members: RefList[Person]
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
    def from_members(cls, people: List[Person]):
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
        lines.append(
            f"**Duración**: {self.start_date} a {self.end_date} ({duration} meses)"
        )

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
