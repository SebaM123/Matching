"""Regression tests con resultados exactos y conocidos de antemano.

A diferencia de tests/verify_all.py (que genera cientos de instancias
aleatorias y chequea invariantes generales), cada test acá corresponde a
un ejemplo concreto con un resultado esperado exacto:

- Uno tomado directamente del libro de referencia del portal (Xiang Sun,
  "Matching and Market Design: Theory and Practice", 2018) -- el ejemplo
  original de Gale-Shapley (Example 2.17), reconstruido a partir de la
  tabla de preferencias del PDF (extraída por coordenadas de texto, no
  por el texto plano que mezcla las columnas) y verificado paso a paso
  contra la traza completa que el libro da en prosa.
- El resto son los ejemplos "por defecto" de cada página del portal, ya
  verificados a mano (y en el navegador) durante el desarrollo -- fijados
  acá para que un cambio futuro que rompa alguno de ellos se note de
  inmediato.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from mechanisms.boston import boston_mechanism
from mechanisms.chile_priorities import apply_minority_reserve
from mechanisms.deferred_acceptance import deferred_acceptance, is_stable
from mechanisms.kidney_exchange import kidney_exchange
from mechanisms.serial_dictatorship import serial_dictatorship
from mechanisms.ttc import top_trading_cycles

failures: list[str] = []
checks_run = 0


def check_eq(actual, expected, label):
    global checks_run
    checks_run += 1
    if actual != expected:
        failures.append(f"{label}:\n    esperado: {expected}\n    obtenido: {actual}")


# ---------------------------------------------------------------------------
# Gale-Shapley, Example 2.17 (Sun, 2018) -- 5 hombres, 4 mujeres.
# ---------------------------------------------------------------------------

def test_gale_shapley_example_2_17():
    # "estudiantes" = hombres (m1..m5), "colegios" = mujeres (w1..w4).
    # Preferencias reconstruidas de la Tabla 2.2 del libro y verificadas
    # contra cada paso de su traza en prosa (Step 1 a Step 4):
    #   Step 1: m1,m4,m5 -> w1 (w1 se queda con m1); m2,m3 -> w4 (w4 se
    #           queda con m2).
    #   Step 2: m3 -> w3; m4 -> w4 (w4 rechaza a m2, se queda con m4);
    #           m5 -> w2.
    #   Step 3: m2 -> w2 (w2 rechaza a m5, se queda con m2).
    #   Step 4: m5 -> w4 (rechazado; ya probó todas sus opciones, soltero).
    student_prefs = {
        "m1": ["w1", "w2", "w3", "w4"],
        "m2": ["w4", "w2", "w3", "w1"],
        "m3": ["w4", "w3", "w1", "w2"],
        "m4": ["w1", "w4", "w3", "w2"],
        "m5": ["w1", "w2", "w4"],
    }
    school_prefs = {
        "w1": ["m2", "m3", "m1", "m4", "m5"],
        "w2": ["m3", "m1", "m2", "m4", "m5"],
        "w3": ["m5", "m4", "m1", "m2", "m3"],
        "w4": ["m1", "m4", "m5", "m2", "m3"],
    }
    capacities = {c: 1 for c in school_prefs}

    men_proposing = deferred_acceptance(student_prefs, school_prefs, capacities, proposing="students")
    check_eq(
        men_proposing.matching,
        {"m1": "w1", "m2": "w2", "m3": "w3", "m4": "w4", "m5": None},
        "Example 2.17 (Sun, 2018): DA con hombres proponiendo",
    )

    # Libro, 2.25: "the matching obtained when the women propose to the
    # men is [w4,w1,w2,w3 / m1,m2,m3,m4,(m5)]", es decir m1-w4, m2-w1,
    # m3-w2, m4-w3, m5 soltero.
    women_proposing = deferred_acceptance(student_prefs, school_prefs, capacities, proposing="schools")
    check_eq(
        women_proposing.matching,
        {"m1": "w4", "m2": "w1", "m3": "w2", "m4": "w3", "m5": None},
        "Example 2.17 (Sun, 2018): DA con mujeres proponiendo",
    )

    # Teorema de Gale-Shapley (1962): ambos resultados deben ser estables.
    stable_men, _ = is_stable(men_proposing.matching, student_prefs, school_prefs, capacities)
    check_eq(stable_men, True, "Example 2.17: estabilidad (hombres proponiendo)")
    stable_women, _ = is_stable(women_proposing.matching, student_prefs, school_prefs, capacities)
    check_eq(stable_women, True, "Example 2.17: estabilidad (mujeres proponiendo)")

    # Teorema del hospital rural (McVitie y Wilson, 1970): el conjunto de
    # agentes matcheados es el mismo en todo matching estable -- acá, m5
    # queda soltero en ambas versiones.
    check_eq(men_proposing.matching["m5"], None, "Example 2.17: rural hospital (hombres proponiendo)")
    check_eq(women_proposing.matching["m5"], None, "Example 2.17: rural hospital (mujeres proponiendo)")


# ---------------------------------------------------------------------------
# Ejemplos por defecto del portal (ya verificados a mano y en el navegador).
# ---------------------------------------------------------------------------

def test_boston_ejemplo_por_defecto_es_inestable():
    student_prefs = {"E1": ["C1", "C2", "C3"], "E2": ["C1", "C2", "C3"], "E3": ["C2", "C1", "C3"]}
    school_prefs = {"C1": ["E1", "E2", "E3"], "C2": ["E1", "E2", "E3"], "C3": ["E1", "E2", "E3"]}
    capacities = {c: 1 for c in school_prefs}

    result = boston_mechanism(student_prefs, school_prefs, capacities)
    check_eq(result.matching, {"E1": "C1", "E2": "C3", "E3": "C2"}, "Boston (ejemplo por defecto): matching")

    stable, blocking = is_stable(result.matching, student_prefs, school_prefs, capacities)
    check_eq(stable, False, "Boston (ejemplo por defecto): debe ser inestable")
    check_eq(blocking, [("E2", "C2")], "Boston (ejemplo por defecto): par bloqueante")


def test_ttc_intercambia_respecto_a_da():
    student_prefs = {"E1": ["C1", "C2", "C3"], "E2": ["C1", "C2", "C3"], "E3": ["C2", "C1", "C3"]}
    school_prefs = {"C1": ["E3", "E1", "E2"], "C2": ["E1", "E2", "E3"], "C3": ["E1", "E2", "E3"]}
    capacities = {c: 1 for c in school_prefs}

    da = deferred_acceptance(student_prefs, school_prefs, capacities, proposing="students")
    check_eq(da.matching, {"E1": "C2", "E2": "C3", "E3": "C1"}, "TTC vs DA (ejemplo trade-off): matching de DA")

    ttc = top_trading_cycles(student_prefs, school_prefs, capacities)
    check_eq(ttc.matching, {"E1": "C1", "E2": "C3", "E3": "C2"}, "TTC vs DA (ejemplo trade-off): matching de TTC")

    stable, blocking = is_stable(ttc.matching, student_prefs, school_prefs, capacities)
    check_eq(stable, False, "TTC vs DA (ejemplo trade-off): TTC debe ser inestable")
    check_eq(blocking, [("E2", "C2")], "TTC vs DA (ejemplo trade-off): par bloqueante de TTC")

    # Mejora de Pareto estricta de TTC sobre DA: E1 y E3 mejoran, E2 igual.
    ranks_da = {s: student_prefs[s].index(da.matching[s]) for s in student_prefs}
    ranks_ttc = {s: student_prefs[s].index(ttc.matching[s]) for s in student_prefs}
    check_eq(ranks_ttc["E1"] < ranks_da["E1"], True, "TTC vs DA: E1 debe mejorar con TTC")
    check_eq(ranks_ttc["E3"] < ranks_da["E3"], True, "TTC vs DA: E3 debe mejorar con TTC")
    check_eq(ranks_ttc["E2"] == ranks_da["E2"], True, "TTC vs DA: E2 debe quedar igual")


def test_house_allocation_ciclo_perfecto():
    agent_prefs = {"A1": ["H2", "H1", "H3"], "A2": ["H3", "H2", "H1"], "A3": ["H1", "H3", "H2"]}
    owner_of = {"H1": "A1", "H2": "A2", "H3": "A3"}
    house_prefs = {h: [owner_of[h]] for h in owner_of}
    capacities = {h: 1 for h in owner_of}

    result = top_trading_cycles(agent_prefs, house_prefs, capacities)
    check_eq(
        result.matching,
        {"A1": "H2", "A2": "H3", "A3": "H1"},
        "Mercado de Casas (ejemplo por defecto): ciclo perfecto de 3",
    )
    check_eq(len(result.cycles), 1, "Mercado de Casas: debe formarse un único ciclo")
    check_eq(len(result.cycles[0].path), 6, "Mercado de Casas: el ciclo debe alternar 3 agentes y 3 casas")


def test_serial_dictatorship_coincide_con_da_bajo_prioridad_comun():
    order = ["E1", "E2", "E3"]
    student_prefs = {"E1": ["C1", "C2", "C3"], "E2": ["C2", "C1", "C3"], "E3": ["C1", "C2", "C3"]}
    capacities = {"C1": 1, "C2": 1, "C3": 1}

    sd = serial_dictatorship(order, student_prefs, capacities)
    check_eq(sd.matching, {"E1": "C1", "E2": "C2", "E3": "C3"}, "Serial Dictatorship (ejemplo por defecto)")

    school_prefs = {c: order for c in capacities}
    da = deferred_acceptance(student_prefs, school_prefs, capacities, proposing="students")
    ttc = top_trading_cycles(student_prefs, school_prefs, capacities)
    check_eq(sd.matching, da.matching, "SD debe coincidir con DA bajo prioridad común")
    check_eq(sd.matching, ttc.matching, "SD debe coincidir con TTC bajo prioridad común")

    stable, _ = is_stable(sd.matching, student_prefs, school_prefs, capacities)
    check_eq(stable, True, "SD bajo prioridad común debe ser estable")


def test_kidney_exchange_ciclo_de_tres_y_largo_maximo():
    pairs = ["P1", "P2", "P3", "P4"]
    compat = {"P1": ["P2"], "P2": ["P3"], "P3": ["P1"], "P4": []}

    result_l3 = kidney_exchange(pairs, compat, max_cycle_length=3)
    check_eq(
        result_l3.matching,
        {"P1": "P3", "P2": "P1", "P3": "P2", "P4": None},
        "Kidney Exchange (ejemplo por defecto): largo máximo 3",
    )
    check_eq(len(result_l3.cycles), 1, "Kidney Exchange: debe formarse un único ciclo de 3")

    result_l2 = kidney_exchange(pairs, compat, max_cycle_length=2)
    check_eq(
        result_l2.matching,
        {"P1": None, "P2": None, "P3": None, "P4": None},
        "Kidney Exchange (ejemplo por defecto): con largo máximo 2, nadie se matchea",
    )


def test_manipulacion_boston_conviene_mentir_da_y_ttc_no():
    school_prefs = {"C1": ["E1", "E2", "E3"], "C2": ["E1", "E2", "E3"], "C3": ["E1", "E2", "E3"]}
    capacities = {c: 1 for c in school_prefs}
    true_prefs = {"E1": ["C1", "C2", "C3"], "E2": ["C1", "C2", "C3"], "E3": ["C2", "C1", "C3"]}
    manip_prefs = dict(true_prefs)
    manip_prefs["E2"] = ["C2", "C1", "C3"]

    boston_honest = boston_mechanism(true_prefs, school_prefs, capacities).matching
    boston_manip = boston_mechanism(manip_prefs, school_prefs, capacities).matching
    check_eq(boston_honest["E2"], "C3", "Manipulación en Boston: E2 honesto")
    check_eq(boston_manip["E2"], "C2", "Manipulación en Boston: E2 mintiendo mejora")

    da_honest = deferred_acceptance(true_prefs, school_prefs, capacities, proposing="students").matching
    da_manip = deferred_acceptance(manip_prefs, school_prefs, capacities, proposing="students").matching
    check_eq(da_honest["E2"], da_manip["E2"], "DA es strategy-proof: mentir no debe cambiar el resultado de E2")

    ttc_honest = top_trading_cycles(true_prefs, school_prefs, capacities).matching
    ttc_manip = top_trading_cycles(manip_prefs, school_prefs, capacities).matching
    check_eq(ttc_honest["E2"], ttc_manip["E2"], "TTC es strategy-proof: mentir no debe cambiar el resultado de E2")


def test_minority_reserve_transformacion():
    order = ["s1", "s2", "s3", "s4", "s5"]
    minorities = {"s2", "s4"}

    check_eq(
        apply_minority_reserve(order, minorities, reserve_count=1),
        ["s2", "s1", "s3", "s4", "s5"],
        "Minority reserve: reserva de 1 sube al minoritario de mayor prioridad",
    )
    check_eq(
        apply_minority_reserve(order, minorities, reserve_count=2),
        ["s2", "s4", "s1", "s3", "s5"],
        "Minority reserve: reserva de 2 sube a ambos minoritarios",
    )
    # Reserva mayor a la cantidad real de minoritarios: se satura en 2.
    check_eq(
        apply_minority_reserve(order, minorities, reserve_count=3),
        ["s2", "s4", "s1", "s3", "s5"],
        "Minority reserve: reserva que excede la cantidad de minoritarios se satura",
    )
    check_eq(
        apply_minority_reserve(order, minorities, reserve_count=0),
        order,
        "Minority reserve: reserva 0 no cambia el orden",
    )


def main():
    tests = [
        test_gale_shapley_example_2_17,
        test_boston_ejemplo_por_defecto_es_inestable,
        test_ttc_intercambia_respecto_a_da,
        test_house_allocation_ciclo_perfecto,
        test_serial_dictatorship_coincide_con_da_bajo_prioridad_comun,
        test_kidney_exchange_ciclo_de_tres_y_largo_maximo,
        test_manipulacion_boston_conviene_mentir_da_y_ttc_no,
        test_minority_reserve_transformacion,
    ]
    print(f"Corriendo {len(tests)} regression tests con resultados exactos conocidos...\n")
    for t in tests:
        print(f"  {t.__name__}...")
        t()

    print(f"\nTotal de chequeos: {checks_run}")
    if failures:
        print(f"\n❌ {len(failures)} FALLAS:\n")
        for f in failures:
            print(f" - {f}")
        sys.exit(1)
    print("\n✅ Todo OK. Ningún chequeo falló.")
    sys.exit(0)


if __name__ == "__main__":
    main()
