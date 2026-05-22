# Razonamiento y Planificación Automática
## Guía de Estudio para Evaluación Final

---

## Sobre la Materia

**Razonamiento y Planificación Automática** es una asignatura que aborda los fundamentos de la toma de decisiones para sistemas inteligentes. Se estudia desde la problemática humana de decidir hasta el diseño de agentes inteligentes capaces de razonar, planificar y actuar de forma autónoma en un entorno.

### Temas principales de la materia:
- Introducción a la toma de decisiones
- Arquitectura y tipos de agentes inteligentes
- Algoritmos de búsqueda en espacios de estados
- Planificación automática
- Razonamiento bajo incertidumbre

---

## Metodología de Estudio

Cada tema se trabaja en **dos fases**:

### Fase 1: Sesión de estudio interactiva
- Lectura guiada del material (PDF del tema)
- Repaso conversacional de los conceptos clave
- Preguntas y respuestas para interiorizar la teoría
- Conexión entre conceptos para construir una visión integral

### Fase 2: Generación de guía de estudio (PDF)
- Al finalizar cada tema, se genera un **PDF resumen** con los conceptos esenciales
- Cada PDF está diseñado para ser una herramienta de repaso rápido antes de la evaluación final
- Incluye tablas comparativas, definiciones clave y resúmenes estructurados

### Variante aplicada en Temas 5, 6 y 7: clase magistral por bloques
- Cuando el tema es denso, se puede optar por formato "clase magistral": Claude desarrolla cada bloque con intuición + formalización + ejemplo numérico, intercalando verificaciones puntuales de comprensión.
- Esta variante funcionó muy bien para Tema 5 (Búsqueda Informada), Tema 6 (Búsqueda entre Adversarios) y Tema 7 (Problemas de Planificación).

---

## Estructura del Proyecto

```
/
├── README.md                          ← Este documento
├── tema1_guia_estudio.pdf             ← Guía de estudio - Tema 1
├── tema2_guia_estudio.pdf             ← Guía de estudio - Tema 2
├── tema3_guia_estudio.pdf             ← Guía de estudio - Tema 3
├── tema4_guia_estudio.pdf             ← Guía de estudio - Tema 4
├── tema5_guia_estudio.pdf             ← Guía de estudio - Tema 5
├── tema6_guia_estudio.pdf             ← Guía de estudio - Tema 6
├── tema7_guia_estudio.pdf             ← Guía de estudio - Tema 7
└── ...
```

---

## Temas Completados

### ✅ Tema 1: Introducción a la Toma de Decisiones
**Conceptos cubiertos:**
- Elementos de la toma de decisiones (efecto futuro, reversibilidad, impacto, calidad, periodicidad)
- Decisiones de alto nivel vs. bajo nivel
- Decisiones programadas vs. no programadas
- Problemas estructurados vs. no estructurados
- Tres etapas para resolver problemas: Comprender → Crear estrategia → Implementar + evaluar
- Técnicas: DAFO, ERIM, Ishikawa, 6 interrogantes, 20 causas, mapas mentales
- Definición de agente inteligente: Racionalidad + Autonomía
- Fases del agente: Sentir → Pensar → Actuar
- Arquitecturas: Deliberativas, Reactivas, Híbridas, Cognitivas
- Modelos: BDI, Subsumption, PRS, COSY, ACT-R, SOAR

**PDF generado:** `tema1_guia_estudio.pdf`

---

### ✅ Tema 2: Representación del Conocimiento y Razonamiento
**Conceptos cubiertos:**
- Representación como sustituto interno de entidades del mundo real
- Técnicas: Marcos, Lógica, Reglas (SI-ENTONCES), Restricciones, Red bayesiana, Lógica difusa
- 4 requisitos de una buena representación: Formal, Expresiva, Natural, Tratable
- Clases de conocimiento: dominio, explícito, implícito, superficial, profundo, de control, metaconocimiento
- Tipos de razonamiento: deductivo, inductivo, por analogía, lógico, no-lógico, argumentativo, hipotético
- **Razonamiento deductivo**: general → particular; conclusión necesaria; método de Euclides
- **Razonamiento inductivo**: particular → general; conclusión probable; método de Francis Bacon
- **Razonamiento abductivo**: efecto → causa; hipótesis explicativa; Peirce (retroducción)

**PDF generado:** `tema2_guia_estudio.pdf`

---

### ✅ Tema 3: Lógica y Pensamiento Humano
**Conceptos cubiertos:**
- Panorama de tipos de lógica: proposicional, predicados, natural, científica, material, formal, deductiva, inductiva, simbólica, modal, computacional
- **Lógica matemática**: proposiciones, tautología, contradicción, contingencia; conectivos lógicos (¬ ∧ ∨ → ↔)
- **Lógica de descripción ALC**: TBox (axiomas terminológicos) y ABox (axiomas asertivos); tipos de inferencia
- **Lógica de orden superior**: cuantifica sobre propiedades y relaciones; monádica y completa
- **Lógica difusa**: valores intermedios; padre Lofti Zadeh (1974); reglas SI-ENTONCES

