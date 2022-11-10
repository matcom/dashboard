from typing import Dict
import streamlit as st
import pandas as pd
import altair

from models import JournalPaper, Person, Journal, ConferencePresentation, Book, BookChapter


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

st.write(f"#### 📃 Artículos `{len(papers)}`")

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

    paper.issue = st.number_input(
        "Número", key="paper_issue", min_value=1, value=paper.issue
    )
    paper.year = st.number_input(
        "Año", key="paper_year", min_value=2020, max_value=2022, value=paper.year
    )
    paper.url = st.text_input("URL", value=paper.url)

    if st.button("💾 Guardar artículo"):
        paper.journal.save()
        paper.save()
        st.success("Entrada salvada con éxito.")


with st.expander("🔹 Listado de artículos"):
    data = []

    for paper in papers:
        text = [f"📃 _{paper.title}_."]

        for author in paper.authors:
            fmt = author.name

            if author.orcid:
                fmt = f"[{fmt}](https://orcid.org/{author.orcid})"

            if author.institution == "Universidad de La Habana":
                fmt = f"**{fmt}**"

            text.append(fmt.format(author.name) + ", ")

        text.append(
            f"En _{paper.journal.title}_, {paper.journal.publisher}. ISSN: {paper.journal.issn}."
        )
        text.append(f"Número {paper.issue}, {paper.year}.")
        st.write(" ".join(text))

presentations = [p for p in ConferencePresentation.all() if p.year == year]
presentations.sort(key=lambda p: p.title)

st.write(f"#### 📢 Presentaciones `{len(presentations)}`")

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
            format_func=lambda p: f"{p.title} - {p.authors[0]}",
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

with st.expander("🔹 Listado de presentaciones"):
    data = []

    for presentation in presentations:
        if presentation.paper:
            text = ["📃"]
        else:
            text = ["📢"]

        text.append(f"_{presentation.title}_.")

        for author in presentation.authors:
            fmt = author.name

            if author.orcid:
                fmt = f"[{fmt}](https://orcid.org/{author.orcid})"

            if author.institution == "Universidad de La Habana":
                fmt = f"**{fmt}**"

            text.append(fmt.format(author.name) + ", ")

        text.append(
            f"En _{presentation.venue}_, {presentation.location}, {presentation.year}"
        )

        st.write(" ".join(text))


books = [b for b in Book.all() if b.year == year]
books.sort(key=lambda b: b.title)

chapters = [c for c in BookChapter.all() if c.year == year]
chapters.sort(key=lambda b: b.chapter)

st.write(f"#### 📚 Libros y Capítulos de Libros `{len(books) + len(chapters)}`")

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
    book.isbn = st.text_input(
        "ISBN", key="book_isbn", value=book.isbn
    )
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

with st.expander("🔹 Listado de libros y capítulos"):
    data = []

    for book in books:
        text = [f"📕 _{book.title}_."]

        for author in book.authors:
            fmt = author.name

            if author.orcid:
                fmt = f"[{fmt}](https://orcid.org/{author.orcid})"

            if author.institution == "Universidad de La Habana":
                fmt = f"**{fmt}**"

            text.append(fmt.format(author.name) + ", ")

        text.append(
            f"{book.publisher}, ISBN: {book.isbn}, Edición: {book.edition}, Páginas: {book.pages}."
        )

        st.write(" ".join(text))

    for chapter in chapters:
        text = [f"📑 _{chapter.chapter}_."]

        for author in chapter.authors:
            fmt = author.name

            if author.orcid:
                fmt = f"[{fmt}](https://orcid.org/{author.orcid})"

            if author.institution == "Universidad de La Habana":
                fmt = f"**{fmt}**"

            text.append(fmt.format(author.name) + ", ")

        text.append(
            f"En _{chapter.title}_, {chapter.publisher}, ISBN: {chapter.isbn}, Edición: {chapter.edition}, Páginas: {chapter.pages}."
        )

        st.write(" ".join(text))
