import streamlit as st
from page_router import PageRouter


def expertos_page(router: PageRouter, **params):
    st.set_page_config(page_title="MatCom Dashboard - Consejos Expertos", page_icon="🪑", layout="wide")
    router.page_header("Expertos")

