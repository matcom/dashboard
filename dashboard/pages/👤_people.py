import streamlit as st
from models import Person

st.set_page_config(
    page_title="MatCom Dashboard - Personal", page_icon="👤", layout="wide"
)


with st.expander("👤 Crear nueva entrada"):
    name = st.text_input("Nombre")
    institution = st.selectbox("Institución", ["Universidad de La Habana", "Externo"])

    if institution == "Externo":
        institution = st.text_input("Nombre de la institución")
        faculty = None
        department = None
    else:
        faculty = st.selectbox("Facultad", ["Matemática y Computación", "Otra"])

        if faculty == "Otra":
            faculty = st.text_input("Nombre de la facultad")
            department = st.text_input("Departamento")
        else:
            department = st.selectbox(
                "Departamento", ["Computación", "Matemática", "Matemática Aplicada"]
            )

    scientific_grade = st.selectbox("Grado científico", ["Licenciado", "Ingeniero", "Máster en Ciencias", "Doctor en Ciencias"])
    academic_grade = st.selectbox("Grado académico", ["Adiestrado", "Instructor", "Asistente", "Auxiliar", "Titular"])

    person = Person(
        name=name, institution=institution, faculty=faculty, department=department, scientific_grade=scientific_grade, academic_grade=academic_grade
    )

    if person.name in [p.name for p in Person.all()]:
        st.error("Ya existe una persona con ese nombre.")

    elif st.button("💾 Salvar entrada"):
        person.save()
        st.success("Entrada salvada con éxito.")


people = []

st.write("#### Listado")
for person in sorted(Person.all(), key=lambda s: s.name):
    people.append(person.encode())

st.dataframe(people)
