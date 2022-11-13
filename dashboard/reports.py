import streamlit as st
import collections
import altair
import pandas as pd

from typing import List
from models import (
    Person,
    JournalPaper,
    ConferencePresentation,
    Book,
    BookChapter,
    Project,
)


def personal_report(person: Person):
    lines = []

    lines.append("### 👤 Información personal\n")
    lines.append(f"- **Institución**: {person.institution}")
    lines.append(f"- **Facultad**: {person.faculty}")
    lines.append(f"- **Departamento**: {person.department}")
    lines.append(f"- **Grado científico:** {person.scientific_grade}")
    lines.append(f"- **Categoría docente:** {person.academic_grade}")

    if person.orcid:
        lines.append(
            f"- **Perfil ORCID:** [{person.orcid}](https://orcid.org/{person.orcid})"
        )

    lines.append("### 📚 Publicaciones")

    lines.append("#### 📃 Artículos")

    for paper in JournalPaper.from_authors([person]):
        lines.append("- " + paper.format())

    lines.append("#### 📢 Ponencias")

    for paper in ConferencePresentation.from_authors([person]):
        lines.append("- " + paper.format())

    lines.append("#### 📕 Libros y Capítulos de Libro")

    for paper in Book.from_authors([person]):
        lines.append("- " + paper.format())

    for paper in BookChapter.from_authors([person]):
        lines.append("- " + paper.format())

    lines.append("### ⚗️ Proyectos")

    for project in Project.from_members([person]):
        lines.append("- " + project.format())

    for line in lines:
        yield line


def research_balance(start_date, end_date):
    lines = []

    papers = [p for p in JournalPaper.all() if p.year == end_date.year]
    papers.sort(key=lambda p: p.title)

    presentations = [p for p in ConferencePresentation.all() if p.year == end_date.year and p.paper]
    presentations.sort(key=lambda p: p.title)

    books = [p for p in Book.all() if p.year == end_date.year]
    books.sort(key=lambda b: b.title)

    chapters = [p for p in BookChapter.all() if p.year == end_date.year]
    chapters.sort(key=lambda b: b.title)

    wos_scopus = []
    ricyt_scielo = []
    international = []
    national = []
    uh = []
    rest = []
    colab = []

    for paper in papers:
        if (
            "Web of Science" in paper.journal.indices
            or "Scopus" in paper.journal.indices
        ):
            wos_scopus.append(paper)
        elif "RICYT" in paper.journal.indices or "Scielo" in paper.journal.indices:
            ricyt_scielo.append(paper)
        elif "Otro (Internacional)" in paper.journal.indices:
            international.append(paper)
        elif "Otro (Nacional)" in paper.journal.indices:
            national.append(paper)
        elif "Universidad de La Habana" != paper.journal.publisher:
            rest.append(paper)

        if paper.journal.publisher == "Universidad de La Habana":
            uh.append(paper)

        for author in paper.authors:
            if author.institution != "Universidad de La Habana":
                colab.append(author)
                break

    events = [p for p in ConferencePresentation.all() if p.year == end_date.year]
    events.sort(key=lambda e: e.title)

    international_events = collections.defaultdict(list)
    international_cuba = collections.defaultdict(list)
    national_events = collections.defaultdict(list)
    activities = collections.defaultdict(list)

    for e in events:
        if e.event_type == "Internacional":
            if "Cuba" in str(e.location):
                international_cuba[(e.venue, e.location)].append(e)
            else:
                international_events[(e.venue, e.location)].append(e)
        elif e.event_type == "Nacional":
            national_events[(e.venue, e.location)].append(e)
        else:
            activities[(e.venue, e.location)].append(e)

    yield "### 📃 Publicaciones"

    data = pd.DataFrame(
            [
                dict(Tipo="Total", Cantidad=len(papers) + len(presentations) + len(books) + len(chapters)),
                dict(Tipo="Artículos", Cantidad=len(papers)),
                dict(Tipo="WoS / Scopus", Cantidad=len(wos_scopus)),
                dict(Tipo="RICYT / Scielo", Cantidad=len(ricyt_scielo)),
                dict(Tipo="Internacional", Cantidad=len(international)),
                dict(Tipo="Nacional", Cantidad=len(national)),
                dict(Tipo="Editorial UH", Cantidad=len(uh)),
                dict(Tipo="Sin índice", Cantidad=len(rest)),
                dict(Tipo="Colaboraciones", Cantidad=len(colab)),
                dict(Tipo="Presentaciones", Cantidad=len(presentations)),
                dict(Tipo="Libros, etc", Cantidad=len(books) + len(chapters)),
            ]
        )

    yield data

    yield altair.Chart(data).mark_bar().encode(y="Tipo", x="Cantidad")

    yield "#### 📃 Artículos"

    for paper in wos_scopus:
        yield paper.format()

    for paper in ricyt_scielo:
        yield paper.format()

    for paper in international:
        yield paper.format()

    for paper in national:
        yield paper.format()

    for paper in uh:
        yield paper.format()

    for paper in rest:
        yield paper.format()

    yield "#### 📢 Presentaciones (con publicación)"

    for presentation in presentations:
        yield presentation.format()

    yield "#### 📕 Libros y Capítulos de Libro"

    for book in books:
        yield book.format()

    for chapter in chapters:
        yield chapter.format()

    yield "### 📢 Eventos"

    yield "#### 💠 Internacionales"

    for (venue, location), events in international_events.items():
        yield f"_{venue}_, {location}: **{len(events)} ponencia(s)**"

    yield "#### 💠 Internacionales en Cuba"

    for (venue, location), events in international_cuba.items():
        yield f"_{venue}_, {location}: **{len(events)} ponencia(s)**"

    yield "#### 💠 Nacionales"

    for (venue, location), events in national_events.items():
        yield f"_{venue}_, {location}: **{len(events)} ponencia(s)**"

    yield "#### 💠 Actividades Científicas"

    for (venue, location), events in activities.items():
        yield f"_{venue}_, {location}: **{len(events)} ponencia(s)**"
