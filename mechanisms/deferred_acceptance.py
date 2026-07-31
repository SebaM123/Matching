"""Deferred Acceptance (Gale-Shapley), version many-to-one con cupos.

Soporta que propongan los estudiantes o los colegios. Devuelve, además del
matching final, una traza paso a paso (rondas de propuestas/rechazos) para
poder mostrar el proceso completo en la UI, no solo el resultado.
"""

from dataclasses import dataclass, field


@dataclass
class Round:
    proposer: str
    target: str
    accepted: bool
    displaced: str | None = None


@dataclass
class DAResult:
    matching: dict[str, str | None]
    rounds: list[Round] = field(default_factory=list)
    proposing_side: str = "students"


def deferred_acceptance(
    student_prefs: dict[str, list[str]],
    school_prefs: dict[str, list[str]],
    capacities: dict[str, int],
    proposing: str = "students",
) -> DAResult:
    """Ejecuta DA. `proposing` es 'students' o 'schools'.

    student_prefs[s] = lista de colegios en orden de preferencia (mejor primero)
    school_prefs[c]  = lista de estudiantes en orden de preferencia (mejor primero)
    capacities[c]    = cupos del colegio c
    """
    if proposing == "students":
        return _da_student_proposing(student_prefs, school_prefs, capacities)
    elif proposing == "schools":
        return _da_school_proposing(student_prefs, school_prefs, capacities)
    raise ValueError("proposing debe ser 'students' o 'schools'")


def _da_student_proposing(student_prefs, school_prefs, capacities) -> DAResult:
    rounds: list[Round] = []
    next_proposal_idx = {s: 0 for s in student_prefs}
    tentative: dict[str, list[str]] = {c: [] for c in capacities}
    unmatched = list(student_prefs.keys())

    school_rank = {
        c: {student: rank for rank, student in enumerate(prefs)}
        for c, prefs in school_prefs.items()
    }

    while unmatched:
        s = unmatched.pop(0)
        prefs = student_prefs[s]
        if next_proposal_idx[s] >= len(prefs):
            continue  # s se queda sin colegios a los que proponer -> no matched
        c = prefs[next_proposal_idx[s]]
        next_proposal_idx[s] += 1

        if s not in school_rank.get(c, {}):
            rounds.append(Round(proposer=s, target=c, accepted=False))
            unmatched.append(s)
            continue

        held = tentative[c]
        if len(held) < capacities[c]:
            held.append(s)
            held.sort(key=lambda x: school_rank[c][x])
            rounds.append(Round(proposer=s, target=c, accepted=True))
        else:
            worst = held[-1]
            if school_rank[c][s] < school_rank[c][worst]:
                held[-1] = s
                held.sort(key=lambda x: school_rank[c][x])
                rounds.append(Round(proposer=s, target=c, accepted=True, displaced=worst))
                unmatched.append(worst)
            else:
                rounds.append(Round(proposer=s, target=c, accepted=False))
                unmatched.append(s)

    matching: dict[str, str | None] = {s: None for s in student_prefs}
    for c, students in tentative.items():
        for s in students:
            matching[s] = c

    return DAResult(matching=matching, rounds=rounds, proposing_side="students")


def _da_school_proposing(student_prefs, school_prefs, capacities) -> DAResult:
    rounds: list[Round] = []
    next_proposal_idx = {c: 0 for c in school_prefs}
    tentative: dict[str, str | None] = {s: None for s in student_prefs}
    school_holds: dict[str, list[str]] = {c: [] for c in capacities}

    student_rank = {
        s: {school: rank for rank, school in enumerate(prefs)}
        for s, prefs in student_prefs.items()
    }

    # Cada colegio propone hasta llenar sus cupos o quedarse sin candidatos.
    active_schools = [c for c in school_prefs if capacities[c] > 0]

    while active_schools:
        c = active_schools.pop(0)
        while len(school_holds[c]) < capacities[c] and next_proposal_idx[c] < len(school_prefs[c]):
            s = school_prefs[c][next_proposal_idx[c]]
            next_proposal_idx[c] += 1

            if c not in student_rank.get(s, {}):
                rounds.append(Round(proposer=c, target=s, accepted=False))
                continue

            current = tentative[s]
            if current is None:
                tentative[s] = c
                school_holds[c].append(s)
                rounds.append(Round(proposer=c, target=s, accepted=True))
            elif student_rank[s][c] < student_rank[s][current]:
                school_holds[current].remove(s)
                if len(school_holds[current]) < capacities[current] and current not in active_schools:
                    active_schools.append(current)
                tentative[s] = c
                school_holds[c].append(s)
                rounds.append(Round(proposer=c, target=s, accepted=True, displaced=current))
            else:
                rounds.append(Round(proposer=c, target=s, accepted=False))

        if len(school_holds[c]) < capacities[c] and next_proposal_idx[c] < len(school_prefs[c]):
            active_schools.append(c)

    return DAResult(matching=tentative, rounds=rounds, proposing_side="schools")


def is_stable(
    matching: dict[str, str | None],
    student_prefs: dict[str, list[str]],
    school_prefs: dict[str, list[str]],
    capacities: dict[str, int],
) -> tuple[bool, list[tuple[str, str]]]:
    """Chequea estabilidad: sin pares bloqueantes (s, c) que se prefieran
    mutuamente por sobre su asignación actual."""
    school_rank = {
        c: {student: rank for rank, student in enumerate(prefs)}
        for c, prefs in school_prefs.items()
    }
    occupants: dict[str, list[str]] = {c: [] for c in capacities}
    for s, c in matching.items():
        if c is not None:
            occupants[c].append(s)

    blocking_pairs = []
    for s, prefs in student_prefs.items():
        current = matching.get(s)
        current_rank = prefs.index(current) if current in prefs else len(prefs)
        for c in prefs[:current_rank]:  # colegios que s prefiere a su asignación actual
            if s not in school_rank.get(c, {}):
                continue
            held = occupants[c]
            if len(held) < capacities[c]:
                blocking_pairs.append((s, c))
            else:
                worst = max(held, key=lambda x: school_rank[c][x])
                if school_rank[c][s] < school_rank[c][worst]:
                    blocking_pairs.append((s, c))

    return (len(blocking_pairs) == 0, blocking_pairs)
