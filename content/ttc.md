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
- **No garantiza estabilidad**: acá está el costo. TTC puede dejar pares
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
Pareto estricta sobre DA. Pero fijate qué dice el simulador sobre
estabilidad del resultado de TTC: aparece un par bloqueante. Ese es
exactamente el costo del que habla la tabla de arriba.
