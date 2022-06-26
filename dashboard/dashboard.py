from typing import Dict
import pandas as pd
import streamlit as st


st.set_page_config(page_title="MatCom Dashboard", page_icon=":star", layout="wide")


@st.experimental_memo
def load_data() -> Dict[str, pd.DataFrame]:
    return pd.read_excel(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1njbIUsTc9nN-TIC9QpDUY0L7Az0aRZ88NznYajzpUBaKA5vf5iaRg98HkOQHU3x9Kpqm7VLLpGp0/pub?output=xlsx",
        sheet_name=None,
    )


data = load_data()


@st.experimental_memo
def convert_to_csv(sheet: str):
    return data[sheet].to_csv().encode("utf8")


with st.sidebar:
    sheet = st.selectbox("Colección", data)

    st.download_button(
        "Descargar",
        data=convert_to_csv(sheet),
        file_name=f"{sheet}.csv",
        mime="text/csv",
    )

with st.expander(f"Ver datos: {sheet}", False):
    st.dataframe(data[sheet])
