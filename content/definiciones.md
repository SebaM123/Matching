## Glosario

Conceptos transversales a todos los mecanismos del portal. Cada página de
mecanismo explica lo específico de ese algoritmo; aquí está lo que se repite
en todos.

### Matching

Una asignación entre dos lados de un mercado (ej. estudiantes y colegios,
médicos y hospitales, donantes y receptores), donde cada agente de un lado
queda vinculado a como máximo un agente (o cupo) del otro lado.

### Mecanismo

La regla o algoritmo que, dado un conjunto de preferencias (y prioridades),
produce un matching. Ejemplos: Deferred Acceptance, Boston, Top Trading
Cycles, Serial Dictatorship.

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

### Cupo / capacidad

Cuántos agentes puede recibir un colegio (u hospital, etc.). Cuando todos
los cupos son 1, se llama matching **uno-a-uno**; si pueden ser mayores a
1, es **muchos-a-uno**.

### Estabilidad

Un matching es estable si no existe un **par bloqueante**: un estudiante y
un colegio que preferirían estar juntos por sobre su asignación actual (el
estudiante prefiere ese colegio a donde está, y el colegio preferiría a ese
estudiante por sobre alguno de los que ya tiene, o tiene cupo libre). La
estabilidad es la propiedad central que persigue Deferred Acceptance.

### Par bloqueante

Ver Estabilidad — es el nombre técnico del "problema" que la estabilidad
busca evitar.

### Optimalidad (para un lado del mercado)

Entre todos los matchings estables posibles, el que es mejor para *todos*
los agentes de un lado simultáneamente. Deferred Acceptance con estudiantes
proponiendo produce el matching **estudiante-óptimo**; con colegios
proponiendo, el **colegio-óptimo**. Pueden ser matchings distintos, y ambos
estables.

### Eficiencia de Pareto

Un matching es Pareto eficiente si no existe otro matching donde **al menos
un agente mejora y ningún agente empeora**. Es un criterio distinto de la
estabilidad — un matching puede ser eficiente pero inestable, o estable
pero no ser el más eficiente posible.

### Strategy-proofness (a prueba de manipulación / compatible con incentivos)

Un mecanismo es strategy-proof si a ningún agente le conviene mentir sobre
sus preferencias verdaderas — decir la verdad es siempre, al menos, tan
bueno como cualquier otra estrategia. Es una propiedad deseable porque hace
que el mecanismo sea fácil y seguro de usar, sin necesitar estrategia.

### Manipulabilidad

Lo opuesto a strategy-proofness: cuando un agente puede obtener un mejor
resultado reportando preferencias distintas a las verdaderas. El mecanismo
de Boston es manipulable; Deferred Acceptance (para el lado que propone) no
lo es.

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
