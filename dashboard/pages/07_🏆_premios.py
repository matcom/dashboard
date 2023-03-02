from uuid import uuid4

import auth
import streamlit as st
from models import Award, Person

st.set_page_config(
    page_title="MatCom Dashboard - Premios", page_icon="🏆", layout="wide"
)


st.title("🏆 Premios")

list_view, create_view, edit_view = st.tabs(
    ["🏆 Listado de premios", "⭐ Crear nuevo premio", "📝 Editar premio"]
)


def save_award(award: Award, prefix):
    award.save()

    for key in st.session_state.keys():
        if key.startswith(prefix):
            del st.session_state[key]

    del st.session_state.current_award
    st.success("Premio guardado con éxito")


with create_view:
    if auth.is_user_logged():
        if "current_award" in st.session_state:
            key = st.session_state.current_award
        else:
            key = str(uuid4())
            st.session_state.current_award = key

        award = Award.create(key=key)

        if award is not None:
            st.button("💾 Guardar", on_click=save_award, args=(award, key))
        else:
            st.warning("⚠️ Complete la información obligatoria, marcada con 🔹")
    else:
        st.error("Acceso de solo lectura. Vaya a la página principal para loguearse.")


with list_view:
    awards = Award.all()
    awards.sort(key=lambda a: (-a.date.year, a.name))

    for award in awards:
        text = [f"🏆 **{award.name}**."]

        if award.title:
            text.append(f"Por _{award.title}_.")

        for person in award.participants:
            fmt = person.name

            if person.orcid:
                fmt = f"[{fmt}](https://orcid.org/{person.orcid})"

            if person.institution == "Universidad de La Habana":
                fmt = f"**{fmt}**"

            text.append(fmt.format(person.name) + ", ")

        text.append(f"{award.institution}, {award.date.year}.")

        st.write(" ".join(text))
