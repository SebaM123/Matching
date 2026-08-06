## ¿Qué es Kidney Exchange?

Como viste en **Motivación**, comprar y vender riñones está prohibido —
es el ejemplo clásico de **mercado repugnante**. Pero muchas veces una
persona necesita un trasplante y tiene un familiar o ser querido dispuesto
a donarle un riñón... que resulta **incompatible** (grupo sanguíneo,
tejido). Roth, Sönmez y Ünver (2004) diseñaron un mecanismo para resolver
esto sin que medie dinero: **intercambios en ciclo**.

### La idea

Cada **pareja** paciente-donante que es incompatible entre sí se anota en
un registro. El mecanismo busca **ciclos de intercambio**: secuencias de
parejas donde el donante de la primera dona al paciente de la segunda, el
de la segunda al de la tercera, y así hasta que el de la última dona al
paciente de la primera, cerrando el ciclo. Todas las cirugías del ciclo se
hacen **el mismo día, en simultáneo** — así nadie corre el riesgo de donar
sin que su ser querido reciba el riñón prometido a cambio.

### ¿Por qué los ciclos son cortos en la práctica (2 o 3 parejas)?

En teoría, un ciclo más largo podría matchear a más gente. Pero cada
cirugía del ciclo tiene que coordinarse en el mismo día, en hospitales
distintos, con equipos médicos distintos — y **ninguna puede fallar** sin
dejar a alguien a mitad de camino (donó pero su familiar no recibió, o
viceversa). Por eso, en la práctica, los programas de kidney exchange
limitan los ciclos a **2 o 3 parejas**: es el punto donde la coordinación
logística sigue siendo manejable. (Existen además "cadenas" que arrancan
con un donante altruista — alguien sin un paciente asociado — que no
necesitan ser simultáneas porque no hay reciprocidad que proteger; son una
extensión del mismo problema que no vas a encontrar en este simulador.)

### El objetivo del mecanismo

Aquí el objetivo no es "estabilidad" ni "eficiencia de Pareto" en el sentido
de las páginas anteriores — es más directo: **maximizar la cantidad de
parejas que consiguen un trasplante**, eligiendo un conjunto de ciclos que
no compartan ninguna pareja entre sí (cada pareja participa, como mucho,
en un ciclo).

Encontrar ese conjunto óptimo de ciclos es, en general, un problema
computacionalmente difícil (crece muy rápido con la cantidad de parejas
cuando se permiten ciclos de largo 3) — los programas de kidney exchange
reales usan software de optimización especializado, no un algoritmo simple
como Deferred Acceptance. El simulador de este portal resuelve el problema
exacto por fuerza bruta, así que anda bien para pocas parejas, pero no
escala a los cientos de parejas de un registro real.

### Para explorar en el simulador

El ejemplo por defecto tiene 4 parejas: P1, P2 y P3 forman un ciclo
perfecto de compatibilidad (P1 compatible con el donante de P2, P2 con el
de P3, P3 con el de P1), y P4 no es compatible con nadie.

- Con **largo máximo de ciclo = 3**: se forma el ciclo completo, las tres
  primeras parejas consiguen trasplante, P4 queda sin match.
- Con **largo máximo de ciclo = 2**: no se encuentra ningún ciclo (no hay
  compatibilidad *mutua* entre ningún par) — **nadie** consigue trasplante,
  a pesar de que la compatibilidad circular sí existía. Esa es la razón
  concreta por la que el largo máximo de ciclo permitido importa tanto en
  la práctica.

### Formalización

**El modelo.** Un conjunto de parejas $P = \{p_1, \dots, p_n\}$ y un
**grafo dirigido de compatibilidad** $G = (P, E)$, donde $(p_i, p_j) \in E$
si y solo si el donante de $p_i$ es compatible con el paciente de $p_j$.
Un **ciclo factible** es una secuencia $p_{i_1} \to p_{i_2} \to \cdots \to
p_{i_k} \to p_{i_1}$ con todas las aristas en $E$ y largo $2 \le k \le L$
(el largo máximo permitido).

**El objetivo**, como problema de optimización — elegir un conjunto de
ciclos $\mathcal{K} = \{K_1, \dots, K_r\}$, vértice-disjuntos entre sí,
que maximice la cantidad total de parejas trasplantadas:

$$\max_{\mathcal{K}} \; \sum_{K \in \mathcal{K}} |K| \qquad \text{sujeto a } \;\; K_i \cap K_j = \emptyset \;\; \forall i \ne j, \;\; 2 \le |K| \le L \;\; \forall K \in \mathcal{K}$$

**Complejidad.** Para $L = 2$, este problema equivale a encontrar un
**matching máximo** en un grafo (resoluble en tiempo polinomial, ej. con
el algoritmo de Edmonds). Para $L \ge 3$, el problema es **NP-difícil**
en general — por eso los programas reales de kidney exchange usan
programación entera y heurísticas especializadas, y por eso este
simulador (que resuelve el problema exacto por fuerza bruta) solo escala
a pocas parejas.
