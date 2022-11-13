import streamlit as st
import datetime

from models import Person
from reports import personal_report, research_balance


st.set_page_config(
    page_title="MatCom Dashboard - Reportes", page_icon="📈", layout="wide"
)


balance, posgrado, personal, group = st.tabs(["⚗️ Balance de Investigación", "📚 Balance de Posgrado", "👤 Reporte Individual", "👥 Reporte Colectivo"])

people = Person.own()
people.sort(key=lambda p: p.name)


with balance:
    today = datetime.date.today()

    left, right = st.columns(2)
    start_date = left.date_input("Fecha de inicio", value=today - datetime.timedelta(days=365))
    end_date = right.date_input("Fecha de fin", value=today)

    with st.spinner("Generando balance..."):
        for line in research_balance(start_date, end_date):
            st.write(line)


with personal:
    person = st.selectbox("Seleccione la persona", ['-'] + people)

    if person != '-':
        with st.spinner("Generando reporte..."):
            for line in personal_report(person):
                st.write(line)
