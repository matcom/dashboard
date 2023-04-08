from typing import Dict

import auth
import streamlit as st
from models import Book, BookChapter, Person


def books_and_chapters_page(router, **params):
    st.set_page_config(page_title="MatCom Dashboard - Libros y Capítulos de Libros", layout="wide")
    router.page_header("📕 Libros y Capítulos de Libros")

    year = st.sidebar.selectbox("Año", [2020, 2021, 2022], index=2)

    people = Person.all()
    people.sort(key=lambda p: p.name)

    books = [b for b in Book.all() if b.year == year]
    books.sort(key=lambda b: b.title)

    chapters = [c for c in BookChapter.all() if c.year == year]
    chapters.sort(key=lambda b: b.chapter)

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
