from typing import Dict

import altair
import auth
import pandas as pd
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

st.set_page_config(
    page_title="MatCom Dashboard - Publicaciones", page_icon="📚", layout="wide"
)

year = st.sidebar.selectbox("Año", [2020, 2021, 2022], index=2)

people = Person.all()
people.sort(key=lambda p: p.name)

journals = Journal.all()
journals.sort(key=lambda j: j.title)

papers = [p for p in JournalPaper.all() if p.year == year]
papers.sort(key=lambda p: p.title)

papers_tab, presentations_tab, books_tab, journals_tab, create_tab = st.tabs(
    [
        "📃 Artículos",
        "📢 Presentaciones",
        "📕 Libros y Capítulos de Libros",
        "🗞️ Revistas",
        "⭐ Nueva entrada / Editar",
    ]
)

with papers_tab:
    if auth.is_user_logged():
        with st.expander("⭐ Nuevo artículo / 📝 Editar"):
            if (
                st.radio(
                    "Tipo de artículo",
                    ["⭐ Nueva entrada", "📝 Editar"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                == "📝 Editar"
            ):
                paper = st.selectbox(
                    "Seleccione un artículo a modificar",
                    papers,
                    format_func=lambda p: f"{p.title} - {p.authors[0]}",
                )
            else:
                paper = JournalPaper(title="", authors=[], journal=journals[0])
            author_name, author_institution = st.columns(2)
            with author_name:
                name = st.text_input("Nombre del autor", "", key="author_name")
            with author_institution:
                institution = st.text_input(
                    "Institución del autor", value="", key="institution"
                )
            if st.button("Añadir"):
                # add to people if it does not exist
                # exist the option that there are two people with the same name but different institutions
                # in this case I consider it appropriate that the people with the institution they belong to are shown
                # so that there is no confusion
                # this is a change that could be done in the future
                person = next((p for p in people if p.name == name), None)
                if person is None:
                    person = Person(name=name, institution=institution)
                    person.save()
                    people.append(person)
                    people.sort(key=lambda p: p.name)

                else:
                    st.warning("Ya existe una persona con ese nombre")

            paper.title = st.text_input("Título", key="paper_title", value=paper.title)
            paper.authors = st.multiselect(
                "Autores", key="paper_authors", options=people, default=paper.authors
            )

            if paper.authors:
                paper.corresponding_author = st.selectbox(
                    "Autor por correspondencia",
                    options=paper.authors,
                    index=paper.authors.index(paper.corresponding_author)
                    if paper.corresponding_author
                    else 0,
                )

            paper.journal = st.selectbox(
                "Journal",
                options=journals + ["➕ Nueva entrada"],
                index=journals.index(paper.journal),
            )

            if paper.journal == "➕ Nueva entrada":
                journal_title = st.text_input("Título del Journal", key="journal_title")
                journal_publisher = st.text_input("Editorial", key="journal_publisher")
                journal_issn = st.text_input("ISSN", key="journal_issn")

                paper.journal = Journal(
                    title=journal_title, publisher=journal_publisher, issn=journal_issn
                )

            paper.volume = st.number_input(
                "Volumen", key="paper_volumen", min_value=1, value=paper.volume
            )
            paper.issue = st.number_input(
                "Número", key="paper_issue", min_value=1, value=paper.issue
            )
            paper.year = st.number_input(
                "Año",
                key="paper_year",
                min_value=2020,
                max_value=2022,
                value=paper.year,
            )
            paper.url = st.text_input("URL", value=paper.url)

            if st.button("💾 Guardar artículo"):
                paper.journal.save()
                paper.save()
                st.success("Entrada salvada con éxito.")

    st.write(f"#### 📃 Artículos `{len(papers)}`")

    data = []

    for paper in papers:
        st.write(paper.format())


presentations = [p for p in ConferencePresentation.all() if p.year == year]
presentations.sort(key=lambda p: p.title)


with presentations_tab:
    if auth.is_user_logged():
        with st.expander("⭐ Nueva presentación / 📝 Editar"):
            if (
                st.radio(
                    "Tipo de presentación",
                    ["⭐ Nueva entrada", "📝 Editar"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                == "📝 Editar"
            ):
                presentation = st.selectbox(
                    "Seleccione una presentación a modificar",
                    presentations,
                    format_func=lambda p: f"{p.title}",
                )
            else:
                presentation = ConferencePresentation(
                    title="", authors=[], venue="", location=""
                )

            presentation.title = st.text_input(
                "Título", key="presentation_title", value=presentation.title
            )
            presentation.authors = st.multiselect(
                "Autores",
                key="presentation_authors",
                options=people,
                default=presentation.authors,
            )

            presentation.venue = st.text_input(
                "Evento", key="presentation_venue", value=presentation.venue
            )
            presentation.location = st.text_input(
                "Lugar", key="presentation_location", value=presentation.location
            )
            types = ["Internacional", "Nacional", "Actividad Científica"]
            presentation.event_type = st.selectbox(
                "Tipo", types, index=types.index(presentation.event_type)
            )
            presentation.year = st.number_input(
                "Año",
                key="presentation_year",
                min_value=2020,
                max_value=2022,
                value=presentation.year,
            )
            presentation.paper = st.checkbox(
                "Tiene publicación en proceedings (seriada)?",
                key="presentation_paper",
                value=presentation.paper,
            )

            if st.button("💾 Guardar presentación"):
                presentation.save()
                st.success("Entrada salvada con éxito.")

    st.write(f"#### 📢 Presentaciones `{len(presentations)}`")

    data = []

    for presentation in presentations:
        st.write(presentation.format())


books = [b for b in Book.all() if b.year == year]
books.sort(key=lambda b: b.title)

chapters = [c for c in BookChapter.all() if c.year == year]
chapters.sort(key=lambda b: b.chapter)

with books_tab:
    if auth.is_user_logged():
        with st.expander("⭐ Nuevo libro / 📝 Editar"):
            if (
                st.radio(
                    "Tipo de libro",
                    ["⭐ Nueva entrada", "📝 Editar"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                == "📝 Editar"
            ):
                book = st.selectbox(
                    "Seleccione un libro a modificar",
                    books + chapters,
                    format_func=lambda p: f"{p.title} - {p.authors[0]}",
                )
            else:
                if st.selectbox("Tipo", ["Libro", "Capítulo de Libro"]) == "Libro":
                    book = Book(title="", publisher="", authors=[])
                else:
                    book = BookChapter(title="", publisher="", authors=[], chapter="")

            book.title = st.text_input(
                "Título del Libro", key="book_title", value=book.title
            )

            if isinstance(book, BookChapter):
                book.chapter = st.text_input(
                    "Título del Capítulo", key="chapter_title", value=book.chapter
                )

            book.authors = st.multiselect(
                "Autores",
                key="book_authors",
                options=people,
                default=book.authors,
            )

            book.publisher = st.text_input(
                "Editorial", key="book_publisher", value=book.publisher
            )
            book.isbn = st.text_input("ISBN", key="book_isbn", value=book.isbn)
            book.year = st.number_input(
                "Año",
                key="book_year",
                min_value=2020,
                max_value=2022,
                value=book.year,
            )
            book.edition = st.number_input(
                "Edición",
                key="book_edition",
                min_value=1,
                value=book.edition,
            )
            book.pages = st.number_input(
                "Páginas",
                key="book_pages",
                min_value=0,
                value=book.pages or 0,
            )

            if st.button("💾 Guardar libro"):
                book.save()
                st.success("Entrada salvada con éxito.")

    st.write(f"#### 📕 Libros y Capítulos de Libros `{len(books) + len(chapters)}`")

    data = []

    for book in books:
        st.write(book.format())

    for chapter in chapters:
        st.write(chapter.format())


journals = Journal.all()
journals.sort(key=lambda j: j.title)

with journals_tab:
    st.write(f"#### 🗞️ Revistas `{len(journals)}`")

    with st.expander("Editar revista"):
        journal = st.selectbox("Revista", journals)

        journal.title = st.text_input(
            "Título", key=f"journal_title_{journal.uuid}", value=journal.title
        )
        journal.publisher = st.text_input(
            "Editorial",
            key=f"journal_publisher_{journal.uuid}",
            value=journal.publisher,
        )
        journal.issn = st.text_input(
            "ISSN", key=f"journal_issn_{journal.uuid}", value=journal.issn
        )
        journal.url = (
            st.text_input(
                "URL", key=f"journal_url_{journal.uuid}", value=journal.url or ""
            )
            or None
        )
        journal.indices = st.multiselect(
            "Indexado en",
            key=f"journal_indices_{journal.uuid}",
            options=[
                "Web of Science",
                "Scopus",
                "RICYT",
                "Scielo",
                "Otro (Internacional)",
                "Otro (Nacional)",
            ],
            default=journal.indices,
        )

        if st.button("💾 Guardar"):
            journal.save()
            st.success("Cambios guardados")

    for journal in journals:
        st.write(journal.format())

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
