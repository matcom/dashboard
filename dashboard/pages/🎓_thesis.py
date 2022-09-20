from typing import List
import pandas as pd
import json
from pathlib import Path
from models import Thesis
import streamlit as st

st.set_page_config(page_title="MatCom Dashboard - Tesis", page_icon="🎓", layout="wide")


listing, create = st.tabs(["📃 Listado", "➕ Crear nueva Tesis"])

theses: List[Thesis] = []

for path in Path("/src/data/Thesis/").rglob("*.yaml"):
    with open(path) as fp:
        theses.append(Thesis.load(fp))

with listing:
    st.write("##### 🏷️ Filtros")

    advisors = set()

    for thesis in theses:
        for advisor in thesis.advisors:
            advisors.add(advisor)

    advisors = list(sorted(advisors))

    selected_advisors = st.multiselect(f"Tutores ({len(advisors)})", advisors)
    data = []

    for thesis in theses:
        for advisor in thesis.advisors:
            if advisor in selected_advisors or not selected_advisors:
                d = thesis.encode()
                d.pop("uuid")
                data.append(d)
                break

    st.write(f"##### 📃 Listado de Tesis ({len(data)})")

    df = pd.DataFrame(data)
    st.dataframe(df)

    st.download_button("💾 Descargar como CSV", df.to_csv())
    st.download_button("💾 Descargar como JSON", json.dumps(data, indent=2))


with create:
    if st.radio("Tipo de entrada", ["⭐ Nueva entrada", "📝 Editar"], horizontal=True) == "📝 Editar":
        thesis = st.selectbox(
            "Seleccione una tesis a modificar",
            sorted(theses, key=lambda t: t.title),
            format_func=lambda t: f"{t.title} - {t.authors[0]}",
        )
    else:
        thesis = Thesis(title="", authors=[], advisors=[], keywords=[])

    left, right = st.columns([2, 1])

    with left:
        thesis.title = st.text_input("Título", key="thesis_title", value=thesis.title).strip()
        thesis.authors = [
            s.strip()
            for s in st.text_area(
                "Autores (uno por línea)", key="thesis_authors", value="\n".join(thesis.authors)
            ).split("\n")
        ]
        thesis.advisors = [
            s.strip()
            for s in st.text_area(
                "Tutores (uno por línea)", key="thesis_advisors", value="\n".join(thesis.advisors)
            ).split("\n")
        ]
        thesis.keywords = [
            s.strip()
            for s in st.text_input(
                "Palabras clave (separadas por ;)", key="thesis_keywords", value=";".join(thesis.keywords)
            ).split(";")
        ]

    with right:
        try:
            thesis.validate()

            if st.button("💾 Salvar Tesis"):
                thesis.save()
                st.success(f"¡Tesis _{thesis.title}_ creada con éxito!")

        except ValueError as e:
            st.error(e)

        st.code(thesis.yaml(), "yaml")
