import os

import extra_streamlit_components as stx
import streamlit as st
from itsdangerous.exc import BadData
from itsdangerous.url_safe import URLSafeTimedSerializer
from models.data_models.person_model import Person
from tools import send_from_template

COOKIE = "Dashboard-AuthToken"


def in_admin_session() -> bool:
    if st.secrets.get("skip_auth", False):
        return True
    return is_user_logged() and st.session_state["user"] == os.environ["ADMIN"]


def is_user_logged() -> bool:
    return st.session_state.get("user", None) is not None


def login(user):
    st.session_state.user = user
    _load_user_model()
    st.experimental_set_query_params()
    set_token_in_cookies(generate_signin_token(user))
    return user


def _load_user_model():
    email = st.session_state.user
    st.session_state.user_model = Person.find_one(emails=email)


def current_user_model() -> Person:
    assert is_user_logged()

    if "user_model" in st.session_state:
        user: Person = st.session_state.user_model
        if user.emails[0] != st.session_state.user:
            _load_user_model()
    else:
        _load_user_model()

    return st.session_state.user_model


def logout():
    del st.session_state["user"]
    delete_token_in_cookies()


def try_login_using_cookies():
    token = get_token_from_cookies()
    credentials = verify_token(token)
    if credentials is not None:
        return login(*credentials)
    return None

def authenticate():
    if st.secrets.get("skip_auth", False):
        login(os.environ["ADMIN"])
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
        user = try_login_using_cookies()
        if user is not None:
            return user

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