**PDF generado:** `tema3_guia_estudio.pdf`

---

### ✅ Tema 4: Búsqueda No Informada
**Conceptos cubiertos:**
- Correspondencia mundo → modelo → grafo (estado, operador, plan)
- Clasificación: informada vs. no informada; offline vs. online
- Características de evaluación: completitud, optimalidad, complejidad en tiempo y espacio
- **BFS** (Breadth-First Search): cola FIFO, completo y óptimo (coste=1), O(b^d)
- **DFS** (Depth-First Search): pila LIFO, completo solo sin ciclos, O(b×m) en espacio
- **UCS** (Uniform Cost Search): cola de prioridad por g(n), óptimo con costes distintos

**PDF generado:** `tema4_guia_estudio.pdf`

---

### ✅ Tema 5: Búsqueda Informada
**Formato de estudio:** Clase magistral por bloques con resolución de dudas en vivo.

**Conceptos cubiertos:**

**Bloque 1 — Heurísticas:** definición, h(n), admisibilidad (h≤h*), consistencia (h(s)≤c(s,s')+h(s')), teorema consistente⊂admisibles, combinación max(h1,...,hm), diseño vía problemas relajados.

**Bloque 2 — A\*:** f(n)=g(n)+h(n), criterio de terminación (extracción, no inserción), ejemplo Arad→Bucarest=418, complejidad entre O(b^d) y lineal, consistencia necesaria en grafo con lista cerrada.

