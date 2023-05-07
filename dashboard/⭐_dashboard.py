import os
from difflib import IS_LINE_JUNK

import auth
import streamlit as st
from page_router import PageRouter, Route
from pages.dashboard_pages.registration import registration_page, user_is_registered


def dashboard(router: PageRouter, **params):
    st.set_page_config(page_title="MatCom Dashboard", layout="wide")
    router.page_header("⭐ Bienvenido al Dashboard de MatCom")

    left, right = st.columns(2)

    with right:
        # if not auth.is_user_logged():
        #     st.info(
        #         """
        #         Si usted es claustro de la facultad y desea modificar los datos,
        #         introduzca la contraseña correspondiente. De lo contrario, puede leer
        #         los datos pero no modificar.

        #         Si usted cree que debería tener acceso, contacte con
        #         [@apiad](https://t.me/apiad) en Telegram."""
        #     )

        auth.authenticate()

        if auth.is_user_logged():
            user = st.session_state.user
            st.info(f"Bienvenido **{user}**")
            st.button("🚪 Cerrar sesión", on_click=auth.logout)

    with left:
        with open("/src/dashboard/main.md", encoding="utf-8") as fp:
            st.write(fp.read())


page_router = PageRouter(
    "dashboard",
    Route(
        url="home",
        builder=dashboard,
        subroutes=[
            Route(
                url="signup",
                builder=registration_page,
                redirect=lambda **_: ("home" if auth.is_user_logged() else None),
            )
        ],
    ),
)

page_router.start()
