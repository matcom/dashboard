import streamlit as st

st.set_page_config(page_title="MatCom Dashboard", page_icon="⭐", layout="wide")

with open("/src/dashboard/main.md") as fp:
    st.write(fp.read())
