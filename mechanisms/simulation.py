"""Generación de mercados aleatorios y estadísticas agregadas.

Pensado para poder correr los mecanismos con muchos agentes (cientos) y
comparar resultados agregados en vez de leer el matching estudiante por
estudiante, que deja de ser legible a esa escala.
"""

import random
from dataclasses import dataclass


@dataclass
class Market:
    students: list[str]
    schools: list[str]
    capacities: dict[str, int]
    student_prefs: dict[str, list[str]]
    school_prefs: dict[str, list[str]]
    sd_order: list[str]


def _make_capacities(n_students: int, schools: list[str]) -> dict[str, int]:
    """Reparte n_students cupos entre los colegios en partes iguales. Si
    hay más colegios que estudiantes, algunos colegios quedan con 0
    cupos -- la suma siempre da exactamente n_students."""
    n_schools = len(schools)
    base, rem = divmod(n_students, n_schools)
    capacities = {}
    for i, c in enumerate(schools):
        capacities[c] = base + (1 if i < rem else 0)
    return capacities


def generate_student_preferences(
    students: list[str],
    schools: list[str],
    pref_correlation: float,
    rng: random.Random,
) -> dict[str, list[str]]:
    """pref_correlation en [0, 1]: 0 = preferencias totalmente independientes
    entre estudiantes; 1 = todos comparten exactamente el mismo orden
    (colegios "populares" comunes a todos)."""
    quality = {c: rng.random() for c in schools}
    student_prefs = {}
    for s in students:
        noise = {c: rng.random() for c in schools}
        score = {c: pref_correlation * quality[c] + (1 - pref_correlation) * noise[c] for c in schools}
        student_prefs[s] = sorted(schools, key=lambda c: -score[c])
    return student_prefs


def generate_market(
    n_students: int,
    n_schools: int,
    pref_correlation: float,
    common_priority: bool,
    seed: int | None = None,
) -> Market:
    """Genera un mercado aleatorio.

    common_priority: si es True, los colegios comparten un único orden de
    prioridad (como en Serial Dictatorship); si es False, cada colegio
    tiene una prioridad independiente sobre los estudiantes.
    """
    rng = random.Random(seed)

    students = [f"E{i+1}" for i in range(n_students)]
    schools = [f"C{i+1}" for i in range(n_schools)]
    capacities = _make_capacities(n_students, schools)

    student_prefs = generate_student_preferences(students, schools, pref_correlation, rng)

    if common_priority:
        order = list(students)
        rng.shuffle(order)
        school_prefs = {c: order for c in schools}
        sd_order = order
    else:
        school_prefs = {}
        for c in schools:
            order = list(students)
            rng.shuffle(order)
            school_prefs[c] = order
        sd_order = list(students)
        rng.shuffle(sd_order)

    return Market(
        students=students,
        schools=schools,
        capacities=capacities,
        student_prefs=student_prefs,
        school_prefs=school_prefs,
        sd_order=sd_order,
    )


def rank_of(student_prefs: dict[str, list[str]], student: str, school: str | None) -> int | None:
    if school is None:
        return None
    prefs = student_prefs[student]
    return prefs.index(school) if school in prefs else None


def rank_bucket(rank: int | None) -> str:
    if rank is None:
        return "Sin asignar"
    if rank == 0:
        return "1ª opción"
    if rank <= 2:
        return "2ª-3ª"
    if rank <= 9:
        return "4ª-10ª"
    return "11ª o peor"


def summarize(
    matching: dict[str, str | None],
    student_prefs: dict[str, list[str]],
) -> dict:
    students = list(student_prefs.keys())
    ranks = [rank_of(student_prefs, s, matching.get(s)) for s in students]
    matched_ranks = [r for r in ranks if r is not None]
    n = len(students)

    buckets = ["1ª opción", "2ª-3ª", "4ª-10ª", "11ª o peor", "Sin asignar"]
    counts = {b: 0 for b in buckets}
    for r in ranks:
        counts[rank_bucket(r)] += 1

    return {
        "n": n,
        "matched": len(matched_ranks),
        "pct_matched": len(matched_ranks) / n if n else 0.0,
        "avg_rank": sum(matched_ranks) / len(matched_ranks) if matched_ranks else None,
        "pct_top_choice": sum(1 for r in matched_ranks if r == 0) / n if n else 0.0,
        "bucket_counts": counts,
    }
