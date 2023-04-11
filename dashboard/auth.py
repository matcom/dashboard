import os

import extra_streamlit_components as stx
import streamlit as st
from itsdangerous.exc import BadData
from itsdangerous.url_safe import URLSafeTimedSerializer
from tools import send_from_template

COOKIE = "Dashboard-AuthToken"


def in_admin_session() -> bool:
    if st.secrets.get("skip_auth", False):
        return True
    return is_user_logged() and st.session_state["user"] == os.environ["ADMIN"]


def is_user_logged() -> bool:
    if st.secrets.get("skip_auth", False):
        return True
    return st.session_state.get("user", None) is not None


def login(user):
    st.session_state.user = user
    st.experimental_set_query_params()
    st.info(f"Bienvenido **{user}**")
    set_token_in_cookies(generate_signin_token(user))
    st.button("🚪 Cerrar sesión", on_click=logout)
    return user


def logout():
    del st.session_state["user"]
    delete_token_in_cookies()


def authenticate():
    if st.secrets.get("skip_auth", False):
        st.info(
            "Bienvenido developer.\n\n_NOTA: el botón de cerrar sesión existe solo "
            "para mostrar un layout similar al de un user loggeado_"
        )
        st.button("🚪 Cerrar sesión")
        return True

    token = st.experimental_get_query_params().get("token")

    if token:
        credentials = verify_token(token[0])

        if credentials is not None:
            return login(*credentials)
        st.error("El token de autenticación es inválido. Vuelva a intentarlo.")
    elif "user" in st.session_state:
        user = st.session_state.user
        return login(user)
    else:
        token = get_token_from_cookies()
        credentials = verify_token(token)

        if credentials is not None:
            return login(*credentials)

    email = st.text_input("Introduza su dirección correo electrónico")

    if email:
        if not check_email(email):
            st.error(
                "El correo electrónico debe ser de la Universidad de la "
                "habana y no puede ser de un estudiante (e.j. "
                "**usuario@matcom.uh.cu**)."
            )
            return False

        st.info(
            f"""
            Haga click en el botón siguiente y le enviaremos a **{email}**
            un enlace de autenticación que le permitirá acceder a la
            plataforma
            """
        )

        if st.button("📧 Enviar enlace de autenticación"):
            token = generate_signin_token(email)
            try:
                send_from_template(
                    "login",
                    email,
                    faculty="Matcom",  # Change in the future for allowing any faculty
                    link=f"http://localhost:8501?page=home/signup&token={token}",
                )
                st.success(
                    "El enlace de autenticación ha sido enviado. Verifique su correo."
                )
            except Exception as e:
                st.error("**ERROR**: " + str(e))

                with st.expander("Ver detalles del error"):
                    st.exception(e)


def check_email(email: str) -> bool:
    if email == os.getenv("ADMIN"):
        return True

    return email.endswith("uh.cu") and "estudiantes" not in email


def generate_signin_token(user):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
    return serializer.dumps(f"{user}")


def verify_token(token):
    if not token:
        return None

    serializer = URLSafeTimedSerializer(os.getenv("SECRET"))

    try:
        return serializer.loads(token, max_age=3600).split("::")
    except BadData:
        return None


def _get_cookie_manager():
    if "cookie_manager" in st.session_state:
        return st.session_state.cookie_manager

    cookie_manager = stx.CookieManager()
    st.session_state.cookie_manager = cookie_manager
    return cookie_manager


def get_token_from_cookies():
    cookie_manager = _get_cookie_manager()
    cookie_manager.get_all()
    auth_token = cookie_manager.get(COOKIE)
    return auth_token


def set_token_in_cookies(token):
    cookie_manager = _get_cookie_manager()
    cookie_manager.set(COOKIE, token, expires_at=None)


def delete_token_in_cookies():
    cookie_manager = _get_cookie_manager()
    cookie_manager.delete(COOKIE)
