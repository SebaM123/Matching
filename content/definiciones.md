## Glosario

Conceptos transversales a todos los mecanismos del portal. Cada página de
mecanismo explica lo específico de ese algoritmo; aquí está lo que se repite
en todos, con su definición en prosa y su versión en notación matemática.

### Notación formal

Esta es la notación que se reutiliza en el resto del portal:

- $S = \{s_1, \dots, s_n\}$: conjunto de estudiantes.
- $C = \{c_1, \dots, c_m\}$: conjunto de colegios.
- $q_c \in \mathbb{Z}_{>0}$: cupo (capacidad) del colegio $c$.
- $\succ_s$: relación de preferencia estricta y completa del estudiante $s$
  sobre $C \cup \{\emptyset\}$ ($\emptyset$ = "quedar sin colegio").
- $\succ_c$: relación de prioridad estricta y completa del colegio $c$
  sobre $S \cup \{\emptyset\}$.
- $\mu$: un **matching**, es decir una función $\mu: S \to C \cup \{\emptyset\}$
  tal que $|\mu^{-1}(c)| \le q_c$ para todo $c \in C$ (nadie excede el cupo).

Con esta notación, cada definición de abajo tiene una versión formal.

### Matching

Una asignación entre dos lados de un mercado (ej. estudiantes y colegios,
médicos y hospitales, donantes y receptores), donde cada agente de un lado
queda vinculado a como máximo un agente (o cupo) del otro lado.

**Formalmente:** una función $\mu: S \to C \cup \{\emptyset\}$ que satisface
$|\mu^{-1}(c)| \le q_c \;\; \forall c \in C$.

### Mecanismo

La regla o algoritmo que, dado un conjunto de preferencias (y prioridades),
produce un matching. Ejemplos: Deferred Acceptance, Boston, Top Trading
Cycles, Serial Dictatorship.

**Formalmente:** una función $\varphi$ que toma un perfil de preferencias
(y, si corresponde, de prioridades) $\big((\succ_s)_{s \in S}, (\succ_c)_{c \in C}\big)$
y devuelve un matching $\mu = \varphi\big((\succ_s), (\succ_c)\big)$.

### Preferencias vs. prioridades

- **Preferencias**: lo que un agente *quiere* (ej. el orden en que un
  estudiante prefiere los colegios).
- **Prioridades**: el orden que *el otro lado* usa para decidir a quién
  aceptar primero cuando hay más candidatos que cupos (ej. el orden de un
  colegio sobre los estudiantes — puede venir de cercanía, mérito, sorteo,
  hermanos ya matriculados, etc.). En mercados de dos lados "simétricos"
  (ej. matrimonio) ambos lados tienen preferencias reales; en muchos
  mercados de asignación (colegios, hospitales) un lado tiene prioridades,
  no preferencias propias.

**Formalmente:** ambas son relaciones de orden estrictas y completas
($\succ_s$ sobre $C$, $\succ_c$ sobre $S$) — la distinción entre
"preferencia" y "prioridad" es de interpretación económica, no matemática:
una preferencia representa bienestar propio; una prioridad, un criterio
que un tercero (la ley, el colegio) impone sobre quién entra primero.

### Cupo / capacidad

Cuántos agentes puede recibir un colegio (u hospital, etc.). Cuando todos
los cupos son 1, se llama matching **uno-a-uno**; si pueden ser mayores a
1, es **muchos-a-uno**.

**Formalmente:** $q_c \in \mathbb{Z}_{>0}$ para cada $c \in C$, con la
restricción de factibilidad $|\mu^{-1}(c)| \le q_c$. Uno-a-uno es el caso
particular $q_c = 1 \; \forall c$.

