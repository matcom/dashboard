import streamlit as st
from models import Book, BookChapter, ConferencePresentation, Journal, JournalPaper


def journals_page(router, **params):
    st.set_page_config(page_title="MatCom Dashboard - Revistas", layout="wide")
    router.page_header("🗞️ Revistas")

    year = st.sidebar.selectbox("Año", [2020, 2021, 2022], index=2)

    journals = Journal.all()
    journals.sort(key=lambda j: j.title)

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
