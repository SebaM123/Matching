import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from mechanisms.kidney_exchange import kidney_exchange

st.set_page_config(page_title="Kidney Exchange", page_icon="🔀", layout="wide")
st.title("Kidney Exchange")

tab_sim, tab_theory = st.tabs(["🧪 Simulador", "📖 Teoría"])


def parse_list(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


with tab_sim:
    st.markdown(
        "Cada pareja paciente-donante es incompatible entre sí. Definí "
        "**con el donante de qué otras parejas es compatible el paciente "
        "de cada una**, y el simulador busca ciclos de intercambio."
    )

    n_pairs = st.number_input("Cantidad de parejas", min_value=2, max_value=10, value=4)
    pairs = [f"P{i+1}" for i in range(n_pairs)]

    default_compat = {
        "P1": "P2",
        "P2": "P3",
        "P3": "P1",
        "P4": "",
    }

    st.subheader("Compatibilidad (el paciente de esta pareja acepta el donante de:)")
    compat = {}
    for p in pairs:
        default = default_compat.get(p, "")
        raw = st.text_input(f"{p} es compatible con el donante de:", value=default, key=f"kex_compat_{p}")
        compat[p] = parse_list(raw)

    max_cycle_length = st.slider(
        "Largo máximo de ciclo permitido (restricción logística)",
        min_value=2,
        max_value=min(6, n_pairs),
        value=3,
    )

    if st.button("▶ Ejecutar Kidney Exchange", type="primary"):
        result = kidney_exchange(pairs, compat, max_cycle_length=max_cycle_length)

        st.subheader("Resultado")
        matched = {p: donor for p, donor in result.matching.items() if donor is not None}
        unmatched = [p for p, donor in result.matching.items() if donor is None]

        res_col1, res_col2 = st.columns([2, 1])
        with res_col1:
            if matched:
                st.table(
                    {
                        "Pareja": list(matched.keys()),
                        "Recibe el riñón de": list(matched.values()),
                    }
                )
            else:
                st.write("Ninguna pareja consiguió trasplante con esta configuración.")
            if unmatched:
                st.warning(f"Sin trasplante: {', '.join(unmatched)}")
        with res_col2:
            st.metric("Parejas trasplantadas", f"{len(matched)} / {n_pairs}")

        with st.expander("Ver ciclos encontrados"):
            if result.cycles:
                for i, cycle in enumerate(result.cycles, start=1):
                    path_str = " → ".join(cycle.pairs + [cycle.pairs[0]])
                    st.write(f"**Ciclo {i}** ({len(cycle.pairs)} parejas): {path_str}")
            else:
                st.write("No se encontró ningún ciclo con el largo máximo permitido.")

        st.info(
            "Probá bajar el largo máximo de ciclo a 2 con el ejemplo por "
            "defecto: la compatibilidad circular de 3 parejas desaparece "
            "por completo, aunque la compatibilidad siga existiendo."
        )

with tab_theory:
    theory_path = Path(__file__).resolve().parent.parent / "content" / "kidney_exchange.md"
    st.markdown(theory_path.read_text(encoding="utf-8"))
