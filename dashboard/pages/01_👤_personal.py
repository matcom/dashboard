import streamlit as st
from models import Person
import Levenshtein

st.set_page_config(
    page_title="MatCom Dashboard - Personal", page_icon="👤", layout="wide"
)

people = Person.all()
people.sort(key=lambda p: p.name)

with st.expander("👤 Nueva entrada / Editar"):
    if (
        st.radio("Tipo de entrada", ["⭐ Nueva entrada", "📝 Editar"], horizontal=True)
        == "📝 Editar"
    ):
        person = st.selectbox(
            "Seleccione una entrada a modificar",
            people,
            format_func=lambda p: f"{p.name} ({p.institution})"
        )
    else:
        person = Person(
            name="",
            institution="Universidad de La Habana",
            faculty="Facultad de Matemática y Computación",
            department="",
        )

    person.name = st.text_input("Nombre", key="person_name", value=person.name)

    best = max(people, key=lambda p: Levenshtein.ratio(p.name, person.name))
    ratio = Levenshtein.ratio(best.name, person.name)

    if ratio > 0.5:
        st.warning(f"Verifique si la persona a agregar no es **{best.name}** que ya se encuentra la base de datos.")

    person.institution = st.text_input(
        "Institución", key="person_institution", value=person.institution or ""
    )
    person.faculty = st.text_input(
        "Facultad", key="person_faculty", value=person.faculty or ""
    )
    person.department = st.text_input(
        "Departamento", key="person_department", value=person.department or ""
    )
    grades = ["Licenciado", "Ingeniero", "Máster en Ciencias", "Doctor en Ciencias"]
    person.scientific_grade = st.selectbox(
        "Grado científico",
        grades,
        key="person_scientific_grade",
        index=grades.index(person.scientific_grade),
    )
    grades = ["Ninguno", "Instructor", "Asistente", "Auxiliar", "Titular"]
    person.academic_grade = st.selectbox(
        "Grado académico",
        grades,
        key="person_academic_grade",
        index=grades.index(person.academic_grade),
    )

    person.emails = [s.strip() for s in st.text_input("Email(s) -- Separados por punto y coma (;)", key="person_email", value="; ".join(person.emails)).split(";")]
    person.orcid = st.text_input("ORCID", key="person_orcid", value=person.orcid or "")

    if st.button("💾 Salvar entrada"):
        person.save()
        st.success("Entrada salvada con éxito.")


people_comp = []
people_appl = []
people_math = []
people_uh = []
people_extra = []

people = Person.all()
people.sort(key=lambda s: s.name)

st.write(f"#### 👥 Listado `{len(people)}`")
for person in people:
    if person.institution != "Universidad de La Habana":
        people_extra.append(person)
        if not person.institution:
            person.academic_grade = "Ninguno"

        continue

    if person.faculty != "Matemática y Computación":
        people_uh.append(person)

        continue

    if person.department == "Computación":
        people_comp.append(person)
    elif person.department == "Matemática Aplicada":
        people_appl.append(person)
    else:
        people_math.append(person)

st.write("##### Facultad de Matemática y Computación")

with st.expander(f"MatCom - Computación ({len(people_comp)})"):
    st.table([p.encode() for p in people_comp])

with st.expander(f"MatCom - Matemática Aplicada ({len(people_appl)})"):
    st.table([p.encode() for p in people_appl])

with st.expander(f"MatCom - Matemática ({len(people_math)})"):
    st.table([p.encode() for p in people_math])

st.write("##### Resto")

with st.expander(f"Universidad de La Habana ({len(people_uh)})"):
    st.table([p.encode() for p in people_uh])

with st.expander(f"Externos ({len(people_extra)})"):
    st.table([p.encode() for p in people_extra])
