from typing import Dict

import altair
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


st.markdown("### Publicaciones")

pub_data = data["Publicaciones"]
pub_data_by_type = (
    pub_data.groupby("Tipo de publicación").agg({"Título": "count"}).to_dict()["Título"]
)

cols = st.columns(len(pub_data_by_type))

for (label, count), col in zip(pub_data_by_type.items(), cols):
    with col:
        st.metric(label=label, value=count)

sheet = "Publicaciones"

with st.expander(f"Ver datos: {sheet}", False):
    st.dataframe(data[sheet])

    st.download_button(
        "Descargar",
        data=convert_to_csv(sheet),
        file_name=f"{sheet}.csv",
        mime="text/csv",
    )

with st.sidebar:
    aggregation = st.selectbox("Modo de agregación", ["Año", "Mes/Año", "Ninguno"])

    if aggregation == "Año":
        agg_method = lambda s: f"year({s})"
    if aggregation == "Mes/Año":
        agg_method = lambda s: f"yearmonth({s})"
    if aggregation == "Ninguno":
        agg_method = lambda s: f"{s}"

left, right = st.columns(2)

with left:
    pub_chart_dates = (
        altair.Chart(pub_data)
        .mark_bar()
        .encode(
            x=agg_method("Fecha de publicación"),
            y="count(Título)",
            color="Tipo de publicación",
        )
    )

    st.altair_chart(pub_chart_dates, use_container_width=False)

with right:
    pub_chart_types = (
        altair.Chart(pub_data)
        .mark_arc()
        .encode(
            theta="count(Título)",
            tooltip=[
                altair.Tooltip("count(Título)", title="Total"),
                altair.Tooltip("Tipo de publicación", title="Tipo"),
            ],
            color="Tipo de publicación",
        )
    )

    st.altair_chart(pub_chart_types, use_container_width=False)

st.markdown("### Tesis")

tesis_data = data["Tesis"]
tesis_data_by_type = (
    tesis_data.groupby("Tipo de tesis").agg({"Título": "count"}).to_dict()["Título"]
)

cols = st.columns(len(tesis_data_by_type))

for (label, count), col in zip(tesis_data_by_type.items(), cols):
    with col:
        st.metric(label=label, value=count)

sheet = "Tesis"

with st.expander(f"Ver datos: {sheet}", False):
    st.dataframe(data[sheet])

    st.download_button(
        "Descargar",
        data=convert_to_csv(sheet),
        file_name=f"{sheet}.csv",
        mime="text/csv",
    )
