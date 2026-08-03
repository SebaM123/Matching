import random
import sys
from collections import Counter
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.chile_priorities import (
    build_priority_reforma,
    build_priority_sae_actual,
    generate_student_attrs,
)
from mechanisms.deferred_acceptance import deferred_acceptance
from mechanisms.simulation import _make_capacities, generate_student_preferences, rank_of

st.set_page_config(page_title="Chile en la práctica", page_icon="🇨🇱", layout="wide")
st.title("🇨🇱 Chile en la práctica: el SAE y la reforma en discusión")

tab_actual, tab_reforma, tab_sim = st.tabs(
    ["📖 Sistema actual (SAE)", "📖 Reforma en discusión (2026)", "🧪 Simulador comparativo"]
)

with tab_actual:
    theory_path = Path(__file__).resolve().parent.parent / "content" / "chile_sae_actual.md"
    st.markdown(theory_path.read_text(encoding="utf-8"))

with tab_reforma:
    theory_path = Path(__file__).resolve().parent.parent / "content" / "chile_reforma_2026.md"
    st.markdown(theory_path.read_text(encoding="utf-8"))

with tab_sim:
    st.markdown(
        "Genera estudiantes sintéticos con atributos al estilo SAE (hermano, "
        "prioritario SEP, hijo de funcionario, exalumno, rendimiento) y "
        "compara la composición de quién accede a los **colegios de alta "
        "demanda** bajo el sistema actual vs. un modelo simplificado de la "
        "reforma. Todos los parámetros son ajustables — son supuestos de "
        "modelación, no cifras oficiales."
    )

    col1, col2 = st.columns(2)
    n_students = col1.slider("Cantidad de estudiantes", min_value=100, max_value=2000, value=400, step=100)
    n_schools = col2.slider("Cantidad de colegios", min_value=10, max_value=100, value=40, step=5)

    st.subheader("Composición de la población de estudiantes")
    c1, c2, c3, c4 = st.columns(4)
    prob_hermano = c1.slider("% con hermano matriculado", 0, 100, 10) / 100
    prob_prioritario = c2.slider("% estudiantes prioritarios (SEP)", 0, 100, 40) / 100
    prob_funcionario = c3.slider("% hijos de funcionarios", 0, 100, 2) / 100
    prob_exalumno = c4.slider("% exalumnos", 0, 100, 5) / 100

    correlacion = st.slider(
        "Correlación entre vulnerabilidad y rendimiento académico simulado",
        min_value=-1.0,
        max_value=1.0,
        value=-0.5,
        step=0.1,
        help=(
            "Supuesto de modelación ajustable: valores negativos hacen que "
            "el rendimiento académico simulado sea, en promedio, más bajo "
            "para estudiantes prioritarios -- representando el argumento, "
            "presente en el debate público, de que el mérito académico "
            "correlaciona con el nivel socioeconómico. Ponelo en 0 para "
            "sacar ese supuesto."
        ),
    )

    pref_correlation = st.slider(
        "Popularidad compartida de colegios (competencia por los mismos colegios)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
    )

    st.subheader("Parámetros de la reforma (Elección Mutua)")
    r1, r2, r3, r4 = st.columns(4)
    peso_merito = r1.slider("Peso: rendimiento académico", 0.0, 1.0, 0.6, 0.1)
    peso_entrevista = r2.slider("Peso: entrevista / adhesión", 0.0, 1.0, 0.3, 0.1)
    peso_cercania = r3.slider("Peso: cercanía territorial", 0.0, 1.0, 0.1, 0.1)
    cupo_reservado_pct = r4.slider("Cupo reservado para prioritarios", 0, 100, 20) / 100

    seed = st.number_input("Semilla aleatoria", value=1)

    if st.button("▶ Generar y comparar", type="primary"):
        rng = random.Random(seed)
        students = [f"E{i+1}" for i in range(n_students)]
        schools = [f"C{i+1}" for i in range(n_schools)]
        capacities = _make_capacities(n_students, schools)

        student_prefs = generate_student_preferences(students, schools, pref_correlation, rng)
        attrs = generate_student_attrs(
            students, prob_hermano, prob_prioritario, prob_funcionario, prob_exalumno, correlacion, rng
        )

        sae_prefs = build_priority_sae_actual(attrs, schools, rng)
        reforma_prefs = build_priority_reforma(
            attrs, schools, capacities, peso_merito, peso_entrevista, peso_cercania, cupo_reservado_pct, rng
        )

        da_sae = deferred_acceptance(student_prefs, sae_prefs, capacities, proposing="students").matching
        da_reforma = deferred_acceptance(student_prefs, reforma_prefs, capacities, proposing="students").matching

        first_choice_counts = Counter(student_prefs[s][0] for s in students)
        n_top = max(1, n_schools // 5)
        top_schools = {c for c, _ in first_choice_counts.most_common(n_top)}

        pct_prioritarios_poblacion = sum(1 for s in students if attrs[s].prioritario) / n_students

        def stats_for(matching):
            asignados_top = [s for s in students if matching.get(s) in top_schools]
            pct_prioritarios_top = (
                sum(1 for s in asignados_top if attrs[s].prioritario) / len(asignados_top)
                if asignados_top
                else None
            )
            ranks_prioritarios = [
                rank_of(student_prefs, s, matching.get(s)) for s in students if attrs[s].prioritario
            ]
            ranks_no_prioritarios = [
                rank_of(student_prefs, s, matching.get(s)) for s in students if not attrs[s].prioritario
            ]
            ranks_prioritarios = [r for r in ranks_prioritarios if r is not None]
            ranks_no_prioritarios = [r for r in ranks_no_prioritarios if r is not None]
            return {
                "% prioritarios en colegios de alta demanda": pct_prioritarios_top,
                "Ranking promedio -- prioritarios": sum(ranks_prioritarios) / len(ranks_prioritarios)
                if ranks_prioritarios
                else None,
                "Ranking promedio -- no prioritarios": sum(ranks_no_prioritarios) / len(ranks_no_prioritarios)
                if ranks_no_prioritarios
                else None,
            }

        st.subheader("Resultado")
        st.caption(
            f"Referencia: los estudiantes prioritarios son el "
            f"{pct_prioritarios_poblacion:.0%} de la población total. "
            f"'Colegios de alta demanda' = el {100 // 5}% de colegios más "
            f"elegidos como primera opción."
        )

        rows = []
        for label, matching in [("SAE actual", da_sae), ("Reforma (Elección Mutua)", da_reforma)]:
            s = stats_for(matching)
            rows.append(
                {
                    "Régimen": label,
                    "% prioritarios en colegios de alta demanda": f"{s['% prioritarios en colegios de alta demanda']:.1%}"
                    if s["% prioritarios en colegios de alta demanda"] is not None
                    else "—",
                    "Ranking promedio (prioritarios)": f"{s['Ranking promedio -- prioritarios']:.2f}"
                    if s["Ranking promedio -- prioritarios"] is not None
                    else "—",
                    "Ranking promedio (no prioritarios)": f"{s['Ranking promedio -- no prioritarios']:.2f}"
                    if s["Ranking promedio -- no prioritarios"] is not None
                    else "—",
                }
            )
        st.table(rows)

        chart_df = pd.DataFrame(
            {
                "SAE actual": [
                    stats_for(da_sae)["Ranking promedio -- prioritarios"],
                    stats_for(da_sae)["Ranking promedio -- no prioritarios"],
                ],
                "Reforma": [
                    stats_for(da_reforma)["Ranking promedio -- prioritarios"],
                    stats_for(da_reforma)["Ranking promedio -- no prioritarios"],
                ],
            },
            index=["Prioritarios", "No prioritarios"],
        )
        st.bar_chart(chart_df)

        st.info(
            "Estos números dependen enteramente de los parámetros que "
            "elegiste arriba (son supuestos de modelación, no cifras "
            "oficiales) -- el objetivo es explorar la dirección del efecto "
            "de cambiar quién define la prioridad, no predecir un resultado "
            "real. Cambiá los pesos y la correlación para ver cómo se mueve."
        )
