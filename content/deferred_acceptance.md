## ¿Qué es Deferred Acceptance?

**Deferred Acceptance (DA)**, o algoritmo de Gale-Shapley (1962), es el mecanismo
central de la teoría de matching. Resuelve el problema de asignar dos lados
(por ejemplo estudiantes y colegios) cuando ambos lados tienen preferencias
sobre el otro.

La idea clave: las aceptaciones son **tentativas**, no definitivas — de ahí el
nombre "diferida". Nadie queda confirmado hasta que el algoritmo termina.

### El algoritmo (versión "proponen los estudiantes")

1. Cada estudiante sin colegio propone al colegio que más prefiere entre los
   que todavía no lo han rechazado.
2. Cada colegio recibe propuestas y las ordena según su propio ranking.
   Retiene tentativamente a los mejores hasta llenar su cupo, y **rechaza al resto**.
3. Un estudiante rechazado propone al siguiente colegio en su lista.
4. Se repite hasta que nadie tiene más propuestas pendientes.

La versión "proponen los colegios" es simétrica: los colegios proponen a
estudiantes, y los estudiantes retienen tentativamente su mejor oferta.

### Propiedades principales

- **Estabilidad**: el resultado de DA nunca tiene un *par bloqueante* — un
  estudiante y un colegio que preferirían estar juntos por sobre su
  asignación actual. Esto es lo que lo distingue de mecanismos como Boston.
- **Optimalidad para el lado que propone**: si proponen los estudiantes, el
  resultado es el mejor matching estable posible *para todos los estudiantes
  simultáneamente* (el "student-optimal stable matching"). Simétricamente
  para colegios si proponen ellos.
- **A-la-inversa, pesimalidad para el lado que recibe propuestas**: el lado
  que no propone obtiene, entre todos los matchings estables, el peor
  resultado posible para sí mismo.
- **Strategy-proofness (solo para el lado que propone)**: si proponen los
  estudiantes, a ningún estudiante le conviene mentir sobre sus preferencias
  — reportar la preferencia verdadera es óptimo. Esto **no** es cierto para
  el lado que recibe (los colegios sí podrían beneficiarse manipulando, en
  general).
- **Existencia**: siempre existe al menos un matching estable, y DA lo
  encuentra en tiempo polinomial.

### ¿Por qué importa quién propone?

El lado que propone termina, en promedio, con una asignación mejor. Esto no
es un detalle técnico menor: es una decisión de diseño con consecuencias
distributivas reales. En el diseño de sistemas de admisión escolar (Boston,
NYC), la elección de que *los estudiantes propongan* fue deliberada,
precisamente para favorecerlos frente a los colegios.

### Para explorar en el simulador

Prueba correr el mismo problema con "proponen estudiantes" y luego con
"proponen colegios" — vas a ver que el matching puede cambiar, pero **ambos
son estables**. Esa es la intuición central: puede haber múltiples matchings
estables, y quién propone determina cuál de ellos se alcanza.

### Formalización

Usando la notación de **Definiciones** ($S$, $C$, $q_c$, $\succ_s$, $\succ_c$):

**El algoritmo** (versión estudiantes-proponentes), como una secuencia de
rondas $t = 1, 2, \dots$: sea $A_t(s) \subseteq C$ el conjunto de colegios
que $s$ todavía no ha probado y que no lo rechazaron. En cada ronda, cada
estudiante $s$ sin colegio tentativo propone a $\arg\max_{\succ_s} A_t(s)$.
Cada colegio $c$ retiene tentativamente, de entre quienes le propusieron
más los que ya tenía, a los $q_c$ mejores según $\succ_c$, y rechaza al
resto. El algoritmo termina cuando ninguna propuesta es rechazada.

**Teorema (Gale y Shapley, 1962).** El algoritmo de Deferred Acceptance
converge en un número finito de pasos a un matching $\mu^{DA}$ que es
**estable**. Además, si proponen los estudiantes, $\mu^{DA}$ es el matching
**estudiante-óptimo**: para todo matching estable $\mu'$,

$$\mu^{DA}(s) \;\; \succeq_s \;\; \mu'(s) \qquad \forall\, s \in S$$

**Teorema (optimalidad/strategy-proofness del lado que propone).** Si
proponen los estudiantes, $\mu^{DA}$ es strategy-proof para $S$: ningún
estudiante puede obtener un resultado mejor (según su propia $\succ_s$)
reportando una preferencia distinta de la verdadera. Formalmente, no existe
$s$, $\succ_s'$, tal que $\mu^{DA}(\succ_s', \succ_{-s})(s) \succ_s \mu^{DA}(\succ_s, \succ_{-s})(s)$.
Esta garantía **no** se extiende al lado que recibe las propuestas (los
colegios sí pueden, en general, beneficiarse reportando una prioridad
distinta de la real).

**Teorema de unicidad (Alcalde y Barberà, 1994).** Con prioridades $\succ_c$
estrictas y fijas, DA (estudiantes proponiendo) es el **único** mecanismo
que es simultáneamente estable y strategy-proof para los estudiantes — no
existe otro mecanismo con esas dos propiedades a la vez. Es el mismo tipo
de resultado que vas a ver para TTC en la página de Mercado de Casas (Ma,
1994), aplicado a un problema distinto: ahí "las tres" propiedades
coexistían porque no había prioridades externas; acá, "las dos"
propiedades (estabilidad + strategy-proofness) determinan un único
mecanismo, precisamente porque exigir la tercera (Pareto eficiencia) es lo
que ya no se puede sumar sin romper alguna de las otras dos.
