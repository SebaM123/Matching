import streamlit as st

st.set_page_config(page_title="Matching Lab", page_icon="🔀", layout="wide")

st.title("🔀 Matching Lab")
st.markdown(
    """
Portal de estudio y simulación de **teoría de matching y market design**.

Definí un problema (por ejemplo, estudiantes y colegios con sus
preferencias), corré distintos mecanismos de asignación, y explorá sus
propiedades — estabilidad, optimalidad, incentivos a decir la verdad.

Elegí un mecanismo en el menú de la izquierda para empezar.

**Disponible hoy:**
- Deferred Acceptance (Gale-Shapley)

**Planeado:**
- Boston / Immediate Acceptance
- Top Trading Cycles (TTC)
- Serial Dictatorship
- Kidney Exchange
"""
)
