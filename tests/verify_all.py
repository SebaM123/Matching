"""Batería de verificación de todos los mecanismos sobre muchos
escenarios aleatorios.

No es una suite de pytest -- es un script standalone (correr con
`python3 tests/verify_all.py`) que genera cientos de instancias al azar
por mecanismo, chequea invariantes matemáticas conocidas (buena
formación, estabilidad, eficiencia de Pareto, racionalidad individual,
optimalidad exacta vía fuerza bruta en instancias chicas), y reporta un
resumen de fallas al final en vez de frenar en el primer error.
"""

import itertools
import random
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from mechanisms.boston import boston_mechanism
from mechanisms.chile_priorities import (
    build_priority_reforma,
    build_priority_sae_actual,
    generate_student_attrs,
)
from mechanisms.deferred_acceptance import deferred_acceptance, is_stable
from mechanisms.kidney_exchange import kidney_exchange
from mechanisms.serial_dictatorship import serial_dictatorship
from mechanisms.simulation import _make_capacities, generate_market, generate_student_preferences, rank_of, summarize
from mechanisms.ttc import top_trading_cycles

failures: list[str] = []
checks_run = 0


def check(condition: bool, message: str):
    global checks_run
    checks_run += 1
    if not condition:
        failures.append(message)


def random_prefs(rng, agents, options, full=True):
    prefs = {}
    for a in agents:
        opts = list(options)
        rng.shuffle(opts)
        if not full:
            k = rng.randint(1, len(opts))
            opts = opts[:k]
        prefs[a] = opts
    return prefs


