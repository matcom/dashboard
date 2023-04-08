import auth
import streamlit as st
from models import Journal, JournalPaper, Person


def papers_page(router, from_year=None, to_year=None, **params):
    st.set_page_config(page_title="MatCom Dashboard - Artículos", layout="wide")
    router.page_header("📃 Artículos")

    # year = st.sidebar.selectbox("Año", [2020, 2021, 2022], index=2)
    people = Person.all()
    people.sort(key=lambda p: p.name)

    journals = Journal.all()
    journals.sort(key=lambda j: j.title)

    years = list(range(int(from_year or 2020), int(to_year or 2022) + 1))
    papers = [p for p in JournalPaper.all() if p.year in years]
    papers.sort(key=lambda p: p.title)

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

    for paper in papers:
        st.write(paper.format())
