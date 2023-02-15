from datetime import date
from typing import List

import streamlit as st
from models.custom_model import CustomModel, RefList, with_refs
from models.data_models.person_model import Person


@with_refs
class Award(CustomModel):
    name: str
    institution: str
    title: str = ""
    participants: RefList[Person]
    awarded: bool = False
    date: date

    @classmethod
    def from_persons(cls, people: List[Person]):
        persons_ids = {p.uuid for p in people}
        for award in cls.all():
            if award.awarded and set(award.participants_ref.uuids) & persons_ids:
                yield award

    @classmethod
    def create(cls, key, obj=None):
        people = Person.all()
        people.sort(key=lambda p: p.name)

        name = st.text_input("🔹Nombre del premio", key=f"{key}_award_name")
        institution = st.text_input(
            "🔹Institución que otorga el premio", key=f"{key}_award_institution"
        )
        title = st.text_input(
            "Título del artículo, proyecto, etc., que se premia (si aplica)",
            key=f"{key}_award_title",
        )
        participants = st.multiselect(
            "🔹Participantes", people, key=f"{key}_award_participants"
        )
        awarded = st.checkbox(
            "El premio ha sido otorgado (no marque si es todavía una propuesta)",
            key=f"{key}_award_awarded",
        )

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
