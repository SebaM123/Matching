from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Motivación", page_icon="🌱", layout="wide")
st.title("¿Qué es el diseño de mercado?")

content_path = Path(__file__).resolve().parent.parent / "content" / "motivacion.md"
st.markdown(content_path.read_text(encoding="utf-8"))