def random_instance(rng, max_students=8, max_schools=4, full_prefs=True):
    n_students = rng.randint(1, max_students)
    n_schools = rng.randint(1, max_schools)
    students = [f"E{i+1}" for i in range(n_students)]
    schools = [f"C{i+1}" for i in range(n_schools)]
    capacities = {c: rng.randint(1, max(1, n_students // n_schools + 1)) for c in schools}
    student_prefs = random_prefs(rng, students, schools, full=full_prefs)
    school_prefs = random_prefs(rng, schools, students, full=full_prefs)
    return students, schools, capacities, student_prefs, school_prefs


def well_formed(matching, capacities, student_prefs, label):
    seen_by_school = {}
    for s, c in matching.items():
        if c is None:
            continue
        check(c in student_prefs[s], f"[{label}] {s} asignado a {c} que no estaba en su lista de preferencias")
        seen_by_school[c] = seen_by_school.get(c, 0) + 1
    for c, count in seen_by_school.items():
        check(count <= capacities[c], f"[{label}] colegio {c} recibió {count} estudiantes, cupo era {capacities[c]}")


def rank_of_local(prefs, school):
    if school is None or school not in prefs:
        return len(prefs)
    return prefs.index(school)


def is_pareto_efficient_bruteforce(matching, students, schools, capacities, student_prefs, school_prefs=None):
    """Sólo tratable para instancias muy chicas: prueba todas las
    asignaciones factibles (respetando cupos, y sólo a pares
    mutuamente aceptables -- si se pasa school_prefs, un estudiante
    fuera de la lista de un colegio no puede serle asignado, igual que
    en TTC/DA) y busca alguna que domine en Pareto al matching dado."""
    current_ranks = {s: rank_of_local(student_prefs[s], matching.get(s)) for s in students}

    school_list = schools + [None]
    all_assignments = itertools.product(school_list, repeat=len(students))
    for assignment in all_assignments:
        candidate = dict(zip(students, assignment))
        load = {}
        feasible = True
        for s, c in candidate.items():
            if c is None:
                continue
            if c not in student_prefs[s]:
                feasible = False
                break
            if school_prefs is not None and s not in school_prefs.get(c, []):
                feasible = False
                break
            load[c] = load.get(c, 0) + 1
            if load[c] > capacities[c]:
                feasible = False
                break
        if not feasible:
            continue
        weakly_better_all = True
        strictly_better_some = False
        for s in students:
            r_new = rank_of_local(student_prefs[s], candidate[s])
            r_old = current_ranks[s]
            if r_new > r_old:
                weakly_better_all = False
                break
            if r_new < r_old:
                strictly_better_some = True
        if weakly_better_all and strictly_better_some:
            return False, candidate
    return True, None


def fuzz_da(trials=300, seed=0):
    rng = random.Random(seed)
    for _ in range(trials):
        students, schools, capacities, student_prefs, school_prefs = random_instance(rng, full_prefs=rng.random() > 0.3)
        for side in ["students", "schools"]:
            result = deferred_acceptance(student_prefs, school_prefs, capacities, proposing=side)
            well_formed(result.matching, capacities, student_prefs, f"DA-{side}")
            stable, blocking = is_stable(result.matching, student_prefs, school_prefs, capacities)
            check(stable, f"DA-{side} produjo un matching inestable: blocking={blocking}")


def fuzz_boston(trials=300, seed=1):
    rng = random.Random(seed)
    for _ in range(trials):
        students, schools, capacities, student_prefs, school_prefs = random_instance(rng, full_prefs=rng.random() > 0.3)
        result = boston_mechanism(student_prefs, school_prefs, capacities)
        well_formed(result.matching, capacities, student_prefs, "Boston")
        for s in students:
            if result.matching.get(s) is not None:
                check(result.matching[s] in student_prefs[s], f"Boston asignó a {s} algo fuera de su lista")


def fuzz_ttc(trials=300, seed=2, bruteforce_trials=60):
    rng = random.Random(seed)
    for i in range(trials):
        students, schools, capacities, student_prefs, school_prefs = random_instance(rng, full_prefs=rng.random() > 0.3)
        result = top_trading_cycles(student_prefs, school_prefs, capacities)
        well_formed(result.matching, capacities, student_prefs, "TTC")
        if i < bruteforce_trials and len(students) <= 4 and len(schools) <= 3:
            efficient, dominator = is_pareto_efficient_bruteforce(
                result.matching, students, schools, capacities, student_prefs, school_prefs
            )
            check(efficient, f"TTC NO es Pareto eficiente en instancia {students, schools, capacities, student_prefs, school_prefs}: lo domina {dominator}")


def fuzz_serial_dictatorship(trials=300, seed=3):
    rng = random.Random(seed)
    for _ in range(trials):
        students, schools, capacities, student_prefs, _ = random_instance(rng, full_prefs=rng.random() > 0.3)
        order = list(students)
        rng.shuffle(order)
        result = serial_dictatorship(order, student_prefs, capacities)
        well_formed(result.matching, capacities, student_prefs, "SerialDictatorship")
        # Cada estudiante, en su turno, debería obtener su colegio favorito
        # disponible en ESE momento -- lo verificamos reproduciendo el
        # remanente de cupos manualmente.
        remaining = dict(capacities)
        for s in order:
            assigned = result.matching[s]
            if assigned is not None:
                check(remaining[assigned] > 0, f"SD asignó {s} a {assigned} sin cupo remanente")
                # Nada preferido a `assigned` con cupo disponible debería existir
                idx = student_prefs[s].index(assigned) if assigned in student_prefs[s] else None
                check(idx is not None, f"SD asignó {s} a algo fuera de su lista")
                for better in student_prefs[s][: idx if idx is not None else 0]:
                    check(remaining.get(better, 0) <= 0, f"SD asignó {s} a {assigned} habiendo cupo en {better}, que prefería más")
                remaining[assigned] -= 1


def fuzz_house_allocation(trials=200, seed=4, bruteforce_trials=60):
    rng = random.Random(seed)
    for i in range(trials):
        n = rng.randint(2, 6)
        agents = [f"A{j+1}" for j in range(n)]
        houses = [f"H{j+1}" for j in range(n)]
        owner_of = {houses[j]: agents[j] for j in range(n)}
        agent_prefs = random_prefs(rng, agents, houses, full=True)
        house_prefs = {h: [owner_of[h]] for h in houses}
        capacities = {h: 1 for h in houses}

        result = top_trading_cycles(agent_prefs, house_prefs, capacities)
        well_formed(result.matching, capacities, agent_prefs, "HouseAllocation")

        for j, a in enumerate(agents):
            own_house = houses[j]
            got = result.matching.get(a)
            check(got is not None, f"HouseAllocation dejó a {a} sin casa (no debería pasar con listas completas)")
            r_new = rank_of_local(agent_prefs[a], got)
            r_own = rank_of_local(agent_prefs[a], own_house)
            check(r_new <= r_own, f"HouseAllocation violó racionalidad individual: {a} terminó peor que con su propia casa")

        if i < bruteforce_trials and n <= 4:
            efficient, dominator = is_pareto_efficient_bruteforce(
                result.matching, agents, houses, capacities, agent_prefs
            )
            check(efficient, f"HouseAllocation NO es Pareto eficiente: {agent_prefs} -> lo domina {dominator}")


def bruteforce_max_kidney_matches(pairs, compat, max_len):
    """Fuerza bruta independiente: prueba TODAS las particiones en ciclos
    válidos (largo 2..max_len) y devuelve el máximo de parejas
    trasplantables, para comparar contra el resultado del algoritmo."""
    n = len(pairs)
    best = 0

    def is_valid_cycle(cycle):
        for i in range(len(cycle)):
            if cycle[(i + 1) % len(cycle)] not in compat.get(cycle[i], []):
                return False
        return True

    def backtrack(remaining, matched_count):
        nonlocal best
        best = max(best, matched_count)
        remaining = list(remaining)
        if not remaining:
            return
        # Rama 1: remaining[0] no participa de ningún ciclo.
        backtrack(remaining[1:], matched_count)
        # Rama 2: remaining[0] participa de algún ciclo de largo 2..max_len.
        for size in range(2, min(max_len, len(remaining)) + 1):
            for combo in itertools.permutations(remaining[1:], size - 1):
                cycle = (remaining[0],) + combo
                if is_valid_cycle(cycle):
                    rest = [p for p in remaining if p not in cycle]
                    backtrack(rest, matched_count + size)

    backtrack(pairs, 0)
    return best


def fuzz_kidney_exchange(trials=150, seed=5, bruteforce_trials=60):
    rng = random.Random(seed)
    for i in range(trials):
        n = rng.randint(2, 6)
        pairs = [f"P{j+1}" for j in range(n)]
        compat = {p: [q for q in pairs if q != p and rng.random() < 0.35] for p in pairs}
        max_len = rng.randint(2, 3)

        result = kidney_exchange(pairs, compat, max_cycle_length=max_len)

        matched_values = [v for v in result.matching.values() if v is not None]
        check(len(matched_values) == len(set(matched_values)), "KidneyExchange usó la misma pareja donante dos veces")
        for p, donor in result.matching.items():
            if donor is not None:
                check(p in compat.get(donor, []), f"KidneyExchange asignó a {p} un riñón incompatible de {donor}")
        for cyc in result.cycles:
            check(2 <= len(cyc.pairs) <= max_len, f"Ciclo de largo inválido: {cyc.pairs}")
            check(len(set(cyc.pairs)) == len(cyc.pairs), f"Ciclo con parejas repetidas: {cyc.pairs}")

        n_matched = len(matched_values)
        if i < bruteforce_trials and n <= 6:
            optimal = bruteforce_max_kidney_matches(pairs, compat, max_len)
            check(n_matched == optimal, f"KidneyExchange no encontró el óptimo: encontró {n_matched}, óptimo real {optimal} (compat={compat}, max_len={max_len})")


def fuzz_chile_priorities(trials=100, seed=6):
    rng = random.Random(seed)
    for _ in range(trials):
        n_students = rng.randint(5, 60)
        n_schools = rng.randint(2, 10)
        students = [f"E{i+1}" for i in range(n_students)]
        schools = [f"C{i+1}" for i in range(n_schools)]
        capacities = _make_capacities(n_students, schools)

        attrs = generate_student_attrs(
            students,
            prob_hermano=rng.random() * 0.3,
            prob_prioritario=rng.random(),
            prob_funcionario=rng.random() * 0.1,
            prob_exalumno=rng.random() * 0.2,
            correlacion_vulnerabilidad_rendimiento=rng.uniform(-1, 1),
            rng=rng,
        )
        check(len(attrs) == n_students, "generate_student_attrs perdió o duplicó estudiantes")
        for s, a in attrs.items():
            check(0.0 <= a.rendimiento <= 1.0, f"rendimiento fuera de rango para {s}: {a.rendimiento}")

        sae_prefs = build_priority_sae_actual(attrs, schools, rng)
        for c, order in sae_prefs.items():
            check(sorted(order) == sorted(students), f"Prioridad SAE para {c} no es una permutación completa de estudiantes")
            check(len(set(order)) == len(order), f"Prioridad SAE para {c} tiene estudiantes repetidos")
            # Nadie de menor categoría legal puede aparecer antes que uno de mayor categoría
            tier = {"hermano": 0, "prioritario": 1, "funcionario": 2, "exalumno": 3, "resto": 4}

            def tier_of(s):
                a = attrs[s]
                if a.hermano:
                    return 0
                if a.prioritario:
                    return 1
                if a.funcionario:
                    return 2
                if a.exalumno:
                    return 3
                return 4

            tiers_in_order = [tier_of(s) for s in order]
            check(tiers_in_order == sorted(tiers_in_order), f"Prioridad SAE para {c} no respeta el orden de categorías legales")

        reforma_prefs = build_priority_reforma(
            attrs, schools, capacities,
            peso_merito=rng.random(), peso_entrevista=rng.random(), peso_cercania=rng.random(),
            cupo_reservado_pct=rng.random() * 0.5, rng=rng,
        )
        for c, order in reforma_prefs.items():
            check(sorted(order) == sorted(students), f"Prioridad Reforma para {c} no es una permutación completa de estudiantes")
            check(len(set(order)) == len(order), f"Prioridad Reforma para {c} tiene estudiantes repetidos")


def fuzz_simulation_module(trials=100, seed=7):
    rng = random.Random(seed)
    for _ in range(trials):
        n_students = rng.randint(3, 100)
        n_schools = rng.randint(1, 20)
        market = generate_market(
            n_students=n_students,
            n_schools=n_schools,
            pref_correlation=rng.random(),
            common_priority=rng.random() > 0.5,
            seed=rng.randint(0, 10**6),
        )
        check(sum(market.capacities.values()) == n_students, "Los cupos generados no suman la cantidad de estudiantes")
        for s in market.students:
            check(sorted(market.student_prefs[s]) == sorted(market.schools), f"Preferencias incompletas para {s}")
        for c in market.schools:
            check(sorted(market.school_prefs[c]) == sorted(market.students), f"Prioridad incompleta para {c}")

        result = deferred_acceptance(market.student_prefs, market.school_prefs, market.capacities, proposing="students")
        summ = summarize(result.matching, market.student_prefs)
        check(summ["matched"] + sum(1 for v in result.matching.values() if v is None) == n_students, "summarize no cuadra con n_students")
        total_bucket = sum(summ["bucket_counts"].values())
        check(total_bucket == n_students, f"Los buckets de ranking no suman n_students: {total_bucket} != {n_students}")


def large_scale_smoke(sizes=(200, 500, 1000, 2000)):
    for n in sizes:
        n_schools = max(2, n // 10)
        t0 = time.time()
        market = generate_market(n_students=n, n_schools=n_schools, pref_correlation=0.7, common_priority=False, seed=123)
        da = deferred_acceptance(market.student_prefs, market.school_prefs, market.capacities, proposing="students")
        stable, blocking = is_stable(da.matching, market.student_prefs, market.school_prefs, market.capacities)
        bos = boston_mechanism(market.student_prefs, market.school_prefs, market.capacities)
        ttc = top_trading_cycles(market.student_prefs, market.school_prefs, market.capacities)
        sd = serial_dictatorship(market.sd_order, market.student_prefs, market.capacities)
        elapsed = time.time() - t0
        check(stable, f"DA inestable a escala n={n}")
        for name, res in [("DA", da.matching), ("Boston", bos.matching), ("TTC", ttc.matching), ("SD", sd.matching)]:
            well_formed(res, market.capacities, market.student_prefs, f"escala-{name}-n{n}")
        print(f"  n={n}: OK en {elapsed:.2f}s (DA estable={stable}, blocking={len(blocking)})")


def test_more_schools_than_students():
    """Caso puntual: más colegios que estudiantes -> algunos colegios
    quedan con 0 cupos. No debería explotar en ningún mecanismo, y los
    cupos deben seguir sumando exactamente n_students."""
    n_students, n_schools = 3, 10
    students = [f"E{i+1}" for i in range(n_students)]
    schools = [f"C{i+1}" for i in range(n_schools)]
    capacities = _make_capacities(n_students, schools)
    check(sum(capacities.values()) == n_students, "Caso colegios>estudiantes: los cupos no suman n_students")
    check(sum(1 for v in capacities.values() if v == 0) > 0, "Caso colegios>estudiantes: se esperaba al menos un colegio con 0 cupos")

    rng = random.Random(99)
    student_prefs = random_prefs(rng, students, schools, full=True)
    school_prefs = random_prefs(rng, schools, students, full=True)

    for side in ["students", "schools"]:
        result = deferred_acceptance(student_prefs, school_prefs, capacities, proposing=side)
        well_formed(result.matching, capacities, student_prefs, f"cero-cupo-DA-{side}")
    well_formed(boston_mechanism(student_prefs, school_prefs, capacities).matching, capacities, student_prefs, "cero-cupo-Boston")
    well_formed(top_trading_cycles(student_prefs, school_prefs, capacities).matching, capacities, student_prefs, "cero-cupo-TTC")
    well_formed(serial_dictatorship(students, student_prefs, capacities).matching, capacities, student_prefs, "cero-cupo-SD")


def main():
    print("Corriendo verificación con muchos escenarios aleatorios por mecanismo...\n")

    print("Deferred Acceptance (300 instancias x 2 lados proponiendo)...")
    fuzz_da()
    print("Boston (300 instancias)...")
    fuzz_boston()
    print("TTC (300 instancias + 60 con verificación de Pareto-eficiencia por fuerza bruta)...")
    fuzz_ttc()
    print("Serial Dictatorship (300 instancias)...")
    fuzz_serial_dictatorship()
    print("House Allocation (200 instancias + IR + 60 con Pareto por fuerza bruta)...")
    fuzz_house_allocation()
    print("Kidney Exchange (150 instancias + 60 con optimalidad por fuerza bruta)...")
    fuzz_kidney_exchange()
    print("Prioridades Chile (SAE actual + Reforma, 100 instancias)...")
    fuzz_chile_priorities()
    print("Módulo de simulación masiva (100 instancias, tamaños variables)...")
    fuzz_simulation_module()
    print("Prueba de escala (200 a 2000 estudiantes)...")
    large_scale_smoke()
    print("Caso puntual: más colegios que estudiantes (cupo 0)...")
    test_more_schools_than_students()

    print(f"\nTotal de chequeos: {checks_run}")
    if failures:
        print(f"\n❌ {len(failures)} FALLAS encontradas:\n")
        for f in failures[:50]:
            print(f" - {f}")
        if len(failures) > 50:
            print(f" ... y {len(failures) - 50} más")
        sys.exit(1)
    else:
        print("\n✅ Todo OK. Ningún chequeo falló.")
        sys.exit(0)


if __name__ == "__main__":
    main()
