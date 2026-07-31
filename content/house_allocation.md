## ¿Qué es House Allocation?

Es el problema original que le dio origen a Top Trading Cycles: el
**mercado de intercambio de casas** de Shapley y Scarf (1974). Es un caso
particular —y muy especial— del problema de matching con prioridades que
ya conoces.

### El modelo

Hay N agentes, y cada uno **ya es dueño** de un bien indivisible (una
casa). No hay colegios con cupos ni prioridades externas: la única
"prioridad" de cada casa es su propio dueño. Cada agente tiene una
preferencia (un orden completo) sobre **todas** las casas, incluyendo la
suya. No se permite usar dinero — solo trueques.

El mecanismo es el mismo algoritmo de TTC que ya viste: cada agente sin
casa asignada apunta a su casa remanente favorita; cada casa remanente
apunta a su dueño (mientras siga remanente). Se forman ciclos, y todos los
agentes de un ciclo intercambian sus casas simultáneamente.

### El resultado teórico más elegante de toda la teoría de matching

En la página de TTC viste que, en el problema de *school choice* (con
prioridades dadas por cada colegio), hay una tensión irreductible entre
estabilidad y eficiencia de Pareto. En el **mercado de casas**, esa tensión
desaparece por completo, porque Shapley, Scarf y (más tarde) Roth (1982) y
Ma (1994) demostraron algo notable:

- **TTC es individualmente racional**: nadie termina peor que quedándose
  con su propia casa (porque cada agente siempre puede, en el peor caso,
  quedarse con la suya — nadie puede ser forzado a ceder su casa a cambio
  de algo que no prefiere).
- **TTC es Pareto eficiente.**
- **TTC es strategy-proof**: a nadie le conviene mentir sobre sus
  preferencias.
- **TTC coincide con el único resultado en el "núcleo"** (*core*) del
  mercado: la única asignación que ningún grupo de agentes podría mejorar
  organizando sus propios intercambios por fuera del mecanismo.

Y el resultado de unicidad (Ma, 1994) es todavía más fuerte: **TTC es el
único mecanismo** que cumple simultáneamente racionalidad individual,
eficiencia de Pareto y strategy-proofness en este modelo. No hay otro
mecanismo posible con esas tres propiedades a la vez.

### ¿Por qué esto no contradice lo que viste en TTC (school choice)?

Porque la diferencia está en qué reemplaza a la "prioridad". En *school
choice*, la prioridad de cada colegio es un dato externo, arbitrario, que
puede no coincidir entre colegios — ahí es donde aparece la tensión con la
estabilidad. En el mercado de casas, la "prioridad" de cada casa es
simplemente su dueño — no hay ninguna prioridad externa que respetar más
que la propiedad original. Por eso desaparece el conflicto: no hay
terceros cuyos derechos de prioridad puedan ser violados.

### Para explorar en el simulador

El ejemplo por defecto tiene 3 agentes en un **ciclo de intercambio
perfecto**: A1 quiere la casa de A2, A2 quiere la de A3, y A3 quiere la de
A1. Vas a ver que los tres consiguen su casa favorita a través de un único
ciclo de tres — nadie se queda con lo que ya tenía, y todos mejoran.
