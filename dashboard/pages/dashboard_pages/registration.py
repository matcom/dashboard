import auth
import streamlit as st
from models.data_models.person_model import Person
from page_router import PageRouter


def user_is_registered(email: str):
    return Person.find(emails=email)


def registration_page(router: PageRouter, token: str = None, **params):
    st.set_page_config(page_title="MatCom Dashboard - Registro")

    router.page_header("Registro")


    # Verify token
    email = auth.verify_token(token)
    if email is None:
        st.error("El token de autenticación es inválido. Vuelva a intentarlo.")
        st.stop()

    # Check if user is already registered
    email = email[0]
    if user_is_registered(email):
        auth.login(email)
        router.go("home")

    st.title("👤 Registro")
    person = Person(name="", emails=[email])

    c1, c2 = st.columns([1, 5])
    with c1:
        person.scientific_grade = st.selectbox(
            "Grado científico", ["Lic.", "Máster", "Doctor"]
        )

    with c2:
        person.name = st.text_input("Nombre y apellidos *")
    st.text_input("Correo principal", value=email, disabled=True)
    emails = st.text_input(
        "Correos adicionales",
        placeholder="Separados por ; (ej. foo@matcom.uh.cu;bar@matcom.uh.cu)",
    ).split(";")
    person.emails = [email for email in emails if email] + [email]

    person.institution = st.text_input(
        "Institución", placeholder="e.j. Universidad de la Habana"
    )
    person.faculty = st.text_input("Facultad", placeholder="e.j. Matcom")
    person.department = st.text_input(
        "Departamento", placeholder="e.j. Departamento de Redes"
    )

    person.orcid = st.text_input("ORCID", placeholder="0000-0000-0000-0000")

    st.write("*Los campos marcados con * son obligatorios*")
    if st.button("**Registrarse**", disabled=(not person.name or not person.emails)):
        person.save()
        auth.login(email)
        router.go("home")
