## ¿Qué es el Mercado de Casas?

Es el problema original que le dio origen a Top Trading Cycles: el
**mercado de intercambio de casas** (*housing market*) de Shapley y Scarf
(1974). Es un caso particular —y muy especial— del problema de matching
con prioridades que ya conoces.

**Una aclaración de nombres**, porque la literatura usa dos términos
parecidos para dos modelos distintos:

- **Mercado de casas / *housing market*** (Shapley y Scarf, 1974): cada
  agente **ya es dueño** de una casa — es este modelo, el que vas a
  explorar acá.
- **Asignación de casas / *house allocation*** (Hylland y Zeckhauser,
  1979): **nadie es dueño** de nada al empezar; un planificador central
  asigna las casas usando solo las preferencias. Ese problema lo resuelven
  Serial Dictatorship (que ya viste) o una variante de TTC que finge una
  propiedad inicial arbitraria — y hay un resultado elegante que los
  conecta (lo ves más abajo, en Formalización).

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

### Formalización

**El modelo (Shapley y Scarf, 1974).** Un conjunto de agentes $A = \{a_1,
\dots, a_n\}$, un conjunto de casas $H = \{h_1, \dots, h_n\}$, una biyección
de propiedad $\omega: A \to H$ (cada agente es dueño de exactamente una
casa), y para cada agente $a$ una relación de preferencia estricta y
completa $\succ_a$ sobre $H$. Una **asignación** es una biyección
$\mu: A \to H$ (todos entregan y reciben exactamente una casa).

**El algoritmo (TTC para mercados de casas).** Sobre el conjunto remanente
$A' \subseteq A$: cada $a \in A'$ apunta a $f(a) = \arg\max_{\succ_a} H'$
(su casa remanente favorita); cada casa remanente $h \in H'$ apunta a
$g(h) = \omega^{-1}(h)$ si $\omega^{-1}(h) \in A'$ (su dueño, mientras
siga presente). Se resuelven los ciclos y se repite.

**Individual racionalidad, formalmente:** $\mu(a) \succeq_a \omega(a)$
para todo $a \in A$ — nadie recibe algo peor que su propia casa.

**El núcleo (***core***).** Una asignación $\mu$ está en el núcleo si
ningún subconjunto de agentes $A_0 \subseteq A$ puede, redistribuyendo
solo las casas que ellos mismos poseen ($\{\omega(a) : a \in A_0\}$),
lograr que todos en $A_0$ obtengan algo tan bueno como $\mu$ y al menos
uno estrictamente mejor.

**Teorema (Shapley y Scarf, 1974; Roth, 1982).** El matching $\mu^{TTC}$
producido por TTC es la única asignación en el núcleo, es Pareto eficiente,
individualmente racional, y strategy-proof.

**Teorema de unicidad (Ma, 1994).** TTC es el **único** mecanismo que es
simultáneamente Pareto eficiente, individualmente racional, y
strategy-proof en este modelo — no existe otro mecanismo con esas tres
propiedades a la vez.

### La conexión con Serial Dictatorship (el modelo *sin* dueños)

Si en vez de partir de una propiedad real $\omega$ le "inventamos" una
propiedad inicial arbitraria $\mu_0: A \to H$ a un problema de
**asignación de casas** (donde nadie es dueño de nada realmente), y
corremos TTC sobre esa propiedad ficticia, obtenemos un mecanismo válido
para ese problema — llamado *"core from assigned endowments"*,
$TTC_{\mu_0}$.

**Teorema (Abdulkadiroğlu y Sönmez, 1998).** Para el problema de
asignación de casas sin dueños, el conjunto de matchings alcanzables por
**alguna** Serial Dictatorship (variando el orden $\pi$) es exactamente
igual al conjunto alcanzable por **algún** $TTC_{\mu_0}$ (variando la
propiedad ficticia $\mu_0$), y ambos conjuntos son exactamente el conjunto
de **todos los matchings Pareto eficientes**:

$$\{\mu^{SD}_\pi : \pi\} \;=\; \{TTC_{\mu_0} : \mu_0\} \;=\; \{\text{matchings Pareto eficientes}\}$$

Es un resultado bonito porque conecta dos mecanismos que en el portal
parecen distintos — turnos secuenciales (Serial Dictatorship) vs. ciclos
de intercambio (TTC) — mostrando que, para este problema, son en el fondo
dos formas de generar exactamente la misma familia de resultados
eficientes.
