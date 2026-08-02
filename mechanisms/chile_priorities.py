"""Modelos de prioridad inspirados en el SAE (Chile) y en la reforma
propuesta en 2026, para explorar cómo distintos criterios de prioridad
afectan la composición de quién accede a los colegios más demandados.

Estos son modelos simplificados con fines pedagógicos, no una réplica
exacta del reglamento del SAE ni del proyecto de ley (todavía en
tramitación al momento de escribir esto). Ver content/chile_sae_actual.md
y content/chile_reforma_2026.md para las fuentes y aclaraciones.
"""

import random
from dataclasses import dataclass


@dataclass
class StudentAttrs:
    hermano: bool
    prioritario: bool
    funcionario: bool
    exalumno: bool
    rendimiento: float  # 0-1, señal de mérito académico


def generate_student_attrs(
    students: list[str],
    prob_hermano: float,
    prob_prioritario: float,
    prob_funcionario: float,
    prob_exalumno: float,
    correlacion_vulnerabilidad_rendimiento: float,
    rng: random.Random,
) -> dict[str, StudentAttrs]:
    """correlacion_vulnerabilidad_rendimiento en [-1, 1]: si es negativa,
    ser estudiante prioritario reduce (en promedio) la señal de
    rendimiento académico simulada -- una forma simple de representar el
    argumento, presente en el debate público, de que el rendimiento
    académico está correlacionado con el nivel socioeconómico. Es un
    supuesto de modelación ajustable, no un dato objetivo."""
    attrs = {}
    for s in students:
        prioritario = rng.random() < prob_prioritario
        base = rng.random()
        shift = -correlacion_vulnerabilidad_rendimiento * 0.3 if prioritario else 0.0
        rendimiento = min(1.0, max(0.0, base + shift))
        attrs[s] = StudentAttrs(
            hermano=rng.random() < prob_hermano,
            prioritario=prioritario,
            funcionario=rng.random() < prob_funcionario,
            exalumno=rng.random() < prob_exalumno,
            rendimiento=rendimiento,
        )
    return attrs


def build_priority_sae_actual(
    students_attrs: dict[str, StudentAttrs],
    schools: list[str],
    rng: random.Random,
) -> dict[str, list[str]]:
    """Orden de prioridad por categorías legales: hermanos > prioritarios
    (SEP) > hijos de funcionarios > exalumnos > resto. Dentro de cada
    categoría, el desempate se simula con un orden aleatorio independiente
    por colegio (en la realidad es un número fijo derivado de RUT+RBD, no
    aleatorio -- ver content/chile_sae_actual.md)."""
    tiers: list[list[str]] = [[], [], [], [], []]
    for s, a in students_attrs.items():
        if a.hermano:
            tiers[0].append(s)
        elif a.prioritario:
            tiers[1].append(s)
        elif a.funcionario:
            tiers[2].append(s)
        elif a.exalumno:
            tiers[3].append(s)
        else:
            tiers[4].append(s)

    result = {}
    for c in schools:
        order = []
        for tier in tiers:
            shuffled = list(tier)
            rng.shuffle(shuffled)
            order.extend(shuffled)
        result[c] = order
    return result


def apply_minority_reserve(order: list[str], target_group: set[str], reserve_count: int) -> list[str]:
    """Transformación de prioridad "minority reserve" (Hafalir, Yenmez y
    Yildirim, 2013): sube hasta `reserve_count` integrantes del grupo con
    cupo reservado al frente de la fila, respetando su orden relativo, y
    deja el resto (de cualquier grupo) en su orden original a continuación.
    Preserva las propiedades de DA sin tener que modificar el algoritmo."""
    reserved = [s for s in order if s in target_group][:reserve_count]
    reserved_set = set(reserved)
    rest = [s for s in order if s not in reserved_set]
    return reserved + rest


def build_priority_reforma(
    students_attrs: dict[str, StudentAttrs],
    schools: list[str],
    capacities: dict[str, int],
    peso_merito: float,
    peso_entrevista: float,
    peso_cercania: float,
    cupo_reservado_pct: float,
    rng: random.Random,
) -> dict[str, list[str]]:
    """Prioridad construida por el colegio bajo un modelo tipo "Elección
    Mutua": combina mérito académico, una señal de entrevista/adhesión al
    proyecto educativo (simulada), y cercanía territorial (simulada por
    colegio) -- con cupos reservados para estudiantes prioritarios."""
    total_weight = max(peso_merito + peso_entrevista + peso_cercania, 1e-9)
    students = list(students_attrs.keys())
    prioritario_group = {s for s, a in students_attrs.items() if a.prioritario}

    result = {}
    for c in schools:
        score = {}
        for s in students:
            entrevista = rng.random()
            cercania = rng.random()
            score[s] = (
                peso_merito * students_attrs[s].rendimiento
                + peso_entrevista * entrevista
                + peso_cercania * cercania
            ) / total_weight
        order = sorted(students, key=lambda s: -score[s])
        reserve_count = round(capacities[c] * cupo_reservado_pct)
        result[c] = apply_minority_reserve(order, prioritario_group, reserve_count)
    return result
