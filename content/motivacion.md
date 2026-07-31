## ¿Por qué existe el diseño de mercado?

La economía tradicional resuelve la escasez con **precios**: si hay más
demanda que oferta, el precio sube hasta que el mercado se vacía. Pero hay
muchísimos mercados donde **usar precios no es posible, no es legal, o la
sociedad lo considera moralmente inaceptable**. Ahí es donde entra el
diseño de mercado (*market design*) y, en particular, la teoría de matching.

Pensá en estos casos:

- **Órganos para trasplante.** En casi todos los países está prohibido
  comprar y vender riñones. No podemos dejar que el precio asigne los
  órganos disponibles a quien más pague.
- **Colegios públicos.** No queremos que el mejor colegio se lo quede la
  familia que más puede pagar — hay un compromiso social de asignar por
  otros criterios (cercanía, prioridad, sorteo).
- **Matrimonio.** Obviamente no se resuelve con precios.
- **Cupos de residencia médica, adopciones, refugiados reubicados entre
  países** — todos casos donde no hay (o no debería haber) un precio de
  mercado.

Alvin Roth —premio Nobel de Economía 2012, junto a Lloyd Shapley, por sus
aportes a esta área— llamó a estos **"mercados repugnantes"** (*repugnant
markets*): transacciones que podrían ser eficientes en el sentido económico
tradicional, pero que la sociedad rechaza permitir que se compren y vendan.
La repugnancia no es un detalle marginal — es una restricción real de
diseño, tan real como una restricción presupuestaria.

### Entonces, ¿cómo se asigna, si no es con precios?

Con **mecanismos**: reglas explícitas que toman las preferencias (y a veces
prioridades) de los participantes y producen una asignación. Diseñar bien
esa regla es un problema de ingeniería económica, no solo de teoría — y ahí
es donde nace la teoría de matching.

### Un ejemplo real: el colapso y rediseño del mercado de residencias médicas

En EE.UU., antes de los años 50, los hospitales competían por reclutar
médicos jóvenes ofreciéndoles posiciones **cada vez más temprano** — a
veces años antes de graduarse — para ganarle a la competencia. Esto se
conoce como **"unraveling"** (desenredo, o carrera hacia atrás): sin una
regla que ordene el proceso, el mercado se vuelve caótico, la información
es mala (nadie sabe realmente sus opciones todavía) y termina siendo peor
para todos. La solución fue un mecanismo centralizado de matching (el
antecesor del *National Resident Matching Program*), basado en las mismas
ideas que después formalizarían Gale y Shapley en 1962.

### Otro ejemplo real: el mecanismo de Boston y por qué se cambió

Boston Public Schools usó durante años el mecanismo que lleva su nombre
(lo vas a explorar en este portal) para asignar estudiantes a colegios.
El problema: **castigaba a las familias que no jugaban estratégicamente**.
Las familias informadas aprendían a no poner su colegio favorito primero
si era muy competido, y jugaban "a lo seguro" — las familias sin esa
información perdían sistemáticamente. En 2003, Abdulkadiroğlu y Sönmez
mostraron formalmente el problema, y en 2005 Boston cambió a un mecanismo
basado en Deferred Acceptance.

### Kidney Exchange: el ejemplo más elegante

Como no se puede comprar/vender un riñón, pero muchas veces un familiar
quiere donar y no es compatible con su ser querido, Roth (junto a Sönmez y
Ünver) diseñó un sistema de **intercambios en cadena**: la pareja A dona a
un desconocido compatible con ellos, cuyo familiar dona a la pareja B, y
así sucesivamente — una cadena de donaciones que sin dinero de por medio
logra que muchas más personas reciban un riñón compatible. Es, literalmente,
matching salvando vidas.

### El marco de Roth: tres condiciones para que un mercado funcione

Roth propone que, para que cualquier mercado (con o sin precios) funcione
bien, necesita:

1. **Espesor (thickness):** suficientes participantes de ambos lados al
   mismo tiempo, para que haya opciones reales de intercambio.
2. **Manejo de la congestión (congestion):** el proceso tiene que resolverse
   en un tiempo razonable — de nada sirve tener mucha gente si nadie llega
   a cerrar un acuerdo.
3. **Seguridad (safety):** tiene que ser seguro y simple participar
   honestamente — si conviene mentir o jugar estratégicamente, el mercado
   se vuelve frágil y beneficia a los mejor informados.

Toda la teoría que vas a explorar en este portal —estabilidad,
strategy-proofness, eficiencia— son formas precisas de medir si un
mecanismo cumple con estas condiciones.
