# 📚 Proyecto de Estudio — Técnicas de Aprendizaje Automático
**Maestría en Inteligencia Artificial — UNIR**

> Repositorio de guías de estudio generadas interactivamente para preparar la evaluación final.
> Cada tema se estudia con metodología socrática y se consolida en una guía PDF descargable.

---

## 🎯 Descripción

Este proyecto centraliza el material de repaso de la materia **Técnicas de Aprendizaje Automático** del primer semestre de la Maestría en IA de la UNIR. Las guías incluyen conceptos clave, tablas comparativas, fórmulas, comandos de Python y preguntas tipo examen con respuesta.

**Herramienta de estudio:** Claude (Anthropic) como profesor particular interactivo.
**Complemento:** Curso CS229 de Stanford Online (Andrew Ng) — un capítulo diario, alineado con los temas de la UNIR.

---

## 📋 Temas del Semestre

| # | Tema | Estado | Guía PDF | Fecha |
|---|------|--------|----------|-------|
| 1 | Origen y Evolución de la Inteligencia Artificial | ✅ Completado | `Guia_Estudio_Tema1.pdf` | Mar 2026 |
| 2 | Análisis Descriptivo y Exploratorio de Datos (EDA) | ✅ Completado | `Guia_Estudio_Tema2.pdf` | Mar 2026 |
| 3 | Datos Ausentes y Normalización | ✅ Completado | `Guia_Estudio_Tema3.pdf` | Mar 2026 |
| 4 | Regresión y Evaluación de Algoritmos de Regresión | ✅ Completado | `Guia_Estudio_Tema4.pdf` | Abr 2026 |
| 5 | Pendiente | ⬜ Pendiente | — | — |

---

## ✅ Tema 1 — Origen y Evolución de la IA

**Conceptos clave dominados:**
- Definiciones de IA: RAE, Bellman (1978), Kurzweil (1990)
- Fundamentos disciplinares: Filosofía, Matemáticas, Economía, Neurociencia, Ingeniería Informática
- Hitos matemáticos: Boole → Frege → Gödel (incompletitud) → Turing (máquina de Turing)
- Línea de tiempo completa 1912–2023, incluyendo los dos inviernos de la IA (1974-1980 y 1987-1993)
- Leyes de la Robótica de Asimov (3 leyes con orden de prioridad)
- Escuelas de IA: Simbólica, Híbrida, Subsimbólica
- Conceptos relacionados: Robótica, Sistemas Expertos, PLN, Algoritmos Genéticos, ML, Deep Learning, Computación Cognitiva
- Aprendizaje supervisado vs no supervisado

**Conexión con CS229 Stanford:** Contexto histórico que justifica el surgimiento del ML moderno.

---

## ✅ Tema 2 — Análisis Descriptivo y Exploratorio (EDA)

**Conceptos clave dominados:**
- Tipos de variables: Cualitativa (nominal, ordinal) y Cuantitativa (discreta, continua)
- One-Hot Encoding para variables nominales en ML
- Histograma: bins, distribución simétrica, sesgo positivo/negativo
- Medidas de dispersión: Rango, RIC (Q3−Q1), Varianza muestral (n−1, corrección de Bessel), Desviación estándar
- Boxplot y regla de Tukey: outlier si < Q1−1.5×RIC o > Q3+1.5×RIC
- Diagramas de dispersión y SPLOM (Scatterplot Matrix)
- Correlación de Pearson: P = Cov(X,Y)/(Sx×Sy), rango [−1,1]
- 3 reglas de oro: correlación ≠ causalidad, P=0 ≠ independencia, Pearson solo mide linealidad
- Matriz de covarianza: cuadrada, simétrica, diagonal = varianzas
- Comandos Python: `df.describe()`, `df.corr()`, `df.cov()`, `sns.boxplot()`, `np.percentile()`

**Conexión con CS229 Stanford:** EDA es el paso previo obligatorio antes de cualquier algoritmo de ML. La correlación y covarianza son la base de PCA y regresión lineal múltiple.

---

## ✅ Tema 3 — Datos Ausentes y Normalización

**Conceptos clave dominados:**
- **Atributos redundantes:** detección con Correlación de Pearson (variables continuas) y Prueba Chi-cuadrado χ² (variables categóricas)
- **Prueba χ²:** H0 (independencia) vs H1 (asociación) · p-value · α=0.05 · tabla de contingencia · grados de libertad
- **Registros duplicados:** `df.duplicated()` · `df.drop_duplicates()`
- **Mecanismos de pérdida:** MCAR (Missing Completely At Random) · MAR (Missing At Random) · NMAR (Not Missing At Random — el más grave)
- **Imputación estadística:** eliminación (`dropna`) · media · mediana (robusta ante outliers) · moda — con `SimpleImputer`
- **Métodos avanzados:** KNN · EM (Esperanza-Maximización) · MI (Imputación Múltiple con MCMC)
- **Normalización Min-Max:** x_norm = (x−xmin)/(xmax−xmin) → rango [0,1] · `MinMaxScaler()` · sensible a outliers
- **Estandarización Z-score:** z = (x−μ)/σ → μ=0, σ=1 · `StandardScaler()` · más robusta ante outliers
- **Algoritmos que NO necesitan escalado:** árboles (CART, Random Forest, Gradient Boosting), Naive Bayes, LDA
- **One-Hot Encoding:** N−1 columnas para evitar la trampa de la variable ficticia (multicolinealidad) · `pd.get_dummies()` · `OneHotEncoder(drop='first')`
- **Flujo de preprocesamiento:** Redundancia → Duplicados → Imputación → Escalado → Codificación nominal

