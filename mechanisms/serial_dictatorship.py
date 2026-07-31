"""Serial Dictatorship (SD).

El mecanismo más simple de todos: hay un único orden de prioridad exógeno
sobre los estudiantes (ej. un sorteo, un puntaje de examen), sin prioridad
propia de cada colegio. En ese orden, cada estudiante elige, en su turno,
el colegio que más prefiere entre los que todavía tienen cupo.

Es, literalmente, un caso particular de Top Trading Cycles donde todos los
colegios comparten la misma prioridad (el orden dado): en ese caso los
ciclos que forma TTC son siempre triviales (un estudiante y el colegio que
elige), y el resultado coincide con el de correr los estudiantes uno por
uno en orden de prioridad.
"""

from dataclasses import dataclass, field


@dataclass
class Pick:
    student: str
    chosen: str | None


@dataclass
class SDResult:
    matching: dict[str, str | None]
    picks: list[Pick] = field(default_factory=list)


def serial_dictatorship(
    order: list[str],
    student_prefs: dict[str, list[str]],
    capacities: dict[str, int],
) -> SDResult:
    remaining_capacity = dict(capacities)
    matching: dict[str, str | None] = {s: None for s in order}
    picks: list[Pick] = []

    for s in order:
        chosen = None
        for c in student_prefs.get(s, []):
            if remaining_capacity.get(c, 0) > 0:
                chosen = c
                break
        if chosen is not None:
            matching[s] = chosen
            remaining_capacity[chosen] -= 1
        picks.append(Pick(student=s, chosen=chosen))

    return SDResult(matching=matching, picks=picks)
