from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Definiciones", page_icon="📚", layout="wide")
st.title("Glosario de definiciones")

content_path = Path(__file__).resolve().parent.parent / "content" / "definiciones.md"
st.markdown(content_path.read_text(encoding="utf-8"))
