## ¿Qué es el mecanismo de Boston?

El **mecanismo de Boston** (también llamado *Immediate Acceptance*) fue,
durante décadas, el sistema real usado por Boston Public Schools para
asignar estudiantes a colegios — de ahí el nombre. Se dejó de usar en 2005,
después de que Abdulkadiroğlu y Sönmez (2003) mostraran sus problemas.

### El algoritmo

1. Cada estudiante propone al colegio que más prefiere.
2. Cada colegio acepta a los postulantes de mejor prioridad hasta llenar su
   cupo — **y esa aceptación es inmediata y definitiva**. Rechaza al resto.
3. Los estudiantes rechazados proponen a su siguiente opción.
4. Se repite. Un colegio que ya llenó su cupo **no vuelve a considerar
   candidatos**, aunque en una ronda posterior se presente alguien con
   mayor prioridad que algún estudiante ya aceptado.

### La diferencia clave con Deferred Acceptance

En DA, un colegio nunca cierra la puerta del todo: retiene tentativamente
a los mejores candidatos vistos *hasta ahora*, y puede desplazar a alguien
si aparece un mejor candidato después. En Boston, una vez que un colegio
acepta, **no hay vuelta atrás** — ni siquiera si eso deja a alguien con
mayor prioridad sin ese lugar.

Esa diferencia, aparentemente pequeña, rompe la estabilidad.

### Propiedades

- **No es estable, en general.** Puede haber un estudiante y un colegio que
  se prefieran mutuamente por sobre su asignación final — algo que DA
  nunca permite.
- **No es strategy-proof.** Como los colegios cierran cupos rápido, a un
  estudiante le puede convenir **no** poner su verdadera primera opción en
  primer lugar, si esa opción es muy competida y tiene baja prioridad ahí —
  le conviene "jugar a lo seguro" con una opción donde tiene más chances
  reales. Esto castiga a las familias que no conocen bien la estrategia del
  mecanismo (típicamente, familias con menos información sobre el sistema).
- Sí puede ser, en algunos casos, más eficiente en el sentido de Pareto que
  el resultado de DA — pero ese beneficio depende de que los agentes jueguen
  estratégicamente, no de que digan la verdad.

### Para explorar en el simulador

El ejemplo por defecto usa la **misma prioridad** (E1 > E2 > E3) en los tres
colegios — un caso realista de "prioridad por mérito único". Fijate que:

- E2 pone C1 como primera opción (su verdadera preferencia), pero pierde
  esa carrera contra E1.
- Como Boston ya cerró el cupo de C2 en la ronda 1 (se lo dio a E3), E2
  termina en C3 — su **última** opción.
- Sin embargo, E2 tenía más prioridad que E3 en C2. Si E2 hubiera podido
  "cambiar" con E3, ambos habrían preferido eso. Ese es exactamente el par
  bloqueante que el simulador te va a marcar: el resultado es inestable.

Compará esto con lo que hace DA sobre las mismas preferencias (pestaña
anterior) — ahí ese problema no aparece.
