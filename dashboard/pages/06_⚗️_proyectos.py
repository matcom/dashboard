import streamlit as st
from uuid import uuid4
from models import Project


st.set_page_config(
    page_title="MatCom Dashboard - Proyectos", page_icon="⚗️", layout="wide"
)


def save_project(project: Project, prefix):
    project.save()

    for key in st.session_state.keys():
        print(key, flush=True)
        if key.startswith(prefix):
            del st.session_state[key]

    del st.session_state.current_project
    print(st.session_state, flush=True)

    st.success("Proyecto guardado con éxito")


st.title("⚗️ Proyectos")

list_view, create_view = st.tabs(["⚗️ Listado de proyectos", "📝 Crear o editar"])


with create_view:
    if "current_project" in st.session_state:
        key = st.session_state.current_project
    else:
        key = str(uuid4())
        st.session_state.current_project = key

    project = Project.create(key=key)

    if project is not None:
        st.button("💾 Guardar", on_click=save_project, args=(project, key))
    else:
        st.warning("⚠️ Complete la información obligatoria, marcada con 🔹")
