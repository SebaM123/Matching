## ¿Qué es Serial Dictatorship?

Es el mecanismo más simple de los que vas a ver en este portal, y por eso
mismo es un buen punto de llegada: ayuda a entender **por qué existen los
otros**.

### El algoritmo

1. Hay un único **orden de prioridad** sobre los estudiantes, dado de
   antemano (ej. un sorteo, un examen, orden de llegada). No hay
   prioridades separadas por colegio — es un solo orden para todos.
2. En ese orden, cada estudiante elige, en su turno, **el colegio que más
   prefiere entre los que todavía tienen cupo disponible**.
3. Se repite hasta que todos los estudiantes eligieron (o se quedaron sin
   colegios con cupo).

Nada de propuestas, rechazos ni ciclos: cada estudiante simplemente elige
lo mejor que queda disponible, en su turno. De ahí el nombre —
"dictadura" porque cada estudiante, en su turno, tiene el poder absoluto
de elegir lo que quiera (no hay negociación ni prioridad del colegio que
pueda rechazarlo).

### Propiedades

- **Eficiencia de Pareto**: siempre. Es fácil de ver por qué: nadie puede
  terminar peor de lo que podría, porque en su turno elige literalmente lo
  mejor disponible.
- **Strategy-proof**: siempre. Como cada estudiante elige lo mejor
  disponible en su momento, no hay ninguna ventaja en mentir sobre las
  preferencias.
- **Estabilidad**: aquí depende de un supuesto. Serial Dictatorship no tiene
  noción de "prioridad del colegio" propia — pero si tratas el **mismo
  orden global** como si fuera la prioridad de todos los colegios por
  igual, el resultado **sí es estable** respecto a esa prioridad. De hecho,
  en ese caso especial, Serial Dictatorship, TTC y Deferred Acceptance
  (estudiantes proponiendo) **producen exactamente el mismo resultado**.

### La pieza que faltaba: por qué importa el trade-off

En la página de TTC viste que, en general, **no se puede tener estabilidad
y eficiencia de Pareto al mismo tiempo**. Serial Dictatorship muestra
*cuándo* ese conflicto desaparece: cuando todos los colegios tienen la
**misma** prioridad sobre los estudiantes (ej. todos usan el mismo puntaje
de examen, o el mismo sorteo), no hay margen para que un colegio "prefiera"
a alguien distinto de lo que ya determina ese orden único — y ahí
Serial Dictatorship, TTC y DA coinciden, siendo simultáneamente estables y
eficientes.

El trade-off aparece exactamente cuando **distintos colegios tienen
distintas prioridades** sobre los mismos estudiantes (como en el ejemplo
de la página de TTC) — ahí es donde puede haber ganancias de intercambio
que romper la estabilidad, y los mecanismos empiezan a diferir.

### ¿Dónde se usa en la práctica?

Serial Dictatorship (o variantes con sorteo, "random serial dictatorship")
se usa en asignaciones donde honestamente **no hay una prioridad legítima
distinta entre las opciones** más que el orden del sorteo — por ejemplo,
sorteos de vivienda universitaria, asignación de cursos por sorteo, o
turnos de elección en una liga deportiva (draft).

### Para explorar en el simulador

El ejemplo por defecto usa el mismo orden (E1, E2, E3) como prioridad y las
mismas preferencias que la página de Deferred Acceptance. Vas a ver que da
exactamente el mismo resultado (E1→C1, E2→C2, E3→C3) — y que el simulador
lo marca como estable. Prueba cambiar el orden de prioridad y ver cómo
cambia el resultado.
