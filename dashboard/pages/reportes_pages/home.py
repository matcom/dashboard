import datetime

import streamlit as st
from models import Person, ResearchGroup
from page_router import PageRouter
from pages.reportes_pages.reports import group_report, personal_report, research_balance
from streamlit.elements import select_slider


def reportes_page(router: PageRouter, **params):
    st.set_page_config(
        page_title="MatCom Dashboard - Reportes", page_icon="📈", layout="wide"
    )
    router.page_header("Reportes")

    balance, posgrado, personal, group = st.tabs(
        [
            "⚗️ Balance de Investigación",
            "📚 Balance de Posgrado",
            "👤 Reporte Individual",
            "👥 Reporte Colectivo",
        ]
    )

    people = Person.own()
    people.sort(key=lambda p: p.name)

    groups = ResearchGroup.all()
    groups.sort(key=lambda g: g.name)

    with balance:
        today = datetime.date.today()

        left, right = st.columns(2)
        start_date = left.date_input(
            "Fecha de inicio", value=today - datetime.timedelta(days=365)
        )
        end_date = right.date_input("Fecha de fin", value=today)

        with st.spinner("Generando balance..."):
            for line in research_balance(start_date, end_date):
                st.write(line)

    with personal:
        person = st.selectbox("Seleccione la persona", people)

        filters = {
            "Infromación personal": "show_personal_info",
            "Publicaciones": "show_papers",
            "Proyectos": "show_projects",
            "Tesis tutoreadas": "show_theses",
            "Clases": "show_classes",
            "Grupos de investigación": "show_research_groups",
            "Premios": "show_awards",
        }
        filter_names = list(filters.keys())
        selections = st.multiselect("Filtros", filter_names, filter_names)
        kwargs = {filters[sel]: True for sel in selections}

        if person is not None and person.name != "":
            with st.spinner("Generando reporte..."):
                for line in personal_report(person, **kwargs):
                    st.write(line)

    with group:
        selected_group = st.selectbox("Seleccione el grupo de investigación", groups)

        filters = {
            "Infromación general": "show_general_info",
            "Publicaciones": "show_papers",
            "Premios": "show_awards",
        }
        filter_names = list(filters.keys())
        selections = st.multiselect("Filtros", filter_names, filter_names)
        kwargs = {filters[sel]: True for sel in selections}

        if selected_group is not None and selected_group.name != "":
            with st.spinner("Generando reporte..."):
                for line in group_report(selected_group, **kwargs):
                    st.write(line)
