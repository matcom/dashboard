import pandas as pd
import streamlit as st


st.set_page_config(page_title="MatCom Dashboard", page_icon=":star", layout="wide")


@st.experimental_memo
def load_data():
    return pd.read_excel(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1njbIUsTc9nN-TIC9QpDUY0L7Az0aRZ88NznYajzpUBaKA5vf5iaRg98HkOQHU3x9Kpqm7VLLpGp0/pub?output=xlsx",
        sheet_name=None,
    )


data = load_data()

st.dataframe(data['Publicaciones'])
