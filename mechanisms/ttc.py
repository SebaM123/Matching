"""Top Trading Cycles (TTC), versión school choice (Abdulkadiroglu-Sonmez 2003).

Cada colegio "apunta" a su estudiante remanente de mayor prioridad. Cada
estudiante remanente "apunta" a su colegio remanente más preferido. Como
cada nodo (estudiante o colegio) apunta a exactamente un nodo, siempre
existe al menos un ciclo. Todos los estudiantes en un ciclo quedan
asignados al colegio al que apuntan, y son removidos (junto con los
colegios que agotan su cupo). Se repite hasta que no queden estudiantes
o no queden colegios con cupo.

A diferencia de Deferred Acceptance, TTC prioriza la eficiencia de Pareto
y la strategy-proofness por sobre la estabilidad: el resultado puede tener
pares bloqueantes.
"""

from dataclasses import dataclass, field


@dataclass
class Cycle:
    path: list[str]  # alterna estudiante, colegio, estudiante, colegio...
    assignments: dict[str, str]  # estudiante -> colegio asignado en este ciclo


@dataclass
class TTCResult:
    matching: dict[str, str | None]
    cycles: list[Cycle] = field(default_factory=list)


def top_trading_cycles(
    student_prefs: dict[str, list[str]],
    school_prefs: dict[str, list[str]],
    capacities: dict[str, int],
) -> TTCResult:
    matching: dict[str, str | None] = {s: None for s in student_prefs}
    remaining_students = set(student_prefs.keys())
    remaining_capacity = dict(capacities)
    remaining_schools = {c for c in capacities if remaining_capacity[c] > 0}

    student_idx = {s: 0 for s in student_prefs}
    cycles: list[Cycle] = []

    def next_school_pointer(s: str) -> str | None:
        prefs = student_prefs[s]
        idx = student_idx[s]
        while idx < len(prefs):
            if prefs[idx] in remaining_schools:
                student_idx[s] = idx
                return prefs[idx]
            idx += 1
        student_idx[s] = idx
        return None

    def top_priority_pointer(c: str) -> str | None:
        for s in school_prefs.get(c, []):
            if s in remaining_students:
                return s
        return None

    while remaining_students and remaining_schools:
        # Remover estudiantes que ya agotaron sus opciones (quedan sin asignar).
        exhausted = [s for s in remaining_students if next_school_pointer(s) is None]
        if exhausted:
            for s in exhausted:
                remaining_students.discard(s)
            continue

        # Remover colegios sin ningún postulante remanente aceptable.
        schools_without_applicants = [
            c for c in remaining_schools if top_priority_pointer(c) is None
        ]
        if schools_without_applicants:
            for c in schools_without_applicants:
                remaining_schools.discard(c)
            continue

        student_pointer = {s: next_school_pointer(s) for s in remaining_students}
        school_pointer = {c: top_priority_pointer(c) for c in remaining_schools}

        start = next(iter(remaining_students))
        path: list[str] = [start]
        position = {start: 0}
        current: str = start
        is_student_turn = True

        while True:
            nxt = student_pointer[current] if is_student_turn else school_pointer[current]
            if nxt in position:
                cycle_start = position[nxt]
                cycle_nodes = path[cycle_start:]
                break
            path.append(nxt)
            position[nxt] = len(path) - 1
            current = nxt
            is_student_turn = not is_student_turn

        # Cada estudiante del ciclo se asigna al nodo siguiente (su colegio
        # apuntado); se identifica por pertenecer a student_pointer, sin
        # asumir en qué posición del ciclo arranca la alternancia.
        n = len(cycle_nodes)
        assignments = {
            node: cycle_nodes[(i + 1) % n]
            for i, node in enumerate(cycle_nodes)
            if node in student_pointer
        }

        for s, c in assignments.items():
            matching[s] = c
            remaining_capacity[c] -= 1
            remaining_students.discard(s)
            if remaining_capacity[c] <= 0:
                remaining_schools.discard(c)

        cycles.append(Cycle(path=cycle_nodes, assignments=assignments))

    return TTCResult(matching=matching, cycles=cycles)
