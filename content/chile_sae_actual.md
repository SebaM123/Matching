## El Sistema de Admisión Escolar (SAE) en Chile

Chile tiene, desde la Ley de Inclusión Escolar (2015), un sistema
centralizado de admisión a colegios que reciben financiamiento público
(públicos y particulares subvencionados): el **Sistema de Admisión
Escolar (SAE)**. Es, en esencia, una implementación real de todo lo que
viste en las páginas de Deferred Acceptance y Definiciones — con una
diferencia importante: **la prioridad de cada colegio no es una
preferencia propia del colegio, sino una fórmula fijada por ley.**

### Los criterios de prioridad legales

A diferencia del ejemplo genérico de este portal (donde cada colegio
tiene su propio ranking de estudiantes), en el SAE el orden de prioridad
dentro de cada colegio se arma combinando categorías fijadas por ley,
en este orden aproximado (el orden exacto entre categorías puede variar
según el reglamento vigente — la fuente oficial y actualizada es
[Ayuda Mineduc — Criterios de prioridad](https://www.ayudamineduc.cl/ficha/criterios-de-prioridad)):

1. **Hermanos**: estudiantes con hermanos ya matriculados en el
   establecimiento.
2. **Estudiantes prioritarios**: estudiantes que pertenecen al 40% más
   vulnerable según el Registro Social de Hogares, en colegios con
   Subvención Escolar Preferencial (SEP).
3. **Hijos de funcionarios** del establecimiento.
4. **Exalumnos**: postulantes que ya asistieron a ese colegio (y no
   fueron expulsados).

Dentro de cada categoría, si hay más postulantes que cupos, hasta la
admisión 2026 el desempate se resolvía por **sorteo aleatorio**. Desde
2026, el desempate pasó a resolverse con un **número fijo y
determinístico** derivado del RUT del postulante y el RBD del colegio —
buscando trazabilidad y objetividad en vez de aleatoriedad (fuente:
[La Tercera](https://www.latercera.com/videos/noticia/adios-a-la-tombola-educacion-presenta-moderno-algoritmo-para-la-admision-escolar-2026/)).

### ¿Qué mecanismo usa el SAE?

El algoritmo del SAE es, en esencia, **Deferred Acceptance** (los
mismos principios que viste en la primera página de este portal):
las familias postulan con una lista ordenada de colegios, y el sistema
corre el algoritmo de aceptación diferida para encontrar una asignación
estable respecto a esas prioridades legales.

### Dónde esto "distorsiona" la teoría genérica

Todo lo que viste sobre estabilidad, optimalidad y strategy-proofness
sigue aplicando exactamente igual — DA sigue siendo estable respecto a
la prioridad que se use. Lo que cambia, y es la parte políticamente
relevante, es **qué prioridad se usa**:

- La prioridad **no representa una preferencia genuina del colegio**
  (a diferencia del modelo "college admissions" donde el colegio
  realmente prefiere a ciertos estudiantes) — es una política pública
  que persigue objetivos explícitos: no separar hermanos, proteger a
  estudiantes en situación de vulnerabilidad (SEP), reconocer vínculos
  laborales del personal, y dar continuidad a exalumnos.
- Cada categoría tiene un fundamento distinto: **hermanos** busca
  cohesión familiar; **prioritarios (SEP)** es una acción afirmativa
  explícita para estudiantes vulnerables; **hijos de funcionarios** es
  un beneficio laboral; **exalumnos** da continuidad.
- El orden entre estas categorías es, en el fondo, una decisión de
  **diseño de mercado con consecuencias distributivas** — no hay una
  respuesta "neutral": priorizar más a "prioritarios" favorece
  integración socioeconómica; priorizar más a "hermanos" o "hijos de
  funcionarios" tiende a favorecer la continuidad de redes ya
  existentes.

### Para explorar en el simulador

En la pestaña **Simulador comparativo** de esta sección podés generar
estudiantes sintéticos con estos mismos atributos (hermano, prioritario
SEP, hijo de funcionario, exalumno) y ver cómo la prioridad que arma el
SAE actual determina quién accede a los colegios más demandados —
antes de comparar con la reforma que se explica en la próxima pestaña.
