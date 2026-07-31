import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.deferred_acceptance import is_stable
from mechanisms.serial_dictatorship import serial_dictatorship

st.set_page_config(page_title="Serial Dictatorship", page_icon="🔀", layout="wide")
st.title("Serial Dictatorship")

tab_theory, tab_sim = st.tabs(["📖 Teoría", "🧪 Simulador"])


def parse_pref_list(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


with tab_sim:
    st.markdown(
        "Acá no hay prioridades por colegio: hay un único **orden de "
        "prioridad** entre los estudiantes, y cada uno elige por turno el "
        "colegio que más prefiere entre los que quedan con cupo."
    )

    col_n1, col_n2 = st.columns(2)
    n_students = col_n1.number_input("Cantidad de estudiantes", min_value=1, max_value=10, value=3)
    n_schools = col_n2.number_input("Cantidad de colegios", min_value=1, max_value=10, value=3)

    students = [f"E{i+1}" for i in range(n_students)]
    schools = [f"C{i+1}" for i in range(n_schools)]

    default_student_prefs = {
        "E1": "C1, C2, C3",
        "E2": "C2, C1, C3",
        "E3": "C1, C2, C3",
    }

    st.subheader("Cupos por colegio")
    capacities = {}
    cap_cols = st.columns(len(schools))
    for i, c in enumerate(schools):
        capacities[c] = cap_cols[i].number_input(
            f"Cupo {c}", min_value=1, max_value=n_students, value=1, key=f"sd_cap_{c}"
        )

    st.subheader("Orden de prioridad (de mayor a menor prioridad)")
    order_raw = st.text_input(
        "Orden:", value=", ".join(students), key="sd_order"
    )
    order = parse_pref_list(order_raw)

    st.subheader("Preferencias de los estudiantes (colegio más preferido primero)")
    student_prefs = {}
    for s in students:
        default = default_student_prefs.get(s, ", ".join(schools))
        raw = st.text_input(f"{s}:", value=default, key=f"sd_pref_{s}")
        student_prefs[s] = parse_pref_list(raw)

    if st.button("▶ Ejecutar Serial Dictatorship", type="primary"):
        result = serial_dictatorship(order, student_prefs, capacities)

        # Para chequear estabilidad, se trata el orden de prioridad como si
        # fuera la prioridad compartida por todos los colegios por igual.
        school_prefs = {c: order for c in schools}
        stable, blocking_pairs = is_stable(result.matching, student_prefs, school_prefs, capacities)

        st.subheader("Resultado")
        matched = {s: c for s, c in result.matching.items() if c is not None}
        unmatched = [s for s, c in result.matching.items() if c is None]

        res_col1, res_col2 = st.columns([2, 1])
        with res_col1:
            st.table(
                {"Estudiante": list(matched.keys()), "Colegio asignado": list(matched.values())}
            )
            if unmatched:
                st.warning(f"Sin asignar: {', '.join(unmatched)}")
        with res_col2:
            if stable:
                st.success("✅ Estable (respecto al orden como prioridad compartida)")
            else:
                st.error("❌ Inestable (respecto al orden como prioridad compartida)")
                for s, c in blocking_pairs:
                    st.write(f"Par bloqueante: **{s}** y **{c}** se prefieren mutuamente")

        with st.expander("Ver turnos paso a paso"):
            for i, pick in enumerate(result.picks, start=1):
                if pick.chosen:
                    st.write(f"{i}. **{pick.student}** elige **{pick.chosen}**")
                else:
                    st.write(f"{i}. **{pick.student}** no tiene colegios con cupo disponible")

        st.info(
            "Con el ejemplo por defecto, el resultado debería coincidir "
            "exactamente con el de Deferred Acceptance sobre las mismas "
            "preferencias. Esto no es casualidad — es el caso especial "
            "donde todos los colegios comparten la misma prioridad."
        )

with tab_theory:
    theory_path = Path(__file__).resolve().parent.parent / "content" / "serial_dictatorship.md"
    st.markdown(theory_path.read_text(encoding="utf-8"))
