import collections
import json
from pathlib import Path
from typing import List
from random import randint

import altair
import pandas as pd
import streamlit as st
from models import Thesis

st.set_page_config(page_title="MatCom Dashboard - Tesis", page_icon="🎓", layout="wide")

listing, create = st.tabs(["📃 Listado", "➕ Crear nueva Tesis"])

theses: List[Thesis] = []

for path in Path("/src/data/Thesis/").rglob("*.yaml"):
    with open(path) as fp:
        theses.append(Thesis.load(fp))

with listing:
    st.write("##### 🏷️ Filtros")

    advisors = collections.defaultdict(list)

    for thesis in theses:
        for advisor in thesis.advisors:
            advisors[advisor].append(thesis)

    advisors_list = list(sorted(advisors))

    selected_advisors = set(
        st.multiselect(f"Tutores ({len(advisors_list)})", advisors_list)
    )
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
    st.download_button(
        "💾 Descargar como JSON", json.dumps(data, ensure_ascii=False, indent=2)
    )

    st.write("#### 👥 Distribución por tutores")

    cols = st.columns(2)

    thesis_df = []

    for thesis in theses:
        for advisor in thesis.advisors:
            for keyword in thesis.keywords:
                thesis_df.append(
                    dict(thesis=thesis.title, advisor=advisor, keyword=keyword)
                )

    thesis_df = pd.DataFrame(thesis_df)

    cols[0].altair_chart(
        altair.Chart(thesis_df)
        .mark_bar()
        .encode(
            y=altair.X("advisor", title="Tutor"),
            x=altair.Y("distinct(thesis)", title="No. Tesis"),
            color=altair.Color("advisor", legend=None),
            tooltip=[altair.Tooltip("distinct(thesis)", title="No. Tesis")],
        )
    )

    coauthor_df = []

    for thesis in theses:
        for advisor_i in thesis.advisors:
            for advisor_j in thesis.advisors:
                if advisor_i == advisor_j:
                    continue

                coauthor_df.append(
                    dict(thesis=thesis.title, advisor_i=advisor_i, advisor_j=advisor_j)
                )

    coauthor_df = pd.DataFrame(coauthor_df)

    cols[1].altair_chart(
        altair.Chart(coauthor_df)
        .mark_point(filled=True)
        .encode(
            x=altair.X("advisor_i", title="Tutor"),
            y=altair.Y("advisor_j", title="Tutor"),
            color=altair.Color("advisor_i", legend=None),
            size=altair.Size("count(thesis)", legend=None),
            tooltip=[
                altair.Tooltip("count(thesis)", title="No. Tesis"),
                altair.Tooltip("advisor_i", title="Tutor (1)"),
                altair.Tooltip("advisor_j", title="Tutor (2)"),
            ],
        )
        .properties(width=600, height=600)
    )


with create:
    if (
        st.radio("Tipo de entrada", ["⭐ Nueva entrada", "📝 Editar"], horizontal=True)
        == "📝 Editar"
    ):
        thesis = st.selectbox(
            "Seleccione una tesis a modificar",
            sorted(theses, key=lambda t: t.title),
            format_func=lambda t: f"{t.title} - {t.authors[0]}",
        )
    else:
        thesis = Thesis(title="", authors=[], advisors=[], keywords=[])

    left, right = st.columns([2, 1])

    with left:
        thesis.title = st.text_input(
            "Título", key="thesis_title", value=thesis.title
        ).strip()
        thesis.authors = [
            s.strip()
            for s in st.text_area(
                "Autores (uno por línea)",
                key="thesis_authors",
                value="\n".join(thesis.authors),
            ).split("\n")
        ]
        thesis.advisors = [
            s.strip()
            for s in st.text_area(
                "Tutores (uno por línea)",
                key="thesis_advisors",
                value="\n".join(thesis.advisors),
            ).split("\n")
        ]
        thesis.keywords = [
            s.strip()
            for s in st.text_input(
                "Palabras clave (separadas por ;)",
                key="thesis_keywords",
                value=";".join(thesis.keywords),
            ).split(";")
        ]
        if  "widget_key" not in st.session_state: 
            st.session_state["widget_key"] = str(randint(0, 1000000))
            
        pdf = st.file_uploader(
            "📤 Subir Tesis", 
            type="pdf",
            key= st.session_state.widget_key
        )

    with right:
        try:
            thesis.check()

            if st.button("💾 Salvar Tesis"):
                if pdf: thesis.save_thesis_pdf(pdf)
                thesis.save()
                st.success(f"¡Tesis _{thesis.title}_ creada con éxito!")
                st.session_state["widget_key"] = str(randint(0, 1000000))

        except ValueError as e:
            st.error(e)

        st.code(thesis.yaml(), "yaml")
