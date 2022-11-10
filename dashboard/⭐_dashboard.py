import streamlit as st
import os


st.set_page_config(page_title="MatCom Dashboard", page_icon="⭐", layout="wide")


st.title("Bienvenido al Dashboard de MatCom")

left, right = st.columns(2)

with right:
    st.info("""
        Si usted es claustro de la facultad y desea modificar los datos, introduzca
        la contraseña correspondiente. De lo contrario, puede leer los datos pero no modificar.

        Si usted cree que debería tener acceso, contacte con [@apiad](https://t.me/apiad) en Telegram.
    """)

    password = st.text_input("Contraseña de acceso", type="password")

    try:
        assert (password == st.secrets["password"])
        st.success("Acceso de modificación")
        st.session_state.write_access = True
    except:
        st.error("Acceso de solo lectura")


with left:
    with open("/src/dashboard/main.md") as fp:
        st.write(fp.read())
