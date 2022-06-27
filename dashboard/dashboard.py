from curses.ascii import alt
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


st.markdown(f"### Publicaciones: {len(data['Publicaciones'])}")

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

agg_method = lambda s: f"year({s})"

# with st.sidebar:
#     aggregation = st.selectbox("Modo de agregación", ["Año", "Mes/Año", "Ninguno"])

#     if aggregation == "Año":
#         agg_method = lambda s: f"year({s})"
#     if aggregation == "Mes/Año":
#         agg_method = lambda s: f"yearmonth({s})"
#     if aggregation == "Ninguno":
#         agg_method = lambda s: f"{s}"


pub_chart_dates = (
    altair.Chart(pub_data)
    .mark_bar()
    .encode(
        column=altair.Column(
            agg_method("Fecha de publicación"), type="nominal", title="Período"
        ),
        y=altair.Y("count(Título)", title="Cantidad"),
        color=altair.Color("Tipo de publicación"),
        x=altair.X("Tipo de publicación", title=None, axis=None),
        tooltip=[
            altair.Tooltip("count(Título)", title="Total"),
            altair.Tooltip("Tipo de publicación", title="Tipo"),
            altair.Tooltip(agg_method("Fecha de publicación"), title="Fecha"),
        ],
    )
)

pub_chart_types = (
    altair.Chart(pub_data, title="Publicaciones por tipo")
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

st.altair_chart(pub_chart_dates | pub_chart_types, use_container_width=False)

venues = (
    pub_data[
        pub_data["Tipo de publicación"].isin(
            [
                "Artículo publicado en journal",
                "Artículo publicado en proceeding de congreso",
                "Presentación en congreso (sin artículo)",
            ]
        )
    ]
    .groupby(["Tipo de publicación", "Nombre de la Publicación / Evento"])
    .count()
    .reset_index()
)

st.altair_chart(
    altair.Chart(venues, width=200, title="Top de publicaciones")
    .mark_bar()
    .encode(
        x=altair.X("Título", title="Publicaciones"),
        y=altair.Y("Nombre de la Publicación / Evento"),
        column="Tipo de publicación",
        color="Tipo de publicación",
        tooltip=[
            altair.Tooltip("Nombre de la Publicación / Evento", title="Nombre"),
            altair.Tooltip("Tipo de publicación", title="Tipo"),
            altair.Tooltip("count(Título)", title="Totalr"),
        ],
    )
)


st.markdown(f"### Tesis: {len(data['Tesis'])}")

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


st.markdown(f"### Proyectos: {len(data['Proyectos'])}")

project = data["Proyectos"]
project_by_type = (
    project.groupby("Tipo de proyecto").agg({"Título": "count"}).to_dict()["Título"]
)

cols = st.columns(len(project_by_type))

for (label, count), col in zip(project_by_type.items(), cols):
    with col:
        st.metric(label=label, value=count)

sheet = "Proyectos"

with st.expander(f"Ver datos: {sheet}", False):
    st.dataframe(data[sheet])

    st.download_button(
        "Descargar",
        data=convert_to_csv(sheet),
        file_name=f"{sheet}.csv",
        mime="text/csv",
    )
