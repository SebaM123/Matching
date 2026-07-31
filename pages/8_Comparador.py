import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.boston import boston_mechanism
from mechanisms.deferred_acceptance import deferred_acceptance, is_stable
from mechanisms.serial_dictatorship import serial_dictatorship
from mechanisms.ttc import top_trading_cycles

st.set_page_config(page_title="Comparador", page_icon="🔀", layout="wide")
st.title("Comparador de mecanismos")

st.markdown(
    "Carga **un solo problema** (estudiantes, colegios, cupos, "
    "preferencias y prioridades) y compara, sobre exactamente los mismos "
    "datos, el resultado de **Deferred Acceptance, Boston, Top Trading "
    "Cycles y Serial Dictatorship** al mismo tiempo. Kidney Exchange y "
    "House Allocation no entran aquí porque son problemas de otra forma "
    "(no de dos lados con cupos)."
)


def parse_pref_list(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


n_students = st.number_input("Cantidad de estudiantes", min_value=1, max_value=8, value=3)
n_schools = st.number_input("Cantidad de colegios", min_value=1, max_value=8, value=3)

students = [f"E{i+1}" for i in range(n_students)]
schools = [f"C{i+1}" for i in range(n_schools)]

default_student_prefs = {
    "E1": "C1, C2, C3",
    "E2": "C1, C2, C3",
    "E3": "C2, C1, C3",
}
default_school_prefs = {
    "C1": "E3, E1, E2",
    "C2": "E1, E2, E3",
    "C3": "E1, E2, E3",
}

st.subheader("Cupos por colegio")
capacities = {}
cap_cols = st.columns(len(schools))
for i, c in enumerate(schools):
    capacities[c] = cap_cols[i].number_input(
        f"Cupo {c}", min_value=1, max_value=n_students, value=1, key=f"cmp_cap_{c}"
    )

st.subheader("Preferencias de los estudiantes (colegio más preferido primero)")
student_prefs = {}
for s in students:
    default = default_student_prefs.get(s, ", ".join(schools))
    raw = st.text_input(f"{s}:", value=default, key=f"cmp_pref_{s}")
    student_prefs[s] = parse_pref_list(raw)

st.subheader("Prioridad de los colegios (estudiante de mayor prioridad primero)")
school_prefs = {}
for c in schools:
    default = default_school_prefs.get(c, ", ".join(students))
    raw = st.text_input(f"{c}:", value=default, key=f"cmp_pref_{c}")
    school_prefs[c] = parse_pref_list(raw)

st.subheader("Orden de prioridad para Serial Dictatorship")
sd_order_raw = st.text_input("Orden:", value=", ".join(students), key="cmp_sd_order")
sd_order = parse_pref_list(sd_order_raw)


def rank_of(student: str, school: str | None) -> int | None:
    if school is None:
        return None
    prefs = student_prefs[student]
    return prefs.index(school) if school in prefs else len(prefs)


if st.button("▶ Ejecutar todos los mecanismos", type="primary"):
    da = deferred_acceptance(student_prefs, school_prefs, capacities, proposing="students")
    bos = boston_mechanism(student_prefs, school_prefs, capacities)
    ttc = top_trading_cycles(student_prefs, school_prefs, capacities)
    sd = serial_dictatorship(sd_order, student_prefs, capacities)

    mechanisms = [
        ("Deferred Acceptance", da.matching),
        ("Boston", bos.matching),
        ("Top Trading Cycles", ttc.matching),
        ("Serial Dictatorship", sd.matching),
    ]

    st.subheader("Matching por estudiante")
    table = {"Estudiante": students}
    for name, matching in mechanisms:
        table[name] = [matching.get(s) or "—" for s in students]
    st.table(table)

    st.subheader("Propiedades del resultado")
    summary_rows = []
    for name, matching in mechanisms:
        stable, blocking = is_stable(matching, student_prefs, school_prefs, capacities)
        ranks = [rank_of(s, matching.get(s)) for s in students]
        valid_ranks = [r for r in ranks if r is not None]
        avg_rank = sum(valid_ranks) / len(valid_ranks) if valid_ranks else None
        n_top_choice = sum(1 for r in valid_ranks if r == 0)
        summary_rows.append(
            {
                "Mecanismo": name,
                "Estable": "✅" if stable else f"❌ ({len(blocking)} par(es) bloqueante(s))",
                "Ranking promedio obtenido": f"{avg_rank:.2f}" if avg_rank is not None else "—",
                "Estudiantes con su 1ª opción": f"{n_top_choice} / {n_students}",
            }
        )
    st.table(summary_rows)

    st.info(
        "Ranking promedio obtenido = 0 significa que, en promedio, todos "
        "consiguieron su primera opción; cuanto más alto, peor. Es una "
        "forma simple de comparar bienestar entre mecanismos, además de "
        "la estabilidad."
    )
