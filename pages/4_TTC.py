import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.deferred_acceptance import is_stable
from mechanisms.ttc import top_trading_cycles

st.set_page_config(page_title="Top Trading Cycles", page_icon="🔀", layout="wide")
st.title("Top Trading Cycles (TTC)")

tab_sim, tab_theory = st.tabs(["🧪 Simulador", "📖 Teoría"])


def parse_pref_list(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


with tab_sim:
    st.markdown(
        "Mismo tipo de problema que en los otros mecanismos, pero acá los "
        "estudiantes y colegios **intercambian lugares en ciclos** en vez "
        "de proponer y aceptar."
    )

    col_n1, col_n2 = st.columns(2)
    n_students = col_n1.number_input("Cantidad de estudiantes", min_value=1, max_value=10, value=3)
    n_schools = col_n2.number_input("Cantidad de colegios", min_value=1, max_value=10, value=3)

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
            f"Cupo {c}", min_value=1, max_value=n_students, value=1, key=f"ttc_cap_{c}"
        )

    st.subheader("Preferencias de los estudiantes (colegio más preferido primero)")
    student_prefs = {}
    for s in students:
        default = default_student_prefs.get(s, ", ".join(schools))
        raw = st.text_input(f"{s}:", value=default, key=f"ttc_pref_{s}")
        student_prefs[s] = parse_pref_list(raw)

    st.subheader("Prioridad de los colegios (estudiante de mayor prioridad primero)")
    school_prefs = {}
    for c in schools:
        default = default_school_prefs.get(c, ", ".join(students))
        raw = st.text_input(f"{c}:", value=default, key=f"ttc_pref_{c}")
        school_prefs[c] = parse_pref_list(raw)

    if st.button("▶ Ejecutar TTC", type="primary"):
        result = top_trading_cycles(student_prefs, school_prefs, capacities)
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
                st.success("✅ Matching estable")
            else:
                st.error("❌ Matching inestable")
                for s, c in blocking_pairs:
                    st.write(f"Par bloqueante: **{s}** y **{c}** se prefieren mutuamente")

        with st.expander("Ver ciclos paso a paso"):
            for i, cycle in enumerate(result.cycles, start=1):
                path_str = " → ".join(cycle.path + [cycle.path[0]])
                st.write(f"**Ciclo {i}:** {path_str}")
                for s, c in cycle.assignments.items():
                    st.write(f"　{s} → {c}")

        st.info(
            "TTC prioriza la eficiencia de Pareto por sobre la estabilidad: "
            "compará este resultado con el de Deferred Acceptance sobre las "
            "mismas preferencias — puede que acá alguien mejore, pero el "
            "matching deje de ser estable."
        )

with tab_theory:
    theory_path = Path(__file__).resolve().parent.parent / "content" / "ttc.md"
    st.markdown(theory_path.read_text(encoding="utf-8"))
