import json
from io import StringIO

import altair
import auth
import pandas as pd
import streamlit as st
from models.custom_model import collection_names
from models.db_handler import DBHandler

if not auth.in_admin_session():
    st.stop()

st.set_page_config(
    page_title="MatCom Dashboard - Administración", page_icon="🛠", layout="wide"
)

st.title("🛠 Administración")
(database,) = st.tabs(["🗄️ Base de datos"])


def format_bytes(n_bytes: int) -> str:
    if n_bytes > 1e6:
        return f"{round(n_bytes * 1e-6, 2)} MB"
    if n_bytes > 1e3:
        return f"{round(n_bytes * 1e-3, 2)} kB"
    return f"{n_bytes} B"


with database:
    general_stats, tools_exp, tools_imp, tools_del = st.columns([2, 1, 1, 1])
    stats = {model: model.stats() for model in collection_names.keys()}

    with general_stats:
        st.title("📊 Estadísticas generales")

        total_entries = sum(stat["count"] for stat in stats.values())

        total_size = sum(stat["size"] for stat in stats.values())
        st.write(
            f"""
                 - <font size=5>Cantidad de modelos:</font>  &nbsp;&nbsp;&nbsp;**<font size=5>{len(stats)}</font>**
                 - <font size=5>Cantidad de entradas:</font>  &nbsp;&nbsp;&nbsp;**<font size=5>{total_entries}</font>**
                 - <font size=5>Tamaño total:</font>  &nbsp;&nbsp;&nbsp;**<font size=5>{format_bytes(total_size)}</font>**
        """,
            unsafe_allow_html=True,
        )

    with tools_exp:
        st.title("Opciones")
        st.write("#### 📤 Exportar")

        # Allow more formats in future
        # file_format = st.radio("Formato", ["csv", "json"], horizontal=True, key=1)
        file_format = "json"

        if st.button(f"Convertir base de datos a {file_format}"):
            data = DBHandler.export_json()
            st.download_button(
                label="Descargar",
                file_name=f"dashoboard_database.{file_format}",
                data=data,
                mime=f"text/{file_format}",
            )

    with tools_imp:
        st.title("&nbsp;")
        st.write("#### 📥 Importar")
        db_data = st.file_uploader("Importar")
        if db_data is not None:
            stringio = StringIO(db_data.getvalue().decode("utf-8"))
            if st.button("Cargar base de datos"):
                DBHandler.import_json(json.load(stringio))

    with tools_del:
        st.title("&nbsp;")
        st.write(
            "#### <font color=#dd5050>🗑️ Borrar base de datos</font>",
            unsafe_allow_html=True,
        )
        with st.expander(
            "Estoy seguro de que quiero borrar la base de datos",
        ):
            if st.button("⚠️ BORRAR BASE DE DATOS"):
                DBHandler.drop_all()

    if total_entries == 0:
        st.stop()

    st.title("Estadísticas por modelos")
    count_col, size_col = st.columns(2)

    with count_col:
        st.write(
            "<h2 style='text-align: center;'>Cantidad de entradas</h2>",
            unsafe_allow_html=True,
        )
        entry_count = []
        for model, stat in stats.items():
            entry_count.append(
                dict(
                    model_name=model.__name__,
                    count=stat["count"],
                )
            )

        data = pd.DataFrame(entry_count)
        st.altair_chart(
            altair.Chart(data)
            .mark_bar()
            .encode(
                x=altair.X("count", title="Cantidad"),
                y=altair.Y("model_name", title="Modelo"),
            ),
            use_container_width=True,
        )

    with size_col:
        st.write(
            "<h2 style='text-align: center;'>Tamaño</h2>",
            unsafe_allow_html=True,
        )
        coll_size = []
        for model, stat in stats.items():
            coll_size.append(
                dict(
                    model_name=model.__name__,
                    percent=round(stat["size"] * 100 / total_size, 2),
                    size=format_bytes(stat["size"]),
                )
            )

        data = pd.DataFrame(coll_size)
        st.altair_chart(
            altair.Chart(data)
            .mark_arc(innerRadius=90)
            .encode(
                theta=altair.Theta(field="percent", type="quantitative"),
                color=altair.Color(field="model_name", type="nominal"),
                tooltip=["model_name", "percent", "size"],
            ),
            use_container_width=True,
        )