**Comandos Python clave:**
`df.corr()` · `chi2_contingency()` · `isnull().sum()` · `replace(0,'nan')` · `dropna()` · `SimpleImputer()` · `MinMaxScaler()` · `StandardScaler()` · `get_dummies()` · `OneHotEncoder()`

**Conexión con CS229 Stanford:** La normalización es condición necesaria para que el Descenso por Gradiente converja eficientemente. La detección de redundancia mediante correlación es la base conceptual de PCA (tema central del CS229).

---

## ✅ Tema 4 — Regresión y Evaluación de Algoritmos de Regresión

**Conceptos clave dominados:**

**Regresión Lineal:**
- Modelo simple: f(x) = β₀ + β₁X + ε · β₀=intercepto/bias · β₁=pendiente/peso
- Modelo múltiple: ŷ = β₀ + β₁X₁ + ··· + βₚXₚ
- Matriz de diseño X: columna de unos para absorber β₀ dentro del producto matricial Xβ
- Función de pérdida cuadrática: L(β) = Σ(yᵢ − ŷᵢ)² — elevar al cuadrado evita cancelación de residuos

**Estimación de parámetros:**
- **Método de Mínimos Cuadrados (OLS):** β₁ = Cov(X,Y)/Var(X) · β₀ = ȳ − β₁x̄
- **Ecuación Normal (solución cerrada):** β = (XᵀX)⁻¹Xᵀy · complejidad O(p³)
- **Descenso por Gradiente (Gradient Descent):** βⱼ := βⱼ − η·∂L/∂βⱼ · η = tasa de aprendizaje
- Conexión con Tema 3: normalización (StandardScaler) necesaria para convergencia eficiente del GD — evita valles elongados en la superficie de pérdida

**Métricas de Evaluación:**
- **MSE** (Mean Squared Error): (1/n)Σ(yᵢ−ŷᵢ)² · penaliza cuadráticamente · no robusto a outliers
- **RMSE** (Root Mean Squared Error): √MSE · mismas unidades que y · distancia promedio predicción-realidad
- **R²** (Coeficiente de Determinación): proporción de varianza explicada · medida de correlación, NO de precisión · depende de la varianza del conjunto de prueba
- **MAE** (Mean Absolute Error): (1/n)Σ|yᵢ−ŷᵢ| · robusto a outliers · interpretación directa
- **RMSLE** (Root Mean Squared Logarithmic Error): para variables con escala amplia o cola larga · penaliza más subestimación que sobreestimación
- **MAPE** (Mean Absolute Percentage Error): equivalente porcentual de MAE · indefinido si y=0 · sesgado hacia subestimaciones
- **MPE** (Mean Percentage Error): sin valor absoluto · detecta sesgo sistemático del modelo (sobreestima/subestima)

**Equilibrio Sesgo-Varianza (Bias-Variance Tradeoff):**
- Error total = Sesgo² + Varianza + Error irreducible
- **Alto sesgo → underfitting:** modelo demasiado simple, no captura la estructura de los datos
- **Alta varianza → overfitting:** modelo memoriza el ruido del training, no generaliza
- **Error irreducible:** ruido inherente en los datos, ningún modelo puede eliminarlo

**Visualización de errores:**
- **Gráfico observados vs. predichos:** puntos sobre la diagonal = sobreestimación · puntos bajo = subestimación
- **Gráfico de residuos:** dispersión aleatoria = modelo apropiado · patrón en abanico = heterocedasticidad · patrón curvo = no linealidad

**Comandos Python clave:**
`mean_squared_error()` · `root_mean_squared_error()` · `r2_score()` · `mean_absolute_error()` · `root_mean_squared_log_error()` · `LinearRegression()` · `Pipeline()` · `train_test_split()`

**Conexión con CS229 Stanford:**
- Ecuación normal derivada algebraicamente en Lecture 2
- Descenso por gradiente: principio unificador de todo el curso CS229
- Bias-variance tradeoff: reaparece en regularización, redes neuronales y ensembles

---

## 🗂 Estructura del Proyecto

```
/
├── README.md                    ← Este archivo
├── Guia_Estudio_Tema1.pdf       ← Guía completa Tema 1
├── Guia_Estudio_Tema2.pdf       ← Guía completa Tema 2
├── Guia_Estudio_Tema3.pdf       ← Guía completa Tema 3
├── Guia_Estudio_Tema4.pdf       ← Guía completa Tema 4
└── (próximamente Tema 5...)
```

---

## 🔗 Recursos Complementarios

| Recurso | Descripción | Relevancia |
|---------|-------------|------------|
| CS229 Stanford (Andrew Ng, 2018) — 21 lecciones | Machine Learning completo | ⭐ Técnicas de Aprendizaje Automático |
| CS231N Stanford (2025) — 18 lecciones | Deep Learning para Visión | ⭐ Visión Artificial |
| CS224N Stanford (2024) — 23 lecciones | NLP con Deep Learning | PSU - IA Generativa |
| CS236 Stanford (2023) — 18 lecciones | Modelos Generativos Profundos | PSU - IA Generativa |
| CS234 Stanford (2024) — 16 lecciones | Reinforcement Learning | Razonamiento y Planificación |
| CS221 Stanford (2021) — 60 lecciones | IA: Principios y Técnicas | Investigación y Gestión de Proyectos |

---

## 📌 Notas del Proyecto

- **Metodología:** Estudio socrático — preguntas antes de explicaciones, verificación de comprensión, terminología técnica rigurosa.
- **Ritmo:** Un tema de la UNIR a la vez + un capítulo diario del CS229 como refuerzo matemático.
- **README:** Se actualiza al completar cada tema. Insertar en la raíz del proyecto de estudio.

---

*Última actualización: Abril 2026 — Tema 4 completado.*
