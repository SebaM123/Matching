## La reforma al SAE propuesta en 2026

En junio de 2026, el presidente José Antonio Kast y la ministra de
Educación, María Paz Arzola, presentaron un **proyecto de ley** que
reforma el Sistema de Admisión Escolar (fuente:
[Ministerio de Educación](https://www.mineduc.cl/presidente-de-la-republica-jose-antonio-kast-y-ministra-arzola-presentaron-proyecto-de-ley-que-reforma-el-sistema-de-admision-escolar/),
[Prensa Presidencia](https://prensa.presidencia.cl/comunicado.aspx?id=332472)).

**Importante:** esto es, al momento de escribir este contenido, un
**proyecto de ley en discusión legislativa**, no una ley vigente. Su
contenido puede cambiar durante la tramitación en el Congreso. Para el
estado actualizado, conviene revisar las fuentes oficiales citadas acá.

### Los tres ejes que declara el proyecto

Según la presentación oficial, la propuesta se organiza en tres ejes:
**reconocimiento al mérito y al esfuerzo**, **libertad de los proyectos
educativos**, y **el derecho de las familias a elegir entre ellos**.

Como motivación, el gobierno citó una encuesta de 2025 según la cual el
62% de los apoderados tiene una percepción mala o muy mala del sistema
actual, y el 84% considera legítimo que los establecimientos puedan
seleccionar estudiantes bajo alguna modalidad.

### El modelo propuesto: dos mecanismos complementarios

1. **Elección Mutua (EM)**: de carácter **voluntario**, solo para
   establecimientos con sobredemanda (más postulantes que cupos).
   Permitiría usar criterios "objetivos, transparentes y no
   discriminatorios" para construir la prioridad del colegio, como:
   adhesión al proyecto educativo, participación en instancias
   informativas, rendimiento académico desde 7° básico, entrevistas, y
   aptitudes para programas especializados. La propuesta **reserva
   cupos** para estudiantes prioritarios (SEP) y estudiantes con
   discapacidad o necesidades educativas especiales permanentes.

2. **Asignación Aleatoria (AA)**: se mantiene el mecanismo centralizado
   actual (el que ya conocés — deferred acceptance sobre prioridad
   legal) para los colegios que no adhieran a Elección Mutua, y para
   los cupos que no se completen tras el proceso de Elección Mutua.

### Cómo se lee esto en términos de la teoría del portal

Este proyecto es, en el fondo, una discusión sobre **quién define la
prioridad** — la pregunta central de diseño de mercado que viste en
Definiciones:

- El SAE actual usa una prioridad **fijada externamente por ley** —
  ningún colegio "elige" a sus estudiantes.
- La propuesta reintroduce, para colegios que adhieran voluntariamente,
  una prioridad que el **colegio ayuda a construir** (mérito, entrevista,
  adhesión al proyecto educativo) — acercándose más al modelo de
  "college admissions" de la teoría de matching, donde el colegio tiene
  preferencias propias, y no solo una fórmula legal pareja para todos.
  Es, en cierto sentido, una reversión parcial hacia lógicas más
  cercanas al mecanismo de Boston/selección previo a 2016 — aunque
  dentro de un proceso todavía centralizado y con cupos reservados
  para estudiantes prioritarios, no una selección libre y descentralizada.
- La Asignación Aleatoria que persiste para el resto de los colegios es
  exactamente el caso de **prioridad común aleatoria** que viste en la
  página de Serial Dictatorship y en Simulación Masiva (el toggle "Todos
  los colegios comparten la misma prioridad").

### El debate de fondo (presentado de forma neutral)

Esta reforma toca una tensión real de la teoría de matching que ya
viste: la prioridad no es un dato neutro, es una decisión de diseño con
consecuencias distributivas. Los argumentos que aparecen en el debate
público incluyen:

- **A favor de incorporar mérito/entrevistas**: mayor alineación entre
  familia y proyecto educativo, reconocimiento al esfuerzo académico,
  respuesta a la insatisfacción medida en la encuesta de 2025.
- **Preocupaciones planteadas por críticos**: el rendimiento académico
  suele estar correlacionado con el nivel socioeconómico de origen, por
  lo que un criterio de mérito podría, sin quererlo, favorecer
  sistemáticamente a estudiantes de mayores recursos en los colegios
  más demandados — de ahí la relevancia de los cupos reservados para
  estudiantes prioritarios como salvaguarda.

Este portal no toma posición sobre si la reforma es deseable — el
**Simulador comparativo** de la siguiente pestaña te deja explorar vos
mismo, con parámetros ajustables, qué efecto tiene (direccionalmente)
incorporar un criterio de mérito en la composición de quién accede a
los colegios más demandados.

### Una aclaración sobre el simulador

Los pesos y porcentajes de cupo reservado en el simulador son
**parámetros ilustrativos y ajustables**, pensados para explorar la
dirección del efecto — no una réplica exacta de la fórmula legal
propuesta (que todavía se está tramitando y podría cambiar). Ajustalos
vos mismo para ver cómo cambia el resultado.

### Formalización

**La prioridad bajo Elección Mutua**, para un colegio $c$ que adhiere, se
modela con un puntaje ponderado sobre criterios observables: sea
$m(s) \in [0,1]$ el rendimiento académico simulado, $e_c(s) \in [0,1]$
una señal de entrevista/adhesión (específica de $c$), y $x_c(s) \in [0,1]$
la cercanía territorial a $c$. Con pesos $w_m, w_e, w_x \ge 0$:

$$\text{puntaje}_c(s) = \frac{w_m \cdot m(s) + w_e \cdot e_c(s) + w_x \cdot x_c(s)}{w_m + w_e + w_x} \qquad \succ_c \; \text{ordena } S \text{ por este puntaje, descendente}$$

**El cupo reservado**, formalmente, es la transformación de prioridad
conocida como ***minority reserve*** (Hafalir, Yenmez y Yıldırım, 2013):
sea $R \subseteq S$ el grupo con cupo reservado (prioritarios SEP y
estudiantes con discapacidad) y $r_c = \lceil \rho \cdot q_c \rceil$ el
cupo reservado del colegio $c$ (con $\rho \in [0,1]$ la proporción
reservada). Se toman los primeros $r_c$ estudiantes de $R$ según el orden
por puntaje, y se los antepone al resto (que sigue ordenado por puntaje
sin distinción de grupo):

$$\succ_c^{\text{con reserva}} \;=\; \underbrace{(R \cap \succ_c)\big[:r_c\big]}_{\text{primero, hasta llenar el cupo reservado}} \;\;+\;\; \underbrace{\succ_c \text{ restante}}_{\text{después, sin distinción de grupo}}$$

Esta transformación preserva las propiedades de Deferred Acceptance
(estabilidad, optimalidad, strategy-proofness) **respecto a la prioridad
ya transformada** $\succ_c^{\text{con reserva}}$ — es una forma de
modelar cupos reservados sin tener que modificar el algoritmo de DA en
sí, y es la misma idea que usa el simulador comparativo de la pestaña
anterior.

**La Asignación Aleatoria**, formalmente, es el caso $\succ_c = \succ_{c'}$
para todo $c, c'$ (prioridad común aleatoria) que ya viste en Serial
Dictatorship — con las propiedades correspondientes de ese caso especial.
