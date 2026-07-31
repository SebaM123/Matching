"""Mecanismo de Boston (Immediate Acceptance).

A diferencia de Deferred Acceptance, las aceptaciones acá son
**inmediatas y permanentes**: si un colegio acepta a un estudiante en una
ronda, ese lugar queda cerrado para siempre, aunque en una ronda futura
se presente un estudiante con mayor prioridad para ese colegio.
Esa es exactamente la propiedad que puede romper la estabilidad.
"""

from dataclasses import dataclass, field


@dataclass
class Round:
    school: str
    accepted: list[str]
    rejected: list[str]


@dataclass
class BostonResult:
    matching: dict[str, str | None]
    rounds: list[Round] = field(default_factory=list)


def boston_mechanism(
    student_prefs: dict[str, list[str]],
    school_prefs: dict[str, list[str]],
    capacities: dict[str, int],
) -> BostonResult:
    school_rank = {
        c: {student: rank for rank, student in enumerate(prefs)}
        for c, prefs in school_prefs.items()
    }
    remaining_capacity = dict(capacities)
    matching: dict[str, str | None] = {s: None for s in student_prefs}
    proposal_idx = {s: 0 for s in student_prefs}
    rounds: list[Round] = []

    active = list(student_prefs.keys())

    while active:
        proposals_by_school: dict[str, list[str]] = {}
        still_active = []

        for s in active:
            idx = proposal_idx[s]
            if idx >= len(student_prefs[s]):
                continue  # sin más colegios a los que proponer: queda sin asignar
            c = student_prefs[s][idx]
            proposal_idx[s] += 1
            proposals_by_school.setdefault(c, []).append(s)
            still_active.append(s)

        active = still_active
        next_active = []

        for c, applicants in proposals_by_school.items():
            acceptable = [s for s in applicants if s in school_rank.get(c, {})]
            unacceptable = [s for s in applicants if s not in school_rank.get(c, {})]
            acceptable.sort(key=lambda s: school_rank[c][s])

            slots = remaining_capacity.get(c, 0)
            accepted = acceptable[:slots]
            rejected = acceptable[slots:] + unacceptable

            for s in accepted:
                matching[s] = c
                remaining_capacity[c] -= 1

            rounds.append(Round(school=c, accepted=accepted, rejected=rejected))
            next_active.extend(rejected)

        active = next_active

    return BostonResult(matching=matching, rounds=rounds)
