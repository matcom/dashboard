import streamlit as st

from typing import List
from models import Person, JournalPaper, ConferencePresentation, Book, BookChapter


def personal_report(person: Person):
    lines = []

    lines.append("### 👤 Información personal\n")
    lines.append(f"- **Institución**: {person.institution}")
    lines.append(f"- **Facultad**: {person.faculty}")
    lines.append(f"- **Departamento**: {person.department}")
    lines.append(f"- **Grado científico:** {person.scientific_grade}")
    lines.append(f"- **Categoría docente:** {person.academic_grade}")

    if person.orcid:
        lines.append(f"- **Perfil ORCID:** [{person.orcid}](https://orcid.org/{person.orcid})")

    lines.append("### 📚 Publicaciones\n")

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


    return "\n".join(lines)
