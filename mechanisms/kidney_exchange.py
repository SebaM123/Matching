"""Kidney Exchange: matching de parejas paciente-donante incompatibles.

A diferencia de los mecanismos anteriores, acá no hay "preferencias
ordenadas" en el mismo sentido: cada pareja (paciente, donante) es
incompatible entre sí, y lo único que importa es un grafo de
**compatibilidad** — qué pacientes podrían recibir el riñón de qué otros
donantes. El mecanismo busca **ciclos de intercambio**: secuencias de
parejas donde cada donante dona al paciente de la siguiente pareja del
ciclo, y el de la última dona al primero, cerrando el círculo. Así nadie
dona sin que su ser querido reciba un riñón a cambio, todo en el mismo
momento.

Por una restricción logística real (todas las cirugías de un ciclo deben
hacerse en simultáneo, para que nadie done sin recibir), los ciclos se
limitan en la práctica a un largo máximo (típicamente 2 o 3).

El objetivo del mecanismo es maximizar la cantidad de parejas
efectivamente intercambiadas, eligiendo un conjunto de ciclos
*disjuntos* (cada pareja participa en, a lo sumo, un ciclo).
"""

from dataclasses import dataclass, field
from itertools import combinations


@dataclass
class Cycle:
    pairs: list[str]  # p1 -> p2 -> ... -> pk -> p1 (donante de p_i dona al paciente de p_{i+1})


@dataclass
class KidneyResult:
    matching: dict[str, str | None]  # pareja -> pareja de quien recibe el riñón (o None)
    cycles: list[Cycle] = field(default_factory=list)


def _canonical(cycle: list[str]) -> tuple[str, ...]:
    """Rotación canónica para no contar el mismo ciclo dos veces."""
    n = len(cycle)
    best = None
    for i in range(n):
        rotated = tuple(cycle[i:] + cycle[:i])
        if best is None or rotated < best:
            best = rotated
    return best


def _find_all_cycles(pairs: list[str], compat: dict[str, list[str]], max_len: int) -> list[list[str]]:
    """DFS: todos los ciclos dirigidos simples de largo 2..max_len."""
    seen: set[tuple[str, ...]] = set()
    cycles: list[list[str]] = []

    def dfs(start: str, current: str, path: list[str]):
        if len(path) > max_len:
            return
        for nxt in compat.get(current, []):
            if nxt == start and len(path) >= 2:
                canon = _canonical(path)
                if canon not in seen:
                    seen.add(canon)
                    cycles.append(list(path))
            elif nxt not in path and len(path) < max_len:
                dfs(start, nxt, path + [nxt])

    for p in pairs:
        dfs(p, p, [p])

    return cycles


def kidney_exchange(
    pairs: list[str],
    compat: dict[str, list[str]],
    max_cycle_length: int = 3,
) -> KidneyResult:
    all_cycles = _find_all_cycles(pairs, compat, max_cycle_length)
    # Priorizar ciclos más cortos primero: son logísticamente más simples
    # y ayuda a que la búsqueda encuentre buenas soluciones rápido.
    all_cycles.sort(key=len)

    best: dict[str, object] = {"chosen": [], "matched": 0}

    def backtrack(idx: int, chosen: list[list[str]], used: set[str], matched: int):
        remaining_capacity = sum(len(c) for c in all_cycles[idx:] if not (set(c) & used))
        if matched + remaining_capacity <= best["matched"]:
            return
        if matched > best["matched"]:
            best["chosen"] = list(chosen)
            best["matched"] = matched
        if idx >= len(all_cycles):
            return
        cycle = all_cycles[idx]
        # Rama 1: no usar este ciclo
        backtrack(idx + 1, chosen, used, matched)
        # Rama 2: usar este ciclo, si es disjunto de lo ya elegido
        if not (set(cycle) & used):
            backtrack(idx + 1, chosen + [cycle], used | set(cycle), matched + len(cycle))

    backtrack(0, [], set(), 0)

    matching: dict[str, str | None] = {p: None for p in pairs}
    cycles_result: list[Cycle] = []
    for cycle in best["chosen"]:
        n = len(cycle)
        for i, p in enumerate(cycle):
            receives_from = cycle[i - 1]  # el anterior en el ciclo le dona
            matching[p] = receives_from
        cycles_result.append(Cycle(pairs=cycle))

    return KidneyResult(matching=matching, cycles=cycles_result)
