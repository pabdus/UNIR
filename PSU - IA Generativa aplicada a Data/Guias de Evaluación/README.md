# PSU — IA Generativa Aplicada al Análisis de Datos (UNIR)

## Descripción

Repositorio de estudio para el PSU de **Inteligencia Artificial Generativa Aplicada al Análisis de Datos** de la Universidad Internacional de La Rioja (UNIR). Contiene guías de estudio con profundidad matemática completa, orientadas a la preparación de la evaluación final.

## Estructura del curso

| Tema | Título | Estado | Guía de estudio |
|------|--------|--------|-----------------|
| 1 | Fundamentos de IA generativa | ✅ Completado | `Guia_Estudio_Tema1_Fundamentos_IA_Generativa.pdf` |
| 2 | Modelos generativos aplicados a datos (GAN, VAE, Transformers) | ✅ Completado | `Guia_Estudio_Tema2_Modelos_Generativos_Datos.pdf` |
| 3 | Preprocesamiento y enriquecimiento de datos con IA | ✅ Completado | `Guia_Estudio_Tema3_Preprocesamiento_Enriquecimiento.pdf` |
| 4 | Por definir | ⏳ Pendiente | — |
| 5 | Ingeniería de características con IA generativa | ✅ Completado | `Guia_Estudio_Tema5_Ingenieria_Caracteristicas.pdf` |

## Progreso semanal

### Semana actual — Tema 5: Ingeniería de características con IA generativa

**Contenido cubierto:**

- **Fundamentos de feature engineering** — Las cuatro operaciones base: construcción de nuevas variables, transformaciones matemáticas (ej. log1p para sesgo positivo), codificación de variables categóricas, reducción/combinación. Criterios de validez de una nueva variable: aporte de información nueva, justificación de dominio, validación empírica
- **Generación de variables con LLM** — Tres tipos: interacción semántica (ej. `friccion_reciente`), condicionales con lógica compleja (ej. `es_cliente_premium`), transformaciones guiadas por contexto matemático. Proceso en tres pasos: descripción → generación → validación humana. Comparativa LLM vs técnicas tradicionales: tiempo, creatividad, trazabilidad, riesgos
- **Embeddings generativos para categóricas** — Limitaciones de One-Hot Encoding (alta dimensionalidad, ausencia de semántica). Definición formal de embedding como \(f: \mathcal{C} \rightarrow \mathbb{R}^d\). Embeddings aprendidos desde datos con autoencoder (bottleneck, semántica emergente, adaptación al dominio). Embeddings preentrenados con LLM (text-embedding-ada-002, text-embedding-3-small). Flujo completo: texto libre → variable categórica interpretable + embedding denso
- **Selección de características e importancia de variables** — Importancia basada en árboles: reducción de impureza acumulada, sesgo hacia alta cardinalidad. Importancia por permutación: agnóstica al modelo, destruye relación variable-target midiendo caída en métrica. SHAP (SHapley Additive exPlanations): valores de Shapley, propiedad de eficiencia \(\sum \phi_j = f(x_i) - \mathbb{E}[f(x)]\), interpretabilidad local por registro vs global por promedio de valores absolutos. Tres roles del LLM: generador de código, experto de dominio ("curador semántico"), intérprete de resultados
- **Evaluación del impacto: uplift** — Protocolo formal en tres pasos: baseline → modelo enriquecido → medición. Fórmula: \(Uplift = \text{Métrica}_{enriquecido} - \text{Métrica}_{baseline}\). Consistencia en múltiples splits. Distinción entre uplift global y valor de negocio en subgrupos clave
- **Feature engineering en pipelines de ML** — Pipeline como DAG (Directed Acyclic Graph). Tres problemas que resuelve: data leakage (fit exclusivo en train), reproducibilidad, training-serving skew (fallo silencioso por desconexión laboratorio-producción). Integración de LLM como FunctionTransformer, embeddings SVD como estimador personalizado con fit/transform, selectores dinámicos. Agentes LLM en pipelines adaptativos
- **Comparación técnicas tradicionales vs IA generativa** — Por tarea: crear interacciones, codificar categóricas, transformar texto libre, evaluar importancia. Rol irremplazable del analista: intencionalidad y validación

**Profundidad matemática alcanzada:**
- Fórmula de uplift: \(Uplift = F1_{enriquecido} - F1_{baseline}\)
- Función de embedding: \(f: \mathcal{C} \rightarrow \mathbb{R}^d\) con \(d \ll |\mathcal{C}|\)
- Valor SHAP: \(\phi_j(i) = \sum_{S \subseteq F \setminus \{j\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [f(S \cup \{j\}) - f(S)]\)
- Propiedad de eficiencia de Shapley: \(\sum_{j=1}^{|F|} \phi_j(i) = f(x_i) - \mathbb{E}[f(x)]\)
- Importancia global SHAP: \(\text{importancia}_j = \frac{1}{n}\sum_{i=1}^n |\phi_j(i)|\)
- Transformación logarítmica para sesgo positivo: \(\log(\text{ingresos} + 1)\)

**Conceptos transversales consolidados:**
- Distinción interpretabilidad local (SHAP por registro) vs global (promedio de valores absolutos)
- Conexión entre uplift global y valor de negocio en subgrupos: SHAP como herramienta para detectar mejoras concentradas
- Analogía autoencoder clásico (punto fijo en latente) vs VAE (distribución \(\mathcal{N}(\mu, \sigma^2)\)) aplicada a embeddings
- Training-serving skew como fallo silencioso — el pipeline como solución estructural
- Rol del analista aumentado: intencionalidad + validación como responsabilidades irremplazables

## Metodología de estudio

- **Enfoque:** Prioridad en comprensión matemática profunda, con español neutro
- **Material base:** Contenido de UNIR (prioridad), complementado con CS224N y CS236 de Stanford
- **Dinámica:** Sesiones de estudio guiado con preguntas dirigidas, analogías, y verificación de comprensión
- **Entregables por tema:** Guía PDF de estudio + actualización de README

## Estrategia recomendada

1. Ver la clase del tema correspondiente en UNIR (primera pasada)
2. Estudiar con la guía de este proyecto (profundización matemática)
3. Resolver las preguntas de autoevaluación de cada guía
4. Repasar conceptos que no hayan quedado claros en sesión guiada

## Recursos complementarios

- **CS224N** — NLP con Deep Learning (Stanford) — Refuerzo, no curso paralelo
- **CS236** — Modelos Generativos Profundos (Stanford) — Refuerzo, no curso paralelo
- **SDV Documentation** — docs.sdv.dev — Referencia práctica para CTGAN/TVAE
- **LangChain Documentation** — python.langchain.com — Referencia práctica para agentes y pipelines
- **DSPy Documentation** — dspy.ai — Referencia para pipelines con optimización automática de prompts

---

*Última actualización: Mayo 2026 — Tema 5 completado*
