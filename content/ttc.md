## ¿Qué es Top Trading Cycles (TTC)?

**Top Trading Cycles** (Abdulkadiroğlu y Sönmez, 2003, adaptando la idea
original de Shapley y Scarf para intercambio de casas) es un mecanismo que
persigue un objetivo distinto al de Deferred Acceptance: en vez de priorizar
la **estabilidad**, prioriza la **eficiencia de Pareto**.

### El algoritmo

1. Cada colegio con cupo disponible "apunta" a su estudiante de mayor
   prioridad entre los que todavía no tienen asignación.
2. Cada estudiante sin asignación "apunta" a su colegio favorito entre los
   que todavía tienen cupo.
3. Como cada estudiante y cada colegio apunta a exactamente un destino, y
   son un número finito de agentes, siguiendo las flechas **siempre se
   forma al menos un ciclo** (una secuencia que vuelve sobre sí misma:
   estudiante → colegio → estudiante → colegio → ... → el primer
   estudiante).
4. Todos los estudiantes que forman parte de un ciclo quedan asignados al
   colegio al que apuntan **de forma definitiva**. Se les resta un cupo a
   esos colegios; si un colegio llega a cupo cero, sale del proceso.
5. Se repite con los estudiantes y colegios que quedan, hasta que no quede
   nadie por asignar.

Intuitivamente, TTC es un **sistema de intercambios**: un estudiante con
alta prioridad en el colegio que otro estudiante quiere "le cede el lugar"
a cambio de que ese otro colegio (donde el primero tiene prioridad) reciba
a alguien más. De ahí el nombre: ciclos de intercambio de las mejores
opciones disponibles.

### Propiedades

- **Eficiencia de Pareto**: TTC siempre produce un matching Pareto
  eficiente — no existe otra asignación donde alguien mejore sin que
  otro empeore. Esto **no** está garantizado en Deferred Acceptance.
- **Strategy-proofness**: a ningún estudiante le conviene mentir sobre sus
  preferencias. En esto es igual a DA (con estudiantes proponiendo).
- **No garantiza estabilidad**: aquí está el costo. TTC puede dejar pares
  bloqueantes — un estudiante y un colegio que se preferirían mutuamente
  por sobre su asignación final. Es el precio que paga por priorizar
  eficiencia sobre estabilidad.

### El trade-off central: TTC vs. Deferred Acceptance

Esta es, probablemente, la tensión más importante de toda la teoría de
matching con prioridades:

|                          | Deferred Acceptance | Top Trading Cycles |
|--------------------------|----------------------|----------------------|
| Estabilidad              | ✅ Siempre           | ❌ No garantizada    |
| Eficiencia de Pareto      | ❌ No garantizada    | ✅ Siempre           |
| Strategy-proof            | ✅ (lado que propone) | ✅ Siempre           |

**No existe un mecanismo que garantice ambas cosas a la vez** (estabilidad
y eficiencia de Pareto) en general. Elegir uno u otro es una decisión de
diseño con consecuencias reales: ¿preferís un sistema donde nadie tiene un
reclamo legítimo de prioridad ignorada (estable), o uno donde se exprimen
todas las ganancias posibles de intercambio (eficiente)?

### Para explorar en el simulador

El ejemplo por defecto está armado a propósito para mostrar el trade-off:

- Con **Deferred Acceptance**, E1 termina en C2 y E3 en C1.
- Con **TTC**, sobre las mismas preferencias y prioridades, E1 y E3
  literalmente **intercambian lugares**: E1 pasa a C1 y E3 a C2 — el ciclo
  que vas a ver en la traza. Ambos terminan en su colegio favorito.
- E2 termina igual en los dos mecanismos (C3).

Es decir: **nadie empeora, y dos estudiantes mejoran** — una mejora de
Pareto estricta sobre DA. Pero observa qué dice el simulador sobre
estabilidad del resultado de TTC: aparece un par bloqueante. Ese es
exactamente el costo del que habla la tabla de arriba.

### Formalización

En cada ronda, sobre el conjunto remanente de estudiantes $S'$ y colegios
$C'$ (con cupo remanente $q_c' > 0$), se definen dos funciones puntero:

$$f(s) = \arg\max_{\succ_s} \{c \in C' : \text{colegio remanente}\} \qquad g(c) = \arg\max_{\succ_c} \{s \in S' : \text{estudiante remanente}\}$$

Como $S' \cup C'$ es finito y cada nodo tiene exactamente una flecha
saliente ($f$ o $g$ según corresponda), siguiendo las flechas siempre se
encuentra un **ciclo**: una secuencia $s_1 \to c_1 \to s_2 \to c_2 \to
\cdots \to s_k \to c_k \to s_1$ con $f(s_i) = c_i$ y $g(c_i) = s_{i+1 \bmod k}$.
Todo estudiante en un ciclo recibe el colegio al que apunta, de forma
definitiva.

**Teorema (Pareto eficiencia, Abdulkadiroğlu y Sönmez, 2003).** El
matching $\mu^{TTC}$ que produce TTC es Pareto eficiente: no existe un
matching factible $\mu'$ con $\mu'(s) \succeq_s \mu^{TTC}(s) \; \forall s$
y $\mu'(s) \succ_s \mu^{TTC}(s)$ para algún $s$.

**Teorema (strategy-proofness).** TTC es strategy-proof: no existen $s$,
$\succ_s'$, $\succ_{-s}$ tales que $\mu^{TTC}(\succ_s', \succ_{-s})(s) \succ_s \mu^{TTC}(\succ_s, \succ_{-s})(s)$.

**Proposición (no estabilidad).** $\mu^{TTC}$ no es, en general, estable:
existen perfiles donde $\mu^{TTC}$ admite un par bloqueante $(s, c)$ con
$c \succ_s \mu^{TTC}(s)$ y $s \succ_c s'$ para algún $s' \in (\mu^{TTC})^{-1}(c)$.

**El trade-off, formalmente.** No existe ningún mecanismo $\varphi$ que
sea simultáneamente estable y Pareto eficiente para todo perfil de
preferencias y prioridades arbitrario — DA logra lo primero, TTC lo
segundo, y ambos son strategy-proof (para el lado que propone), pero
ningún mecanismo logra las tres cosas en general.
