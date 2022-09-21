import streamlit as st
import pandas as pd
import altair
from models import Classes, Subject, Person


st.set_page_config(
    page_title="MatCom Dashboard - Docencia", page_icon="📝", layout="wide"
)


subjects_tab, classes_tab = st.tabs(["Asignaturas", "Clases"])

with subjects_tab:
    with st.expander("⭐ Crear nueva asignatura"):

        cols = st.columns([2,2,1,1])
        subject = cols[0].text_input("Nombre de la asignatura")
        career = cols[1].selectbox("Carrera", ["Matemática", "Ciencia de la Computación", "Externa"])
        year = cols[2].selectbox("Año", [1,2,3,4], format_func=lambda a: f"Año {a}")
        semester = cols[3].selectbox("Semestre", [1,2], format_func=lambda s: f"Semestre {s}")

        subject = Subject(subject=subject, career=career, year=year, semester=semester)

        if st.button("💾 Salvar asignatura"):
            subject.save()

    st.write("#### 📝 Listado de asignaturas")

    subjects = []

    for subject in sorted(Subject.all(), key=lambda s: (s.year, s.semester, s.subject)):
        subjects.append(subject.encode())

    st.dataframe(subjects)


with classes_tab:
    with st.expander("📝 Crear nueva entrada"):
        cols = st.columns([2,2,1,1])

        subject = cols[0].selectbox("Asignatura", sorted(Subject.all(), key=lambda s: s.subject))
        professor = cols[1].selectbox("Profesor", sorted(Person.all(), key=lambda s: s.name))
        lecture_hours = cols[2].number_input("Horas de conferencia (semanal)", min_value=0, value=0)
        practice_hours = cols[3].number_input("Horas de prácticas (semanal)", min_value=0, value=0)

        classes = Classes(subject=subject, professor=professor, lecture_hours=lecture_hours, practice_hours=practice_hours)

        if lecture_hours == 0 and practice_hours == 0:
            st.error("Al menos debe tener horas de conferencias o prácticas")
        elif st.button("💾 Guardar entrada"):
            classes.save()

    st.write("#### ⏳ Carga docente")

    data = []

    for entry in Classes.all():
        data.append(dict(subject=entry.subject.subject, professor=entry.professor.name, hours=entry.practice_hours + entry.lecture_hours))

    data = pd.DataFrame(data)

    st.write(altair.Chart(data).mark_bar().encode(
        x=altair.X("sum(hours)", title="Horas semanales"),
        y=altair.Y("professor", title="Profesor"),
        color=altair.Color("subject", title="Asignatura"),
        tooltip=["subject", "hours"]
    ))