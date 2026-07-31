import streamlit as st

st.set_page_config(page_title="Matching Lab", page_icon="🔀", layout="wide")

st.title("🔀 Matching Lab")
st.markdown(
    """
Portal de estudio y simulación de **teoría de matching y market design**.

Define un problema (por ejemplo, estudiantes y colegios con sus
preferencias), ejecuta distintos mecanismos de asignación, y explora sus
propiedades — estabilidad, optimalidad, incentivos a decir la verdad.

Elige una sección en el menú de la izquierda para empezar. Si es tu primera
vez, comienza por **Motivación** y **Definiciones** antes de meterte en los
mecanismos.

**Disponible hoy:**
- 🌱 Motivación — por qué existe el diseño de mercado
- 📚 Definiciones — glosario de conceptos
- Deferred Acceptance (Gale-Shapley)
- Boston / Immediate Acceptance
- Top Trading Cycles (TTC)
- Serial Dictatorship
- Kidney Exchange
- House Allocation (mercado de casas, Shapley-Scarf)

**Planeado:**
- Comparador (todos los mecanismos sobre el mismo problema)
- Manipulación interactiva (jugar a mentir tus preferencias)
- Simulación masiva / evaluación de mecanismos a escala
"""
)
