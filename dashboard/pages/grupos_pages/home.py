import auth
import streamlit as st
from models import Person, ResearchGroup
from page_router import PageRouter


def grupos_page(router: PageRouter, **params):
    st.set_page_config(page_title="MatCom Dashboard - Grupos de Investigación",page_icon="👥",layout="wide",)
    st.title("👥 Grupos de Investigación")

    list_view, create_view = st.tabs(["👥 Listado de grupos", "📝 Crear o editar"])


    groups = ResearchGroup.all()
    people = Person.all()
    people.sort(key=lambda p: p.name)


    with create_view:
        if auth.is_user_logged():
            if (
                st.radio(
                    "Tipo de entrada",
                    ["⭐ Nueva entrada", "📝 Editar"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                == "📝 Editar"
            ):
                group = st.selectbox(
                    "Seleccione un grupo a modificar",
                    sorted(groups, key=lambda t: t.name),
                    format_func=lambda t: t.name,
                )
            else:
                group = ResearchGroup(name="", members=[], collaborators=[], keywords=[])

            if group:
                group.name = st.text_input("Nombre", key="group_name", value=group.name)
                group.members = st.multiselect(
                    "Miembros (permanentes)",
                    key="group_members",
                    options=people,
                    default=group.members,
                )
                group.head = st.selectbox(
                    "Coordinador",
                    options=group.members,
                    key="group_head",
                    index=group.members.index(group.head) if group.head else 0,
                )
                group.collaborators = st.multiselect(
                    "Colaboradores (internos o externos)",
                    key="group_collaborators",
                    options=people,
                    default=group.collaborators,
                )
                group.keywords = [
                    s.strip()
                    for s in st.text_input(
                        "Líneas de investigación (separadas por ;)",
                        value="; ".join(group.keywords),
                    ).split(";")
                ]

                if st.button("💾 Guardar"):
                    group.save()
                    st.success("Información guardad con éxito")
        else:
            st.error("Acceso de solo lectura. Vaya a la página principal para loguearse.")

    with list_view:
        for group in groups:
            with st.expander(f"{group.name} ({len(group.members)} miembros)"):
                left, mid, right = st.columns([2, 1, 1])

                with left:
                    st.write(f"#### {group.name}")
                    st.write("**Líneas de investigación:** " + "; ".join(group.keywords))
                    st.write(f"**Coordinador**: {group.head.name}")

                with mid:
                    st.write(
                        "**Miembros:**\n"
                        + "\n".join(
                            f"- {p.name}"
                            for p in sorted(group.members, key=lambda p: p.name)
                        )
                    )

                with right:
                    if group.collaborators:
                        st.write(
                            "**Colaboradores:**\n"
                            + "\n".join(
                                f"- {p.name}"
                                for p in sorted(group.collaborators, key=lambda p: p.name)
                            )
                        )
