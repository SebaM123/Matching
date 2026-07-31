import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.ttc import top_trading_cycles

st.set_page_config(page_title="House Allocation", page_icon="🔀", layout="wide")
st.title("House Allocation (mercado de casas, Shapley-Scarf)")

tab_theory, tab_sim = st.tabs(["📖 Teoría", "🧪 Simulador"])


def parse_pref_list(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


with tab_sim:
    st.markdown(
        "Cada agente ya es dueño de una casa. Define las preferencias de "
        "cada agente sobre **todas** las casas (incluida la propia), y el "
        "simulador ejecuta Top Trading Cycles para encontrar los "
        "intercambios."
    )

    n_agents = st.number_input("Cantidad de agentes (= cantidad de casas)", min_value=2, max_value=10, value=3)
    agents = [f"A{i+1}" for i in range(n_agents)]
    houses = [f"H{i+1}" for i in range(n_agents)]

    st.caption("Cada agente A_i es dueño de la casa H_i.")

    default_prefs = {
        "A1": "H2, H1, H3",
        "A2": "H3, H2, H1",
        "A3": "H1, H3, H2",
    }

    st.subheader("Preferencias de cada agente (casa más preferida primero)")
    agent_prefs = {}
    for a in agents:
        default = default_prefs.get(a, ", ".join(houses))
        raw = st.text_input(f"{a}:", value=default, key=f"ha_pref_{a}")
        agent_prefs[a] = parse_pref_list(raw)

    owner_of = {f"H{i+1}": f"A{i+1}" for i in range(n_agents)}
    house_prefs = {h: [owner_of[h]] for h in houses}
    capacities = {h: 1 for h in houses}

    if st.button("▶ Ejecutar House Allocation", type="primary"):
        result = top_trading_cycles(agent_prefs, house_prefs, capacities)

        st.subheader("Resultado")
        matched = {a: h for a, h in result.matching.items() if h is not None}
        unmatched = [a for a, h in result.matching.items() if h is None]

        col1, col2 = st.columns([2, 1])
        with col1:
            rows = []
            for a in agents:
                own = f"H{agents.index(a) + 1}"
                got = matched.get(a)
                rows.append(
                    {
                        "Agente": a,
                        "Casa propia": own,
                        "Casa asignada": got,
                        "¿Mejoró?": "Sí" if got != own else "Se quedó con la suya",
                    }
                )
            st.table(rows)
            if unmatched:
                st.warning(f"Sin asignar: {', '.join(unmatched)}")
        with col2:
            n_traded = sum(1 for a in agents if matched.get(a) != f"H{agents.index(a) + 1}")
            st.metric("Agentes que intercambiaron", f"{n_traded} / {n_agents}")

        with st.expander("Ver ciclos de intercambio"):
            for i, cycle in enumerate(result.cycles, start=1):
                path_str = " → ".join(cycle.path + [cycle.path[0]])
                st.write(f"**Ciclo {i}:** {path_str}")

        st.info(
            "En este modelo, TTC es simultáneamente eficiente en el sentido "
            "de Pareto, individualmente racional y strategy-proof — no hay "
            "trade-off que explorar, a diferencia de la página de TTC para "
            "colegios."
        )

with tab_theory:
    theory_path = Path(__file__).resolve().parent.parent / "content" / "house_allocation.md"
    st.markdown(theory_path.read_text(encoding="utf-8"))
