import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.deferred_acceptance import deferred_acceptance, is_stable

st.set_page_config(page_title="Deferred Acceptance", page_icon="🔀", layout="wide")
st.title("Deferred Acceptance (Gale-Shapley)")

tab_theory, tab_sim = st.tabs(["📖 Teoría", "🧪 Simulador"])


def parse_pref_list(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


with tab_sim:
    st.markdown(
        "Define estudiantes, colegios, cupos y preferencias, elige quién "
        "propone, y ejecuta el algoritmo."
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
    default_school_prefs = {
        "C1": "E2, E1, E3",
        "C2": "E1, E2, E3",
        "C3": "E1, E2, E3",
    }

    st.subheader("Cupos por colegio")
    capacities = {}
    cap_cols = st.columns(len(schools))
    for i, c in enumerate(schools):
        capacities[c] = cap_cols[i].number_input(
            f"Cupo {c}", min_value=1, max_value=n_students, value=1, key=f"cap_{c}"
        )

    st.subheader("Preferencias de los estudiantes (colegio más preferido primero)")
    student_prefs = {}
    for s in students:
        default = default_student_prefs.get(s, ", ".join(schools))
        raw = st.text_input(f"{s}:", value=default, key=f"pref_{s}")
        student_prefs[s] = parse_pref_list(raw)

    st.subheader("Preferencias de los colegios (estudiante más preferido primero)")
    school_prefs = {}
    for c in schools:
        default = default_school_prefs.get(c, ", ".join(students))
        raw = st.text_input(f"{c}:", value=default, key=f"pref_{c}")
        school_prefs[c] = parse_pref_list(raw)

    proposing = st.radio(
        "¿Quién propone?",
        options=["students", "schools"],
        format_func=lambda x: "Estudiantes" if x == "students" else "Colegios",
        horizontal=True,
    )

    if st.button("▶ Ejecutar Deferred Acceptance", type="primary"):
        result = deferred_acceptance(student_prefs, school_prefs, capacities, proposing=proposing)
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

        with st.expander("Ver traza paso a paso"):
            for i, r in enumerate(result.rounds, start=1):
                if r.accepted and r.displaced:
                    st.write(
                        f"{i}. **{r.proposer}** propone a **{r.target}** → aceptado, "
                        f"desplaza a **{r.displaced}**"
                    )
                elif r.accepted:
                    st.write(f"{i}. **{r.proposer}** propone a **{r.target}** → aceptado (tentativo)")
                else:
                    st.write(f"{i}. **{r.proposer}** propone a **{r.target}** → rechazado")

        st.info(
            "Prueba cambiar '¿Quién propone?' y vuelve a ejecutar con las mismas "
            "preferencias: el matching puede cambiar, pero ambos resultados son estables."
        )

with tab_theory:
    theory_path = Path(__file__).resolve().parent.parent / "content" / "deferred_acceptance.md"
    st.markdown(theory_path.read_text(encoding="utf-8"))
