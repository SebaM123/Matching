import streamlit as st

st.set_page_config(page_title="Matching Lab", page_icon="🔀", layout="wide")

st.title("🔀 Matching Lab")
st.markdown(
    """
Portal de estudio y simulación de **teoría de matching y market design**.

Definí un problema (por ejemplo, estudiantes y colegios con sus
preferencias), corré distintos mecanismos de asignación, y explorá sus
propiedades — estabilidad, optimalidad, incentivos a decir la verdad.

Elegí una sección en el menú de la izquierda para empezar. Si es tu primera
vez, arrancá por **Motivación** y **Definiciones** antes de meterte en los
mecanismos.

**Disponible hoy:**
- 🌱 Motivación — por qué existe el diseño de mercado
- 📚 Definiciones — glosario de conceptos
- Deferred Acceptance (Gale-Shapley)
- Boston / Immediate Acceptance
- Top Trading Cycles (TTC)

**Planeado:**
- Serial Dictatorship
- Kidney Exchange
- Simulación masiva / evaluación de mecanismos a escala
"""
)
