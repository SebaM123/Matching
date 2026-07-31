# Matching Lab

Portal de estudio y simulación interactiva de teoría de matching y market
design. Permite definir un problema de asignación (ej. estudiantes y
colegios con preferencias y cupos), correr distintos mecanismos, y explorar
sus propiedades (estabilidad, optimalidad, incentivos).

## Estructura

- `mechanisms/` — implementación de cada mecanismo (algoritmos puros,
  sin UI), con funciones auxiliares para verificar propiedades (ej.
  estabilidad).
- `content/` — explicaciones teóricas en markdown, una por mecanismo/tema.
- `pages/` — una página Streamlit por sección (simulador + teoría).
- `app.py` — página de inicio.

## Correr localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Mecanismos

- [x] Deferred Acceptance (Gale-Shapley)
- [ ] Boston / Immediate Acceptance
- [ ] Top Trading Cycles (TTC)
- [ ] Serial Dictatorship
- [ ] Kidney Exchange
