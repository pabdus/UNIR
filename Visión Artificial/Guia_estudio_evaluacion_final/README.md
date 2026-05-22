# 📚 Visión Artificial — UNIR
## Guías de Estudio para la Evaluación Final

Este repositorio contiene las guías de estudio generadas tema a tema a partir del material oficial de la asignatura **Visión Artificial** de la UNIR.

Cada guía incluye: conceptos clave, tablas comparativas, derivaciones matemáticas completas, ejemplos numéricos, dudas frecuentes resueltas de la sesión, y claves del test de autoevaluación.

---

## ✅ Temas Completados

| # | Tema | Archivo | Estado |
|---|------|---------|--------|
| 1 | Introducción a los sistemas de percepción | `Guia_Estudio_Tema1_Vision_Artificial.pdf` | ✅ Completado |
| 2 | Elementos de un sistema de percepción | `Guia_Estudio_Tema2_Vision_Artificial.pdf` | ✅ Completado |
| 3 | Captura y digitalización de señales | `Guia_Estudio_Tema3_Vision_Artificial.pdf` | ✅ Completado |
| 4 | Fuentes y tipos de ruido | `Guia_Estudio_Tema4_Vision_Artificial.pdf` | ✅ Completado |
| 5 | Detección y cancelación de anomalías | `Guia_Estudio_Tema5_Vision_Artificial.pdf` | ✅ Completado |
| 6 | Procesamiento de imagen. Operaciones elementales | `Guia_Estudio_Tema6_Vision_Artificial.pdf` | ✅ Completado |
| 7 | Procesamiento de imagen. Operaciones espaciales | `Guia_Estudio_Tema7_Vision_Artificial.pdf` | ✅ Completado |

---

## 📝 Resumen por Tema

### Tema 1 — Introducción a los sistemas de percepción
Sistemas auditivo y visual humano como referencia para los sistemas artificiales.
Conceptos clave: sonido, oído (externo/medio/interno), cóclea, membrana basilar, conos y bastones, Ley de Weber (JND), inhibición lateral, muestreo temporal, síntesis de color RGB.

### Tema 2 — Elementos de un sistema de percepción
Los tres módulos esenciales de cualquier sistema de percepción computacional.
Conceptos clave: captura de información (especificidad, precisión, sensibilidad), tipos de sensores, conversión A/D, preprocesamiento (ruido, anomalías, errores), procesamiento (filtros, segmentación, extracción de características), toma de decisión.

### Tema 3 — Captura y digitalización de señales
La teoría matemática detrás de cómo se convierte una señal analógica a digital.
Conceptos clave: señal analógica vs. discreta, conversor A/D (muestreador → cuantificador → codificador), función x(t) = A·cos(2πft), Teorema de Nyquist-Shannon (f_s ≥ 2f), aliasing, sobremuestreo, cuantificación (bits, niveles = 2^n, resolución).

### Tema 4 — Fuentes y tipos de ruido
Caracterización estadística del ruido en señales e imágenes.
Conceptos clave: clasificación del ruido (térmico, impulsivo, 1/f, man-made), Shannon entropy, entropía aproximada (ApEn), procesos estocásticos, estacionaridad, SNR (Signal-to-Noise Ratio).

### Tema 5 — Detección y cancelación de anomalías
Identificación y eliminación de valores atípicos (outliers) en señales e imágenes.
Conceptos clave: anomalías puntuales/contextuales/colectivas, atributos contextuales vs. de comportamiento, métodos supervisados/semisupervisados/no supervisados, desequilibrio de clases, filtro de mediana (ventana deslizante, robustez a outliers, ruido sal y pimienta), técnicas estadísticas (score = 1/f(x), regla de Freedman-Diaconis, estimación paramétrica, método de Parzen/KDE).

### Tema 6 — Procesamiento de imagen. Operaciones elementales
Técnicas de preprocesado para realzar imágenes mediante operaciones punto a punto.
Conceptos clave: operador punto a punto B(x,y) = T(A(x,y)), ajuste de intensidad (negativo, transformación logarítmica, ley de potencia/corrección gamma, funciones a trozos), histograma como estimación de la fdp, igualación de histograma mediante histograma acumulado (CDA), operador resta (revelar diferencias entre imágenes), operador suma/promediado (reducción de ruido: σ²_C = σ²/M).

### Tema 7 — Procesamiento de imagen. Operaciones espaciales
Filtros que operan sobre el píxel y su vecindad mediante una máscara de coeficientes.
Conceptos clave: operador espacial v = T(u, u₁,...; λ, λ₁,...), operador convolutivo (suma ponderada), estrategias de borde (recorte/vecindad parcial/padding), filtros paso bajo (box filter, gaussiano ponderado, regla suma=1), filtros paso alto (regla suma=0), derivada de primer orden (gradiente, direccional, bordes gruesos) vs. segunda derivada (laplaciano, isotrópico, bordes finos pero sensible al ruido), operadores de Roberts (2×2 diagonales), Prewitt (3×3 sin ponderar), Sobel (3×3 con centro ponderado), magnitud y dirección del gradiente, algoritmo de Canny (pipeline de 5 pasos: suavizado gaussiano → gradiente → supresión de no-máximos → doble umbral → histéresis), regla mnemotécnica (deriva en X detecta bordes verticales y viceversa).

---

## 🔗 Conexión entre temas

```
Tema 1 (percepción biológica)
    ↓ inspira y justifica
Tema 2 (arquitectura del sistema artificial)
    ↓ el primer módulo es la captura, que necesita
Tema 3 (digitalización: muestreo y cuantificación)
    ↓ la señal digitalizada contiene
Tema 4 (ruido: tipos, caracterización estadística)
    ↓ el ruido introduce anomalías que hay que eliminar con
Tema 5 (detección y cancelación de anomalías)
    ↓ la señal ya limpia entra al preprocesado de imagen
Tema 6 (operaciones elementales: realce, histograma, aritmética)
    ↓ tras el realce punto a punto, se aplican
Tema 7 (operaciones espaciales: filtros paso bajo/alto, detección de bordes)
    ↓ con los bordes detectados, se entra al procesamiento avanzado
Temas siguientes...
```

---

*Guías generadas con Claude · Visión Artificial · UNIR*
