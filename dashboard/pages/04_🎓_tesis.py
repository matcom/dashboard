import collections
import json
import datetime
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st
from models import Thesis, Court, Person, Place
from modules.utils import generate_widget_key
from modules.graph import build_advisors_graph

st.set_page_config(page_title="MatCom Dashboard - Tesis", page_icon="🎓", layout="wide")

listing, create, thesis_details, courts, court_details = st.tabs(["📃 Listado", "➕ Crear nueva Tesis", "📄 Detalles - Tesis", "🤵 Tribunales", "📜 Detalles - Tribunales"])

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

    graph = build_advisors_graph(advisors, theses)

with create:
    if st.session_state.get('write_access', False):
        if (
            st.radio("Tipo de entrada", ["⭐ Nueva entrada", "📝 Editar"], horizontal=True, label_visibility="collapsed")
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
                st.session_state["file_uploader_key"] = generate_widget_key();
            pdf = st.file_uploader(
                "📤 Subir Tesis",
                type="pdf",
                key= st.session_state["file_uploader_key"]
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

            st.code(thesis.yaml(), "yaml")
    else:
        st.error("Acceso de solo lectura. Vaya a la página principal para loguearse.")
        
with thesis_details:
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
            btn=st.download_button(
                label="📥 Descargar Tesis",
                data=file,
                file_name=name_pdf,
                
            )
    else:
        st.write(f"####   No existe el pdf de la tesis")            

with courts:
    if st.session_state.get('write_access', False):
        selected = st.radio(
            "Tipo de entrada", 
            ["⭐ Nuevo Tribunal"] + (["📝 Editar Tribunal"] if len(Court.all()) > 0 else []), 
            horizontal=True, 
            label_visibility="collapsed"
        )
        
        if selected == "📝 Editar Tribunal":        
            court = st.selectbox(
                "Seleccione un tribunal a modificar",
                sorted(Court.all(), key=lambda c: c.thesis.title),
                format_func=lambda c: f"{c.thesis.title}",
            )
        else:
            court = Court(thesis=None, members=[], date=None, minutes_duration=60, place=None)
            
        left, right = st.columns([2, 1])

        with left:
            
            if selected == "⭐ Nuevo Tribunal":
                theses = sorted(theses, key=lambda t: t.title)
                court.thesis = st.selectbox(
                    "Seleccione una tesis",
                    theses,
                    format_func=lambda t: f"{t.title} - {t.authors[0]}",
                    index=theses.index(court.thesis if court.thesis else theses[0]),
                    key='courts_select_thesis',
                )
                
            court.members = st.multiselect(
                'Seleccione los miembros de la tesis', 
                Person.all(),
                [p for p in Person.all() if p.name in court.thesis.advisors] # selected advisors
            )
            
            places = sorted(Place.all(), key=lambda p: p.description) + [ Place(description="➕ Nueva entrada") ]
            court.place = st.selectbox(
                'Seleccione un local',
                places,
                format_func=lambda p: p.description,
                index=places.index(court.place if court.place else places[0]),
                key='courts_select_places',
            )
            if court.place.description == "➕ Nueva entrada":
                court.place.description = st.text_input(
                    "Descripción del lugar",
                    key="court_place_description",
                )
            
            date = st.date_input(
                'Seleccione una fecha', 
                value=court.date.date() if court.date else datetime.date.today(),
            )
            time = st.time_input(
                'Seleccione una hora', 
                value=court.date.time() if court.date else datetime.time(9, 0),
            )
            court.date = datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=time.hour,
                minute=time.minute
            )

            court.minutes_duration = st.number_input(
                'Introduce los minutos de duración',
                step=5,
                min_value=20,
                value = court.minutes_duration
            )
            
        with right:
            try:
                court.check()
                
                if st.button("💾 Guardar Tribunal"):
                    court.save()
                    court.place.save()
                    if selected == "⭐ Nuevo Tribunal":
                        st.success(f"¡Tribunal de la tesis _{court.thesis.title}_ creada con éxito!")   
                    elif selected == "📝 Editar Tribunal":
                        st.success(f"¡Tribunal de la tesis _{court.thesis.title}_ editada con éxito!")   
                    
            except ValueError as e:
                st.error(e)
    else:
        st.error("Acceso de solo lectura. Vaya a la página principal para loguearse.")
        

with court_details:
    st.write("##### 🏷️ Filtros")
    
    places = sorted(Place.all(), key=lambda p: p.description)
    member_selected = st.selectbox(
        "Filtrar por un miembro de tribunal",
        ["Todos"] + [ p.name for p in Person.all() ],
        key='court_details_select_member',
    )

    place_selected = st.selectbox(
        "Filtrar por un lugar",
        ["Todos"] + [ p for p in places ],
        key='court_details_select_place',
    )
   
    data = []
    for court in Court.all():
        include = True
        if member_selected != "Todos":
            if member_selected not in [p.name for p in court.members]:
                include = False

        if place_selected != "Todos":
            if place_selected != court.place:
                include = False
    
        if include:
            data.append(court.print())
    
    
    if len(data) > 0:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.error("No hay datos para mostrar")