Una nota técnica: cuando $q_c > 1$, la prioridad $\succ_c$ que usa este
portal es un orden sobre estudiantes *individuales* — para que eso alcance
para comparar *grupos* de estudiantes (y así comparar matchings completos),
se asume que la preferencia del colegio sobre grupos es **responsive**
["responsiva", Roth (1985)]: prefiere un grupo a otro si se obtiene
reemplazando a un estudiante por uno mejor (según $\succ_c$), sin cambiar
al resto. Es el supuesto estándar en la literatura y el que hace que "una
lista de prioridad" alcance para definir el mecanismo.

### Racionalidad individual

Un matching es individualmente racional si a nadie le conviene, por sí
solo, romper su propia asignación — ningún estudiante prefiere quedarse
sin colegio a su asignación actual, y ningún colegio preferiría dejar un
cupo vacío antes que tener a alguno de sus estudiantes actuales.

**Formalmente:** $\mu$ es individualmente racional si no está **bloqueado
por ningún agente individual**:

- No está bloqueado por un estudiante $s$: $\mu(s) \succeq_s \emptyset$
  (a $s$ le resulta aceptable su asignación, o queda sin colegio).
- No está bloqueado por un colegio $c$: para todo $s' \in \mu^{-1}(c)$,
  $s' \succeq_c \emptyset$ (todos los estudiantes que $c$ recibió le son
  aceptables).

### Estabilidad

Un matching es estable si no existe un **par bloqueante**: un estudiante y
un colegio que preferirían estar juntos por sobre su asignación actual (el
estudiante prefiere ese colegio a donde está, y el colegio preferiría a ese
estudiante por sobre alguno de los que ya tiene, o tiene cupo libre y lo
acepta). La estabilidad es la propiedad central que persigue Deferred
Acceptance.

**Formalmente:** $\mu$ es estable si es individualmente racional y no
admite ningún par bloqueante (ver definición formal abajo). De forma
equivalente (Balinski y Sönmez, 1999), $\mu$ es estable si y solo si es
individualmente racional, **no desperdicia cupos**, y **elimina la
envidia justificada** — ver esas dos definiciones más abajo, que separan
el par bloqueante en sus dos causas posibles.

### Par bloqueante

Ver Estabilidad — es el nombre técnico del "problema" que la estabilidad
busca evitar.

**Formalmente:** el par $(s, c) \in S \times C$ **bloquea** $\mu$ si
$c \succ_s \mu(s)$ (s prefiere $c$ a su asignación actual) y, además,
$c$ preferiría tener a $s$:

$$c \succ_s \mu(s) \quad \text{y} \quad \Big(\exists\, s' \in \mu^{-1}(c) \text{ con } s \succ_c s' \quad \text{o} \quad \big(|\mu^{-1}(c)| < q_c \text{ y } s \succ_c \emptyset\big)\Big)$$

Es decir: $s$ prefiere $c$ a su asignación actual, y además $c$ prefiere a
$s$ por sobre algún estudiante que ya tiene, o tiene cupo libre **y** $s$
le resulta aceptable.

### No desperdicio (*non-wasteful*)

Un matching no desperdicia cupos si ningún estudiante que preferiría un
colegio con asiento libre se queda sin ir a él — no tiene sentido dejar un
cupo vacío mientras alguien que lo prefiere y es aceptable para ese
colegio no lo consigue.

**Formalmente:** $\mu$ no desperdicia cupos si no existen $s \in S$,
$c \in C$ tales que $c \succ_s \mu(s)$, $|\mu^{-1}(c)| < q_c$, y
$s \succ_c \emptyset$.

### Envidia justificada

Un estudiante $s$ tiene envidia justificada de otro estudiante $s'$ si $s$
preferiría el colegio de $s'$ y además tiene *mayor prioridad* que $s'$ en
ese colegio — es "justificada" precisamente porque, de existir, sería un
caso legítimo de prioridad ignorada.

