import auth
import streamlit as st
from models import ConferencePresentation, Person


def presentations_page(router, **params):
    st.set_page_config(page_title="MatCom Dashboard - Presentaciones", layout="wide")
    router.page_header("📢 Presentaciones")

    year = st.sidebar.selectbox("Año", [2020, 2021, 2022], index=2)

    people = Person.all()
    people.sort(key=lambda p: p.name)

    presentations = [p for p in ConferencePresentation.all() if p.year == year]
    presentations.sort(key=lambda p: p.title)

    if auth.is_user_logged():
        with st.expander("⭐ Nueva presentación / 📝 Editar"):
            if (
                st.radio(
                    "Tipo de presentación",
                    ["⭐ Nueva entrada", "📝 Editar"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                == "📝 Editar"
            ):
                presentation = st.selectbox(
                    "Seleccione una presentación a modificar",
                    presentations,
                    format_func=lambda p: f"{p.title}",
                )
            else:
                presentation = ConferencePresentation(
                    title="", authors=[], venue="", location=""
                )

            presentation.title = st.text_input(
                "Título", key="presentation_title", value=presentation.title
            )
            presentation.authors = st.multiselect(
                "Autores",
                key="presentation_authors",
                options=people,
                default=presentation.authors,
            )

            presentation.venue = st.text_input(
                "Evento", key="presentation_venue", value=presentation.venue
            )
            presentation.location = st.text_input(
                "Lugar", key="presentation_location", value=presentation.location
            )
            types = ["Internacional", "Nacional", "Actividad Científica"]
            presentation.event_type = st.selectbox(
                "Tipo", types, index=types.index(presentation.event_type)
            )
            presentation.year = st.number_input(
                "Año",
                key="presentation_year",
                min_value=2020,
                max_value=2022,
                value=presentation.year,
            )
            presentation.paper = st.checkbox(
                "Tiene publicación en proceedings (seriada)?",
                key="presentation_paper",
                value=presentation.paper,
            )

            if st.button("💾 Guardar presentación"):
                presentation.save()
                st.success("Entrada salvada con éxito.")

    st.write(f"#### 📢 Presentaciones `{len(presentations)}`")

    data = []

    for presentation in presentations:
        st.write(presentation.format())
