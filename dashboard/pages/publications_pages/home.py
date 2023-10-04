from typing import Dict

import auth
import streamlit as st
from models import (
    Book,
    BookChapter,
    ConferencePresentation,
    Journal,
    JournalPaper,
    Person,
)
from modules.graph import build_publications_graph
from page_router import PageRouter


def home_page(router: PageRouter, **params):
    st.set_page_config(
        page_title="MatCom Dashboard - Publicaciones", page_icon="📚", layout="wide"
    )

    router.page_header("Publicaciones")
    st.markdown("#### *Todo lo relacionado con artículos, revistas, libros, etc*")

    with st.expander("Índice"):
        if st.button("📃 Artículos", type="secondary"):
            router.go("home/papers", from_year=2020)
        if st.button("📢 Presentaciones"):
            router.go("home/presentations")
        if st.button("📕 Libros y Capítulos de Libros"):
            router.go("home/books-and-chapters")
        if st.button("🗞️ Revistas"):
            router.go("home/journals")

    year = st.sidebar.selectbox("Año", [2020, 2021, 2022], index=2)

    people = Person.all()
    people.sort(key=lambda p: p.name)

    journals = Journal.all()
    journals.sort(key=lambda j: j.title)

    papers = [p for p in JournalPaper.all() if p.year == year]
    papers.sort(key=lambda p: p.title)

    books = [b for b in Book.all() if b.year == year]
    books.sort(key=lambda b: b.title)

    chapters = [c for c in BookChapter.all() if c.year == year]
    chapters.sort(key=lambda b: b.chapter)

    presentations = [p for p in ConferencePresentation.all() if p.year == year]
    presentations.sort(key=lambda p: p.title)

    publications = {
        "papers": {
            "title": "Artículos",
            "data": papers,
        },
        "presentations": {
            "title": "Presentaciones",
            "data": presentations,
        },
        "books": {
            "title": "Libros",
            "data": books,
        },
        "chapters": {
            "title": "Capítulos",
            "data": chapters,
        },
    }

    st.write("### 📊Gráfica de publicaciones")

    options = [publication["title"] for publication in publications.values()]
    selection = st.multiselect(
        "Seleccione las publicaciones que desea incluir en el gráfico",
        options,
        ["Libros", "Capítulos"],
    )

    # show in the graph
    data = []
    for publication in publications.values():
        if publication["title"] in selection:
            for item in publication["data"]:
                data.append(item)

    sections = {"Todas": True}
    for publ in data:
        for author in publ.authors:
            if author.department != "":
                sections[author.department] = True
            if author.department != "":
                sections[author.institution] = True
            if author.department != "":
                sections[author.faculty] = True

    section = st.selectbox("Seleccionar una sección", sections.keys(), index=0)
    color = st.color_picker("Color de la sección", "#ACDBC9", key=654)

    _, _, graph = build_publications_graph(data, color=[section, color], height=1000)