**Formalmente:** $\mu$ **elimina la envidia justificada** si no existen
$s, s' \in S$ tales que $\mu(s') \succ_s \mu(s)$ y $s \succ_{\mu(s')} s'$.

### Optimalidad (para un lado del mercado)

Entre todos los matchings estables posibles, el que es mejor para *todos*
los agentes de un lado simultáneamente. Deferred Acceptance con estudiantes
proponiendo produce el matching **estudiante-óptimo**; con colegios
proponiendo, el **colegio-óptimo**. Pueden ser matchings distintos, y ambos
estables.

**Formalmente:** $\mu$ es **estudiante-óptimo** si $\mu$ es estable y, para
todo matching estable $\mu'$ y todo $s \in S$, se cumple $\mu(s) \succeq_s \mu'(s)$.
(Análogo para colegio-óptimo, intercambiando los roles.)

### Eficiencia de Pareto

Un matching es Pareto eficiente si no existe otro matching donde **al menos
un agente mejora y ningún agente empeora**. Es un criterio distinto de la
estabilidad — un matching puede ser eficiente pero inestable, o estable
pero no ser el más eficiente posible.

**Formalmente:** $\mu$ es Pareto eficiente (para $S$) si no existe un
matching factible $\mu'$ tal que:

$$\mu'(s) \succeq_s \mu(s) \;\; \forall s \in S \quad \text{y} \quad \mu'(s) \succ_s \mu(s) \;\; \text{para algún } s \in S$$

### Strategy-proofness (a prueba de manipulación / compatible con incentivos)

Un mecanismo es strategy-proof si a ningún agente le conviene mentir sobre
sus preferencias verdaderas — decir la verdad es siempre, al menos, tan
bueno como cualquier otra estrategia. Es una propiedad deseable porque hace
que el mecanismo sea fácil y seguro de usar, sin necesitar estrategia.

**Formalmente:** el mecanismo $\varphi$ es strategy-proof si para todo
estudiante $s$, toda preferencia verdadera $\succ_s$, toda preferencia
reportada $\succ_s'$, y todo perfil del resto de los agentes $\succ_{-s}$:

$$\varphi(\succ_s, \succ_{-s})(s) \;\; \succeq_s \;\; \varphi(\succ_s', \succ_{-s})(s)$$

Es decir: reportar $\succ_s$ (la verdad) nunca da un resultado peor, según
$\succ_s$, que reportar cualquier otra cosa.

### Manipulabilidad

Lo opuesto a strategy-proofness: cuando un agente puede obtener un mejor
resultado reportando preferencias distintas a las verdaderas. El mecanismo
de Boston es manipulable; Deferred Acceptance (para el lado que propone) no
lo es.

**Formalmente:** $\varphi$ es manipulable si existen $s$, $\succ_s$,
$\succ_s'$, y $\succ_{-s}$ tales que:

$$\varphi(\succ_s', \succ_{-s})(s) \;\; \succ_s \;\; \varphi(\succ_s, \succ_{-s})(s)$$

### Mercado repugnante (*repugnant market*)

Concepto de Alvin Roth: una transacción que podría ser eficiente en el
sentido económico, pero que la sociedad considera moralmente inaceptable
comprar o vender (ej. órganos humanos). Es una de las razones centrales por
las que se necesitan mecanismos de matching en vez de mercados de precios.

### Unraveling ("desenredo")

Cuando, en ausencia de una regla que ordene el proceso, los participantes
de un mercado empiezan a cerrar acuerdos cada vez más temprano para
ganarle a la competencia, degradando la calidad de la información
disponible y empeorando el resultado para todos. Fue el problema que
motivó el diseño del mercado de residencias médicas en EE.UU.

### Espesor, congestión y seguridad (Roth)

Las tres condiciones que Roth propone para que cualquier mercado funcione
bien: suficientes participantes simultáneos (**espesor**), capacidad de
cerrar transacciones en tiempo razonable (**manejo de la congestión**), y
que sea seguro/simple participar diciendo la verdad (**seguridad**).
