import os

import auth
import streamlit as st
from page_router import PageRouter, Route


def dashboard(router: PageRouter, **params):
    st.set_page_config(page_title="MatCom Dashboard", layout="wide")
    st.title("⭐ Bienvenido al Dashboard de MatCom")

    left, right = st.columns(2)

    with right:
        if not auth.is_user_logged():
            st.info(
                """
                Si usted es claustro de la facultad y desea modificar los datos,
                introduzca la contraseña correspondiente. De lo contrario, puede leer
                los datos pero no modificar.

                Si usted cree que debería tener acceso, contacte con
                [@apiad](https://t.me/apiad) en Telegram."""
            )

        auth.authenticate()

    with left:
        with open("/src/dashboard/main.md", encoding="utf-8") as fp:
            st.write(fp.read())

page_router = PageRouter(
    "dashboard",
    Route(
        url="home",
        builder=dashboard,
    )
)

page_router.start()
