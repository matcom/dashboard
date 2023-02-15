import collections
import json
from pathlib import Path
from typing import List

import auth
import pandas as pd
import streamlit as st
import yaml
from models import Thesis
from modules.graph import build_advisors_graph
from modules.utils import generate_widget_key

st.set_page_config(page_title="MatCom Dashboard - Tesis", page_icon="🎓", layout="wide")

listing, create, details = st.tabs(["📃 Listado", "➕ Crear nueva Tesis", "📄 Detalles"])

theses: List[Thesis] = Thesis.all()

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

    graph = build_advisors_graph(advisors, theses)

with create:
    if auth.is_user_logged():
        if (
            st.radio(
                "Tipo de entrada",
                ["⭐ Nueva entrada", "📝 Editar"],
                horizontal=True,
                label_visibility="collapsed",
            )
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
            if "file_uploader_key" not in st.session_state:
                st.session_state["file_uploader_key"] = generate_widget_key()
            pdf = st.file_uploader(
                "📤 Subir Tesis", type="pdf", key=st.session_state["file_uploader_key"]
            )

        with right:
            try:
                thesis.check()

                if st.button("💾 Salvar Tesis"):
                    if pdf:
                        thesis.save_thesis_pdf(pdf)
                    thesis.save()
                    st.success(f"¡Tesis _{thesis.title}_ creada con éxito!")
                    st.session_state["file_uploader_key"] = generate_widget_key()

            except ValueError as e:
                st.error(e)

            st.code(yaml.dump(thesis.encode()), "yaml")

with details:
    thesis = st.selectbox(
        "Seleccione una tesis",
        sorted(theses, key=lambda t: t.title),
        format_func=lambda t: f"{t.title} - {t.authors[0]}",
    )

    st.write(f"#### 📝 Título: {thesis.title}")
    st.write(f"#### 👤 Autores: {', '.join(thesis.authors)}")
    st.write(f"#### 👨‍🏫 Tutores: {', '.join(thesis.advisors)}")
    st.write(f"#### 🔑 Palabras clave: {', '.join(thesis.keywords)}")
    st.write(f"#### 📄 Versión: {thesis.version}")
    st.write(f"#### 📚 Balance: {thesis.balance}")

    name_pdf = f"{thesis.uuid}_v{thesis.version}.pdf"
    path: Path = Path(f"/src/data/Thesis/files/{name_pdf}")

    if path.exists():
        with open(path, "rb") as file:
            btn = st.download_button(
                label="📥 Descargar Tesis",
                data=file,
                file_name=name_pdf,
            )
    else:
        st.write(f"####   No existe el pdf de la tesis")