**Bloque 3 — Subobjetivos:** aplicación débil vs fuerte, b^d→(x+1)·b^{d'}, cálculo con logaritmos, completitud y optimalidad condicionales.

**Bloque 4 — Búsqueda online:** hill climbing (voraz, óptimos locales), búsqueda con horizonte k, hill climbing = horizonte k=1, trade-off reactividad vs deliberación.

**PDF generado:** `tema5_guia_estudio.pdf` (28 páginas)

---

### ✅ Tema 6: Búsqueda entre Adversarios
**Formato de estudio:** Clase magistral por bloques con resolución de dudas en vivo.

**Conceptos cubiertos:**

**Bloque 1 — Marco conceptual:** escenarios cooperativo/antagónico, suma cero (von Neumann, 1928), árbol de juego G=⟨N,E,L⟩, jugadores max/min, ply, función de utilidad.

**Bloque 2 — Minimax:** estrategia óptima para max, árbol completo → propagación, funciones MaxValor/MinValor, O(b^d), minimax con suspensión y función heurística e(s)=w₁f₁(s)+...+wₙfₙ(s).

**Bloque 3 — Poda Alfa-Beta:** α ("piso" de max), β ("techo" de min), poda alfa (β≤α) y beta (α≥β), resultado idéntico al minimax, O(b^{d/2}) mejor caso, eficiencia depende del orden de exploración.

**Bloque 4 — Expectiminimax:** nodo azar, valor esperado ∑p(s)·ExpectMinimax(s), escala de valores importa (≠ minimax), función e con intervalo finito, O(b^d · n^d).

**PDF generado:** `tema6_guia_estudio.pdf` (20 páginas)

---

### ✅ Tema 7: Problemas de Planificación
**Formato de estudio:** Clase magistral por bloques (paquete de transferencia desde sesión previa).

**Conceptos cubiertos:**

**Bloque 1 — Definición y diferencia con búsqueda:** los cuatro ingredientes (estado actual, meta, acción, plan); estado estructurado vs. opaco; la planificación SÍ usa búsqueda; complejidad PSPACE-Completo.

**Bloque 2 — Planificación clásica vs. con incertidumbre:** seis asunciones clásicas (observable, estático, determinista, proposicional, duración unitaria, offline); función de transición probabilística P(s'|s,a); HMM para observabilidad parcial; sub-campos por relajación de asunciones (numérica, temporal, online).

**Bloque 3 — Clasificación de métodos:** forward (progresión), backward (regresión), POP (orden parcial), HTN (jerárquica); anomalía de Sussman; cuatro formas de dependencia entre submetas (destrucción, habilitación, costo variable, conflicto de recursos).

**Bloque 4 — Planificadores de orden parcial (POP):** espacio de planes parciales (no de estados); componentes (nodos, arcos de orden A≺B, enlaces causales A→ᵖB, precondiciones abiertas); acciones INICIO y FINAL; criterios de plan solución; amenazas; resolución por promoción (B≺C) y democión (C≺A).

**Bloque 5 — Ejemplo trabajado:** anomalía de Sussman resuelta paso a paso con POP; detección y resolución de amenaza sobre libre(B); dos linalizaciones válidas del plan parcial solución.

**PDF generado:** `tema7_guia_estudio.pdf` (16 páginas)

---

## Dudas y comentarios pedagógicos del Tema 5

### Confusiones comunes
1. FIFO/LIFO (no "LILO"): BFS=FIFO, DFS=LIFO
2. Nodo vs pieza en puzzle-8: nodo = configuración completa del tablero
3. Admisibilidad (global) vs consistencia (local): toda consistente es admisible, no al revés
4. Monotonía creciente ≠ estrictamente creciente: f nunca decrece, puede mantenerse igual
5. Heurística inadmisible: pierde optimalidad pero NO completitud
6. Terminación A*: cuando la meta es **extraída**, no cuando es agregada

### Claves para la evaluación del Tema 5
- A* con h(n)=0 degenera en UCS
- Subobjetivos: completitud y optimalidad son **condicionales**
- Hill climbing y horizonte no garantizan completitud ni optimalidad en general

---

## Dudas y comentarios pedagógicos del Tema 6

### Confusiones comunes
1. Min no poda la rama completa desde el inicio: no sabe el mínimo sin explorar los hijos
2. Si no hay valor ≤ α: devuelve el mínimo normalmente, sin podar
3. Poda α-β ≠ resultado diferente: siempre produce el mismo resultado que minimax
4. Escala en expectiminimax: sumas ponderadas son sensibles a escala absoluta (≠ minimax)
5. Ply = media jugada; turno completo = dos plys

### Claves para la evaluación del Tema 6
- Estrategia óptima = mejor resultado garantizado para **max**
- Poda α-β: mismo resultado que sin poda, eficiencia depende del orden de exploración
- Expectiminimax: azar solo cuando hay evento aleatorio **independiente** de los jugadores
- Función e ideal: transformación lineal positiva de P(ganar)
- Complejidad expectiminimax: O(b^d · n^d)

---

## Dudas y comentarios pedagógicos del Tema 7

### Confusiones comunes
1. "La planificación no usa búsqueda" → FALSO: sí la usa; lo que cambia es el espacio y la representación del estado
2. La meta es una **condición** sobre el estado final, no un punto específico del espacio
3. POP no es búsqueda backward: la dirección no es la diferencia clave — es el **espacio de búsqueda** (planes parciales vs. estados)
4. Una amenaza no significa que el plan está mal: es un riesgo que se resuelve con promoción o democión
5. El plan parcial solución no es ejecutable directamente: hay que linealizarlo eligiendo un orden total compatible
6. Dos submetas independientes no significa que ninguna destruya a la otra: hay cuatro formas de dependencia

### Claves para la evaluación del Tema 7
- Los cuatro ingredientes: **estado actual, meta, acción, plan**
- Complejidad planificación clásica: **PSPACE-Completo**
- Función de transición con incertidumbre: **P(s' | s, a)**
- POP busca en el **espacio de planes parciales** (no de estados)
- Amenaza: C amenaza A→ᵖB si C elimina p, y puede ir entre A y B
- Resolución: **promoción** (B≺C) o **democión** (C≺A)
- Plan parcial solución: sin precondiciones abiertas + sin amenazas + sin ciclos
- HTN: tareas complejas → sub-tareas → … → tareas primitivas (ejecutables directamente)
- Anomalía de Sussman: motivación del POP; planificadores secuenciales fracasan en ella

---

## Temas Pendientes

| Tema | Título | Estado |
|------|--------|--------|
| 1    | Introducción a la Toma de Decisiones | ✅ Completado |
| 2    | Representación del Conocimiento y Razonamiento | ✅ Completado |
| 3    | Lógica y Pensamiento Humano | ✅ Completado |
| 4    | Búsqueda No Informada | ✅ Completado |
| 5    | Búsqueda Informada | ✅ Completado |
| 6    | Búsqueda entre Adversarios | ✅ Completado |
| 7    | Problemas de Planificación | ✅ Completado |
| 8+   | ... | ⏳ Pendiente |

---

## Notas

- Los PDFs se generan como resúmenes enfocados en la evaluación final
- Cada guía contiene tablas de resumen rápido al final para repaso express
- La metodología prioriza la comprensión activa sobre la memorización pasiva
- Universidad: UNIR (Universidad Internacional de La Rioja)
- Formato Temas 5, 6 y 7: clase magistral por bloques con resolución de dudas en vivo (metodología alternativa exitosa)
- Pipeline de PDF: skill `pdf-matematico` con HTML+MathJax → matplotlib+weasyprint (tipografía Computer Modern vectorial)
