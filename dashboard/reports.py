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
    Award,
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

    presentations = [
        p for p in ConferencePresentation.all() if p.year == end_date.year and p.paper
    ]
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
        elif paper.journal.publisher == "Universidad de La Habana":
            uh.append(paper)
        else:
            rest.append(paper)

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
            dict(
                Tipo="Total",
                Cantidad=len(papers) + len(presentations) + len(books) + len(chapters),
            ),
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

    def total_events(d):
        return sum(len(v) for v in d.values())

    def total_events_first_author(d):
        return sum(1 for v in d.values() for e in v if e.authors[0].faculty == "MatCom")

    def total_events_colab_uh(d):
        return sum(
            1
            for v in d.values()
            for e in v
            if any(
                a.institution == "Universidad de La Habana"
                and not a.faculty == "MatCom"
                for a in e.authors
            )
        )

    yield pd.DataFrame(
        [
            dict(
                Tipo="Eventos Internacionales",
                Total=total_events(international_events),
                Principal=total_events_first_author(international_events),
                Colab=total_events_colab_uh(international_events),
            ),
            dict(
                Tipo="Eventos Internacionales en Cuba",
                Total=total_events(international_cuba),
                Principal=total_events_first_author(international_cuba),
                Colab=total_events_colab_uh(international_cuba),
            ),
            dict(
                Tipo="Eventos Nacionales",
                Total=total_events(national_events),
                Principal=total_events_first_author(national_events),
                Colab=total_events_colab_uh(national_events),
            ),
            dict(
                Tipo="Actividades Cientítficas",
                Total=total_events(activities),
                Principal=total_events_first_author(activities),
                Colab=total_events_colab_uh(activities),
            ),
        ]
    )

    if international_events:
        yield "#### 💠 Internacionales"

    for (venue, location), events in international_events.items():
        yield f"_{venue}_, {location}: **{len(events)} ponencia(s)**"

    if international_cuba:
        yield "#### 💠 Internacionales en Cuba"

    for (venue, location), events in international_cuba.items():
        yield f"_{venue}_, {location}: **{len(events)} ponencia(s)**"

    if national_events:
        yield "#### 💠 Nacionales"

    for (venue, location), events in national_events.items():
        yield f"_{venue}_, {location}: **{len(events)} ponencia(s)**"

    if activities:
        yield "#### 💠 Actividades Científicas"

    for (venue, location), events in activities.items():
        yield f"_{venue}_, {location}: **{len(events)} ponencia(s)**"

    yield "### ⚗️ Proyectos"

    projects = Project.all()
    projects.sort(key=lambda p: (p.project_type, p.title))

    df = (
        pd.DataFrame(
            [
                dict(Proyecto=p.title, Estado=p.status, Tipo=p.project_type)
                for p in projects
            ]
        )
        .groupby(["Tipo", "Estado"])
        .count()
        .reset_index()
        .set_index("Tipo")
    )

    yield df

    yield pd.DataFrame(
        [
            dict(
                Proyecto=p.title,
                Fondos=p.funds_total,
                Efectuado=p.funds_collected,
                Financia="; ".join(p.funding),
                Resto=p.funds_total - p.funds_collected,
            )
            for p in projects
        ]
    ).set_index(["Proyecto", "Financia"])

    for project in projects:
        yield project.format()

    yield "### 👥 Personal"

    people = set(Person.own())

    yield pd.DataFrame(
        [dict(Persona=p.name, Grado=p.scientific_grade) for p in people]
    ).groupby("Grado").count()

    people_with_papers = (
        set(
            person
            for paper in papers + presentations + books + chapters + events
            for person in paper.authors
        )
        & people
    )

    st.write(f"**Personal con publicaciones:** {len(people_with_papers)} ({len(people_with_papers) * 100 / len(people):0.1f}%)")

    people_in_projects = (
        set(
            person
            for project in projects
            for person in [project.head] + project.members
        )
        & people
    )

    st.write(f"**Personal con proyectos:** {len(people_in_projects)} ({len(people_in_projects) * 100 / len(people):0.1f}%)")

    st.write(f"**Personal en ambos:** {len(people_in_projects & people_with_papers)}")

    people_in_awards = (
        set(
            person
            for award in Award.all()
            for person in award.participants
        )
        & people
    )

    st.write(f"**Personal con premios:** {len(people_in_awards)} ({len(people_in_awards) * 100 / len(people):0.1f}%)")
