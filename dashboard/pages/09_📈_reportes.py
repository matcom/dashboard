import streamlit as st
from models import Person
from reports import personal_report


st.set_page_config(
    page_title="MatCom Dashboard - Reportes", page_icon="📈", layout="wide"
)


balance, posgrado, personal, group = st.tabs(["⚗️ Balance de Investigación", "📚 Balance de Posgrado", "👤 Reporte Individual", "👥 Reporte Colectivo"])

people = Person.own()
people.sort(key=lambda p: p.name)


with personal:
    person = st.selectbox("Seleccione la persona", ['-'] + people)

    if person != '-':
        with st.spinner("Generando reporte..."):
            st.write(personal_report(person))
