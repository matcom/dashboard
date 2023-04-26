import auth
import streamlit as st
from models.data_models.person_model import Person
from page_router import PageRouter


def profile_page(router: PageRouter, **params):
    st.set_page_config(page_title="MatCom Dashboard - Perfil")
    router.page_header("Perfil")

    if not auth.is_user_logged():
        st.subheader("No estás logeado")
        st.stop()

    email = st.session_state.get("user", "angela@matcom.uh.cu")

    persons = Person.find(emails=email)
    if not persons:
        st.error("Tu cuenta no está registrada")
        st.stop()
    
    person = persons[0]

    c1, c2 = st.columns([1, 5])
    with c1:
        grades = ["Lic.", "Mtr.", "Dr."]
        person.scientific_grade = st.selectbox(
            "Grado",
            grades,
            index=grades.index(person.scientific_grade)
            if person.scientific_grade in grades
            else 0,
        )

    with c2:
        person.name = st.text_input("Nombre", value=person.name)

    st.text_input("Correo principal", value=email, disabled=True)
    emails = st.text_input(
        "Correos adicionales",
        value=";".join([e for e in person.emails if e != email]),
        placeholder="Separados por ; (ej. foo@matcom.uh.cu;bar@matcom.uh.cu)",
    ).split(";")
    person.emails = [email for email in emails if email] + [email]

    person.institution = st.text_input(
        "Institución",
        placeholder="e.j. Universidad de la Habana",
        value=person.institution,
    )
    if person.institution == "Universidad de la Habana":
        person.faculty = st.text_input(
            "Facultad", placeholder="e.j. Matcom", value=person.faculty
        )
        person.department = st.text_input(
            "Departamento",
            placeholder="e.j. Departamento de Redes",
            value=person.department,
        )

    person.orcid = st.text_input(
        "ORCID", placeholder="0000-0000-0000-0000", value=person.orcid
    )

    if st.button("**Guardar**", disabled=(not person.name or not person.emails)):
        person.save()
