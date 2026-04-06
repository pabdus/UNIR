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

---

## Estructura del Proyecto

```
/
├── README.md                          ← Este documento
├── tema1_guia_estudio.pdf             ← Guía de estudio - Tema 1
├── tema2_guia_estudio.pdf             ← Guía de estudio - Tema 2
├── tema3_guia_estudio.pdf             ← Guía de estudio - Tema 3
├── tema4_guia_estudio.pdf             ← Guía de estudio - Tema 4
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
- Tres etapas para resolver problemas:
  1. Comprender (identificar + explicar)
  2. Crear estrategia (idear + elegir + diseñar intervención)
  3. Implementar + evaluar
- Técnicas: DAFO, ERIM, Ishikawa, 6 interrogantes, 20 causas, mapas mentales
- Definición de agente inteligente: Racionalidad + Autonomía
- Fases del agente: Sentir → Pensar → Actuar
- Arquitecturas: Deliberativas, Reactivas, Híbridas, Cognitivas
- Modelos: BDI, Subsumption, PRS, COSY, ACT-R, SOAR
- Agentes basados en búsquedas y planificación

**PDF generado:** `tema1_guia_estudio.pdf`

---

### ✅ Tema 2: Representación del Conocimiento y Razonamiento
**Conceptos cubiertos:**
- Representación como sustituto interno de entidades del mundo real
- Técnicas de representación simbólica: Marcos, Lógica, Reglas (SI-ENTONCES), Restricciones, Red bayesiana, Lógica difusa
- 4 requisitos de una buena representación: Formal, Expresiva, Natural, Tratable
- Sistemas multicapa: descomposición del problema en niveles con agentes especializados
- Clases de conocimiento: dominio, explícito, implícito, superficial, profundo, de control, metaconocimiento
- Tipos de razonamiento: deductivo, inductivo, por analogía, lógico, no-lógico, argumentativo, hipotético
- Validez del razonamiento: depende de la forma, no del contenido
- **Razonamiento deductivo**: general → particular; conclusión necesaria; método de Euclides
- **Razonamiento inductivo**: particular → general; conclusión probable; método de Francis Bacon
- **Razonamiento abductivo**: efecto → causa; hipótesis explicativa; Peirce (retroducción)
- Estructura de Peirce para los 3 tipos de razonamiento
- Inductivo completo vs. incompleto

**PDF generado:** `tema2_guia_estudio.pdf`

---

### ✅ Tema 3: Lógica y Pensamiento Humano
**Conceptos cubiertos:**
- Panorama de tipos de lógica: proposicional, predicados, natural, científica, material, formal, deductiva, inductiva, simbólica, modal, computacional
- Lógicas relevantes para IA: matemática, descriptiva ALC, orden superior, multivaluada, difusa
- **Lógica matemática**: proposiciones, tautología, contradicción, contingencia; conectivos lógicos (¬ ∧ ∨ → ↔); tablas de verdad
- **Lógica de descripción ALC**: conceptos, roles e individuos; TBox (axiomas terminológicos) y ABox (axiomas asertivos); tipos de razonamiento por inferencia (satisfacción, subsunción, instanciación, recuperación, comprensión); atributos de propiedades
- **Lógica de orden superior**: extensión de 1.er orden; cuantifica sobre propiedades y relaciones; tipos monádica y completa
- **Lógica difusa**: valores intermedios; padre Lofti Zadeh (1974); reglas SI-ENTONCES; sistemas de control con retroalimentación

**PDF generado:** `tema3_guia_estudio.pdf`

---

### ✅ Tema 4: Búsqueda No Informada
**Conceptos cubiertos:**
- Qué es la búsqueda en IA: mecanismo para resolver problemas mediante secuencias de acciones
- Correspondencia mundo → modelo → grafo (estado, operador, plan)
- Clasificación: búsqueda informada vs. no informada; offline vs. online
- Mecanismos de resolución: tablas de actuación, algoritmos específicos del dominio, métodos independientes del dominio
- Conocimiento a priori del agente: estado inicial, función expandir, función meta, costes
- Algoritmo general de búsqueda (cola abierta, backtracking, estados repetidos)
- Características de evaluación: completitud, optimalidad, complejidad en tiempo y espacio
- Notación O() y factor de ramificación b
- **BFS** (Breadth-First Search): cola FIFO, explora por niveles, completo y óptimo (coste=1), O(b^d)
- **DFS** (Depth-First Search): pila LIFO, explora por ramas, completo solo sin ciclos, O(b×m) en espacio
- **UCS** (Uniform Cost Search): cola de prioridad por g(n), óptimo con costes distintos, requiere costes positivos
- Aplicación práctica: resolución del reto del foro (problema de rutas con UCS)

**PDF generado:** `tema4_guia_estudio.pdf`

---

## Temas Pendientes

| Tema | Título | Estado |
|------|--------|--------|
| 1    | Introducción a la Toma de Decisiones | ✅ Completado |
| 2    | Representación del Conocimiento y Razonamiento | ✅ Completado |
| 3    | Lógica y Pensamiento Humano | ✅ Completado |
| 4    | Búsqueda No Informada | ✅ Completado |
| 5+   | ... | ⏳ Pendiente |

---

## Notas

- Los PDFs se generan como resúmenes enfocados en la evaluación final
- Cada guía contiene tablas de resumen rápido al final para repaso express
- La metodología prioriza la comprensión activa sobre la memorización pasiva
- Universidad: UNIR (Universidad Internacional de La Rioja)
