import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.boston import boston_mechanism
from mechanisms.deferred_acceptance import deferred_acceptance, is_stable
from mechanisms.serial_dictatorship import serial_dictatorship
from mechanisms.simulation import generate_market, summarize
from mechanisms.ttc import top_trading_cycles

st.set_page_config(page_title="Simulación masiva", page_icon="📊", layout="wide")
st.title("📊 Simulación masiva")

st.markdown(
    "Los ejemplos anteriores usaban 3 o 4 agentes para poder seguir el "
    "algoritmo paso a paso. Acá se invierte el objetivo: generar mercados "
    "**grandes** (cientos de estudiantes) al azar y comparar **estadísticas "
    "agregadas** entre mecanismos — cosas que no se ven con ejemplos "
    "chicos, como qué tan seguido aparecen pares bloqueantes o qué "
    "fracción de estudiantes consigue su primera opción.\n\n"
    "No incluye Kidney Exchange ni Mercado de Casas: sus algoritmos no "
    "están pensados para esta escala (Kidney Exchange en particular es "
    "computacionalmente costoso de resolver de forma exacta)."
)

col1, col2 = st.columns(2)
n_students = col1.slider("Cantidad de estudiantes", min_value=50, max_value=2000, value=500, step=50)
n_schools = col2.slider("Cantidad de colegios", min_value=5, max_value=200, value=50, step=5)

st.caption(
    f"Cupos: se reparten {n_students} cupos entre los {n_schools} colegios "
    "en partes iguales, así que en principio alcanza para todos — la "
    "pregunta no es cuántos consiguen algo, sino qué tan bueno."
)

pref_correlation = st.slider(
    "Correlación de preferencias entre estudiantes",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help=(
        "0 = cada estudiante tiene un orden de preferencia totalmente "
        "independiente (sin colegios 'populares'). 1 = todos los "
        "estudiantes tienen exactamente el mismo orden de preferencia "
        "(máxima competencia por los mismos colegios)."
    ),
)

common_priority = st.checkbox(
    "Todos los colegios comparten la misma prioridad (mérito único / sorteo único)",
    value=False,
    help=(
        "Si se activa, DA, TTC y Serial Dictatorship deberían coincidir "
        "exactamente — es el caso especial que viste en la página de "
        "Serial Dictatorship."
    ),
)

n_reps = st.number_input(
    "Cantidad de simulaciones a promediar", min_value=1, max_value=20, value=5
)
seed = st.number_input("Semilla aleatoria (para poder repetir el mismo experimento)", value=42)

mechanism_names = ["Deferred Acceptance", "Boston", "Top Trading Cycles", "Serial Dictatorship"]


def run_all(market):
    da = deferred_acceptance(market.student_prefs, market.school_prefs, market.capacities, proposing="students")
    bos = boston_mechanism(market.student_prefs, market.school_prefs, market.capacities)
    ttc = top_trading_cycles(market.student_prefs, market.school_prefs, market.capacities)
    sd = serial_dictatorship(market.sd_order, market.student_prefs, market.capacities)
    return {
        "Deferred Acceptance": da.matching,
        "Boston": bos.matching,
        "Top Trading Cycles": ttc.matching,
        "Serial Dictatorship": sd.matching,
    }


if st.button("▶ Generar y ejecutar simulación", type="primary"):
    with st.spinner(f"Generando {n_reps} mercado(s) de {n_students} estudiantes y corriendo los 4 mecanismos..."):
        acc = {name: {"pct_matched": [], "avg_rank": [], "pct_top_choice": [], "blocking": [], "buckets": []} for name in mechanism_names}

        for rep in range(n_reps):
            market = generate_market(
                n_students=n_students,
                n_schools=n_schools,
                pref_correlation=pref_correlation,
                common_priority=common_priority,
                seed=seed + rep,
            )
            matchings = run_all(market)
            for name, matching in matchings.items():
                summ = summarize(matching, market.student_prefs)
                _, blocking = is_stable(matching, market.student_prefs, market.school_prefs, market.capacities)
                acc[name]["pct_matched"].append(summ["pct_matched"])
                acc[name]["avg_rank"].append(summ["avg_rank"] if summ["avg_rank"] is not None else 0)
                acc[name]["pct_top_choice"].append(summ["pct_top_choice"])
                acc[name]["blocking"].append(len(blocking))
                acc[name]["buckets"].append(summ["bucket_counts"])

    st.subheader(f"Resultados promediados sobre {n_reps} simulación(es)")

    summary_rows = []
    bucket_order = ["1ª opción", "2ª-3ª", "4ª-10ª", "11ª o peor", "Sin asignar"]
    bucket_table = {b: [] for b in bucket_order}

    for name in mechanism_names:
        data = acc[name]
        n = len(data["pct_matched"])
        summary_rows.append(
            {
                "Mecanismo": name,
                "% Asignados": f"{sum(data['pct_matched']) / n:.1%}",
                "Ranking promedio obtenido": f"{sum(data['avg_rank']) / n:.2f}",
                "% con 1ª opción": f"{sum(data['pct_top_choice']) / n:.1%}",
                "Pares bloqueantes (prom.)": f"{sum(data['blocking']) / n:.1f}",
                "% simulaciones estables": f"{sum(1 for b in data['blocking'] if b == 0) / n:.0%}",
            }
        )
        total_students = n_students * n
        summed_buckets = {b: sum(rep[b] for rep in data["buckets"]) for b in bucket_order}
        for b in bucket_order:
            bucket_table[b].append(summed_buckets[b] / total_students)

    st.table(summary_rows)

    st.subheader("Distribución de resultados por estudiante")
    chart_df = pd.DataFrame(bucket_table, index=mechanism_names)
    st.bar_chart(chart_df)

    st.info(
        "Ranking promedio obtenido = 0 significa que, en promedio, todos "
        "consiguieron su primera opción. 'Pares bloqueantes (prom.)' es la "
        "cantidad promedio de pares estudiante-colegio que se prefieren "
        "mutuamente por sobre su asignación — en Deferred Acceptance "
        "siempre debería dar 0."
    )
