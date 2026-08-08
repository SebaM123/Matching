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

    with st.expander("📋 Supuestos de este simulador — leé esto antes de citar un resultado"):
        st.markdown(
            """
Si vas a compartir o citar un resultado de este simulador, estos son los
supuestos que lo generan — todos son elecciones de modelación, no datos
oficiales, y cambiarlos puede cambiar la conclusión:

1. **Los atributos (hermano, prioritario, hijo de funcionario, exalumno)
   se sortean de forma independiente entre sí.** En la realidad podrían
   estar correlacionados (ej. ser hijo de funcionario probablemente
   correlaciona negativamente con ser prioritario SEP) — este simulador no
   captura esas correlaciones cruzadas.
2. **La "correlación" entre vulnerabilidad y rendimiento es un
   desplazamiento simple del promedio** (hasta ±0.3 en una escala 0-1),
   no un coeficiente de correlación estadística en sentido estricto.
3. **"Entrevista" y "cercanía territorial" (bajo la reforma) se generan
   como ruido aleatorio, independiente de cualquier otro atributo del
   estudiante — en particular, independiente de ser prioritario.** Este
   es un supuesto optimista para el argumento de que la reforma perjudica
   a los prioritarios: si en la realidad la cercanía territorial está
   correlacionada con segregación socioeconómica (barrios vulnerables más
   lejos de los colegios de alta demanda), el efecto real podría ser
   **mayor** al que muestra el simulador con este supuesto neutral.
4. **Los pesos de mérito/entrevista/cercanía son los mismos para todos
   los colegios.** En la realidad, cada colegio podría ponderar estos
   criterios distinto según su propio proyecto educativo.
5. **Las preferencias de las familias se mantienen fijas entre ambos
   regímenes.** No se modela que las familias cambien a qué colegios
   postulan al cambiar el mecanismo (sin respuesta estratégica o
   conductual a la reforma).
6. **"Colegios de alta demanda"** se define una sola vez (aprox. el 20%
   más elegido como primera opción, sobre las preferencias generadas) y
   se usa la misma definición para comparar ambos regímenes — así la
   comparación es sobre la misma vara.
7. **Cada corrida es aleatoria.** Con una sola simulación, el resultado
   puede variar bastante de una tirada a otra — usá "Cantidad de
   simulaciones a promediar" (abajo) para un número más estable antes de
   citarlo.
            """
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

    n_reps = st.number_input(
        "Cantidad de simulaciones a promediar",
        min_value=1,
        max_value=20,
        value=5,
        help="Una sola tirada aleatoria puede variar bastante. Promediar varias da un número más estable para citar.",
    )
    seed = st.number_input("Semilla aleatoria (para poder repetir el mismo experimento)", value=1)

    def stats_for(matching, students, attrs, student_prefs, top_schools):
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

    if st.button("▶ Generar y comparar", type="primary"):
        with st.spinner(f"Generando {n_reps} simulación(es) de {n_students} estudiantes..."):
            students = [f"E{i+1}" for i in range(n_students)]
            schools = [f"C{i+1}" for i in range(n_schools)]
            capacities = _make_capacities(n_students, schools)

            acc = {"SAE actual": [], "Reforma (Elección Mutua)": []}
            pct_prioritarios_reps = []
            n_top_pct_reps = []

            for rep in range(n_reps):
                rng = random.Random(seed + rep)

                student_prefs = generate_student_preferences(students, schools, pref_correlation, rng)
                attrs = generate_student_attrs(
                    students, prob_hermano, prob_prioritario, prob_funcionario, prob_exalumno, correlacion, rng
                )

                sae_prefs = build_priority_sae_actual(attrs, schools, rng)
                reforma_prefs = build_priority_reforma(
                    attrs, schools, capacities, peso_merito, peso_entrevista, peso_cercania, cupo_reservado_pct, rng
                )

                da_sae = deferred_acceptance(student_prefs, sae_prefs, capacities, proposing="students").matching
                da_reforma = deferred_acceptance(
                    student_prefs, reforma_prefs, capacities, proposing="students"
                ).matching

                first_choice_counts = Counter(student_prefs[s][0] for s in students)
                n_top = max(1, n_schools // 5)
                top_schools = {c for c, _ in first_choice_counts.most_common(n_top)}
                n_top_pct_reps.append(n_top / n_schools)

                pct_prioritarios_reps.append(sum(1 for s in students if attrs[s].prioritario) / n_students)

                acc["SAE actual"].append(stats_for(da_sae, students, attrs, student_prefs, top_schools))
                acc["Reforma (Elección Mutua)"].append(
                    stats_for(da_reforma, students, attrs, student_prefs, top_schools)
                )

        def avg(key, entries):
            vals = [e[key] for e in entries if e[key] is not None]
            return sum(vals) / len(vals) if vals else None

        pct_prioritarios_poblacion = sum(pct_prioritarios_reps) / len(pct_prioritarios_reps)
        n_top_pct = sum(n_top_pct_reps) / len(n_top_pct_reps)

        st.subheader(f"Resultado (promedio sobre {n_reps} simulación(es))")
        st.caption(
            f"Referencia: los estudiantes prioritarios son, en promedio, el "
            f"{pct_prioritarios_poblacion:.0%} de la población total. "
            f"'Colegios de alta demanda' = el {n_top_pct:.0%} de colegios más "
            f"elegidos como primera opción."
        )

        rows = []
        for label in ["SAE actual", "Reforma (Elección Mutua)"]:
            entries = acc[label]
            pct_top = avg("% prioritarios en colegios de alta demanda", entries)
            rank_p = avg("Ranking promedio -- prioritarios", entries)
            rank_np = avg("Ranking promedio -- no prioritarios", entries)
            rows.append(
                {
                    "Régimen": label,
                    "% prioritarios en colegios de alta demanda": f"{pct_top:.1%}" if pct_top is not None else "—",
                    "Ranking promedio (prioritarios)": f"{rank_p:.2f}" if rank_p is not None else "—",
                    "Ranking promedio (no prioritarios)": f"{rank_np:.2f}" if rank_np is not None else "—",
                }
            )
        st.table(rows)

        chart_df = pd.DataFrame(
            {
                "SAE actual": [
                    avg("Ranking promedio -- prioritarios", acc["SAE actual"]),
                    avg("Ranking promedio -- no prioritarios", acc["SAE actual"]),
                ],
                "Reforma": [
                    avg("Ranking promedio -- prioritarios", acc["Reforma (Elección Mutua)"]),
                    avg("Ranking promedio -- no prioritarios", acc["Reforma (Elección Mutua)"]),
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
