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
