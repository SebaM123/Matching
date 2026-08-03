import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.boston import boston_mechanism
from mechanisms.deferred_acceptance import deferred_acceptance
from mechanisms.serial_dictatorship import serial_dictatorship
from mechanisms.ttc import top_trading_cycles

st.set_page_config(page_title="Manipulación", page_icon="🎭", layout="wide")
st.title("🎭 ¿Conviene mentir? Manipulación interactiva")

st.markdown(
    "Elige un estudiante **focal** y compara qué le conviene reportar: "
    "sus preferencias **verdaderas**, o una lista **manipulada**. Todos "
    "los demás estudiantes reportan sus preferencias reales. El "
    "simulador corre el mecanismo dos veces y te dice si mentir te "
    "convino, evaluado según tus preferencias verdaderas."
)


def parse_pref_list(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


mechanism = st.radio(
    "Mecanismo",
    options=["Deferred Acceptance", "Boston", "Top Trading Cycles", "Serial Dictatorship"],
    horizontal=True,
)

n_students = st.number_input("Cantidad de estudiantes", min_value=2, max_value=8, value=3)
n_schools = st.number_input("Cantidad de colegios", min_value=1, max_value=8, value=3)

students = [f"E{i+1}" for i in range(n_students)]
schools = [f"C{i+1}" for i in range(n_schools)]

default_true_prefs = {
    "E1": "C1, C2, C3",
    "E2": "C1, C2, C3",
    "E3": "C2, C1, C3",
}
default_school_prefs = {
    "C1": "E1, E2, E3",
    "C2": "E1, E2, E3",
    "C3": "E1, E2, E3",
}

st.subheader("Cupos por colegio")
capacities = {}
cap_cols = st.columns(len(schools))
for i, c in enumerate(schools):
    capacities[c] = cap_cols[i].number_input(
        f"Cupo {c}", min_value=1, max_value=n_students, value=1, key=f"man_cap_{c}"
    )

st.subheader("Preferencias verdaderas de cada estudiante")
true_prefs = {}
for s in students:
    default = default_true_prefs.get(s, ", ".join(schools))
    raw = st.text_input(f"{s}:", value=default, key=f"man_true_{s}")
    true_prefs[s] = parse_pref_list(raw)

school_prefs = {}
sd_order: list[str] = students
if mechanism == "Serial Dictatorship":
    st.subheader("Orden de prioridad para Serial Dictatorship")
    order_raw = st.text_input("Orden:", value=", ".join(students), key="man_sd_order")
    sd_order = parse_pref_list(order_raw)
else:
    st.subheader("Prioridad de los colegios (estudiante de mayor prioridad primero)")
    for c in schools:
        default = default_school_prefs.get(c, ", ".join(students))
        raw = st.text_input(f"{c}:", value=default, key=f"man_school_{c}")
        school_prefs[c] = parse_pref_list(raw)

st.subheader("El experimento")
default_focal_index = 1 if len(students) > 1 else 0
focal = st.selectbox(
    "Estudiante focal (el que va a decidir si miente)",
    options=students,
    index=default_focal_index,
)
default_manip = default_true_prefs.get(focal, ", ".join(schools))
if focal == "E2":
    default_manip = "C2, C1, C3"
manip_raw = st.text_input(
    f"Preferencia reportada por {focal} (puede ser distinta de la real):",
    value=default_manip,
    key="man_manip_pref",
)
manip_pref = parse_pref_list(manip_raw)


def run_mechanism(student_prefs: dict[str, list[str]]) -> dict[str, str | None]:
    if mechanism == "Deferred Acceptance":
        return deferred_acceptance(student_prefs, school_prefs, capacities, proposing="students").matching
    if mechanism == "Boston":
        return boston_mechanism(student_prefs, school_prefs, capacities).matching
    if mechanism == "Top Trading Cycles":
        return top_trading_cycles(student_prefs, school_prefs, capacities).matching
    return serial_dictatorship(sd_order, student_prefs, capacities).matching


def rank_of(student: str, school: str | None) -> int | None:
    prefs = true_prefs[student]
    if school is None:
        return None
    return prefs.index(school) if school in prefs else len(prefs)


if st.button("▶ Comparar honestidad vs. manipulación", type="primary"):
    manipulated_prefs = dict(true_prefs)
    manipulated_prefs[focal] = manip_pref

    honest_matching = run_mechanism(true_prefs)
    manip_matching = run_mechanism(manipulated_prefs)

    honest_school = honest_matching.get(focal)
    manip_school = manip_matching.get(focal)
    honest_rank = rank_of(focal, honest_school)
    manip_rank = rank_of(focal, manip_school)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### Si {focal} es honesto")
        st.write(f"Reporta: {', '.join(true_prefs[focal])}")
        st.write(f"Consigue: **{honest_school}**")
        st.write(f"Posición en su ranking verdadero: **{honest_rank}** (0 = su favorito)")
    with col2:
        st.markdown(f"### Si {focal} reporta {', '.join(manip_pref)}")
        st.write(f"Reporta: {', '.join(manip_pref)}")
        st.write(f"Consigue: **{manip_school}**")
        st.write(f"Posición en su ranking verdadero: **{manip_rank}** (0 = su favorito)")

    st.subheader("Veredicto")
    if manip_rank is None or honest_rank is None:
        st.warning("Alguno de los dos escenarios deja a este estudiante sin colegio asignado.")
    elif manip_rank < honest_rank:
        st.error(
            f"🎭 A {focal} **le convino mentir**: consiguió un colegio mejor (según sus "
            f"preferencias verdaderas) reportando algo distinto de lo que realmente prefiere."
        )
    elif manip_rank > honest_rank:
        st.success(f"✅ Mentir le salió mal a {focal}: terminó peor que siendo honesto.")
    else:
        st.info(f"➖ Da igual: {focal} termina en el mismo lugar en su ranking, mienta o no.")

    with st.expander("Ver el matching completo en ambos escenarios"):
        st.write("**Si todos son honestos:**", honest_matching)
        st.write(f"**Si {focal} reporta distinto:**", manip_matching)

    st.info(
        "Deferred Acceptance (estudiantes proponiendo) y Top Trading Cycles son "
        "strategy-proof: por más que cambies el ejemplo, mentir nunca debería "
        "mejorar el resultado del estudiante focal. En Boston, en cambio, sí "
        "puede convenir — con el ejemplo por defecto, notarás que a E2 le "
        "conviene reportar C2 primero en vez de su verdadero orden."
    )
