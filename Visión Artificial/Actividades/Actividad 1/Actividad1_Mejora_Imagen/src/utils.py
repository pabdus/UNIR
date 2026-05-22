"""
utils.py — Funciones reutilizables para el laboratorio de mejora de imagen.

Centraliza:
  - Lectura/escritura de imágenes (con soporte para rutas con tildes en Windows)
  - Conversión a escala de grises
  - Transformaciones de intensidad (negativo, log, gamma, a trozos)
  - Igualación de histograma (implementación manual desde la fórmula)
  - Métricas de contraste y calidad
  - Helpers de visualización (histogramas)
  - Procesamiento en color (estrategia RGB canal por canal y estrategia HSV)

Las implementaciones priorizan claridad y fidelidad a las fórmulas del Tema 6
sobre eficiencia. Todas las transformaciones operan sobre arreglos numpy en
escala de grises, con valores en el rango [0, 255] y tipo uint8 a la salida.
"""

from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as plt


# =============================================================================
# RUTAS DEL PROYECTO
# =============================================================================

# Raíz del proyecto: dos niveles arriba de este archivo (src/utils.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW     = PROJECT_ROOT / "data" / "raw"
OUT_FIGS     = PROJECT_ROOT / "outputs" / "figures"
OUT_TABLES   = PROJECT_ROOT / "outputs" / "tables"

# Asegurar que los directorios de salida existan
OUT_FIGS.mkdir(parents=True, exist_ok=True)
OUT_TABLES.mkdir(parents=True, exist_ok=True)

# Las 4 imágenes seleccionadas del dataset Dark Face
IMAGENES           = ["1013.png", "1033.png", "1045.png", "1088.png"]
IMAGEN_PROTAGONISTA = "1033.png"
IMAGEN_COLOR        = "1088.png"   # única imagen trabajada en color


# =============================================================================
# E/S DE IMÁGENES  —  usa imdecode para soportar rutas con tildes en Windows
# =============================================================================

def _leer_imagen_bytes(ruta):
    """
    Lee una imagen desde disco usando numpy + imdecode.
    cv2.imread falla en Windows cuando la ruta contiene caracteres
    no-ASCII (tildes, ñ, etc.). np.fromfile + cv2.imdecode no tienen
    ese problema porque leen los bytes directamente sin pasar la ruta
    al sistema de archivos de OpenCV.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró la imagen en: {ruta}")
    buffer = np.fromfile(str(ruta), dtype=np.uint8)
    img = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if img is None:
        raise IOError(f"No se pudo decodificar la imagen: {ruta}")
    return img


def cargar_imagen(nombre, escala_grises=True):
    """
    Carga una imagen del directorio data/raw/.

    Parámetros
    ----------
    nombre : str
        Nombre del archivo (ej. "1033.png").
    escala_grises : bool
        Si True, devuelve un arreglo 2D en escala de grises (H, W) uint8.
        Si False, devuelve un arreglo 3D RGB (H, W, 3) uint8.

    Devuelve
    --------
    np.ndarray uint8
    """
    ruta = DATA_RAW / nombre
    img_bgr = _leer_imagen_bytes(ruta)
    if escala_grises:
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def cargar_imagen_color(nombre):
    """
    Carga una imagen del directorio data/raw/ en color RGB.
    Devuelve un arreglo (H, W, 3) uint8 en orden RGB.
    """
    ruta = DATA_RAW / nombre
    img_bgr = _leer_imagen_bytes(ruta)
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def guardar_figura(fig, nombre, dpi=150):
    """Guarda una figura matplotlib en outputs/figures/."""
    ruta = OUT_FIGS / nombre
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    print(f"  ✓ Figura guardada: {ruta.name}")
    return ruta


# =============================================================================
# TRANSFORMACIONES DE INTENSIDAD (FAMILIA 1)
# =============================================================================

def transf_negativo(A):
    """
    Negativo: B = (L-1) - A.
    Para imagen de 8 bits, L-1 = 255.
    Convierte a int16 durante el cálculo para evitar overflow de uint8.
    """
    return (255 - A.astype(np.int16)).clip(0, 255).astype(np.uint8)


def transf_logaritmica(A):
    """
    Transformación logarítmica: B = c * log(1 + A).
    La constante c = 255 / log(256) normaliza la salida al rango [0, 255].
    El término (1 + A) evita log(0) = -infinito cuando A = 0.
    """
    A_float = A.astype(np.float64)
    c = 255.0 / np.log(1.0 + 255.0)
    B = c * np.log(1.0 + A_float)
    return np.clip(B, 0, 255).astype(np.uint8)


def transf_gamma(A, gamma):
    """
    Ley de potencia / corrección gamma: B = 255 * (A/255)^gamma.
    Se normaliza al rango [0,1] antes de elevar para mantener
    el resultado acotado independientemente del valor de gamma.

    Comportamiento:
        gamma < 1  -> aclara (expande tonos bajos)
        gamma = 1  -> identidad
        gamma > 1  -> oscurece (comprime tonos bajos)
    """
    A_norm = A.astype(np.float64) / 255.0
    B = 255.0 * np.power(A_norm, gamma)
    return np.clip(B, 0, 255).astype(np.uint8)


def transf_a_trozos(A, r1=5, s1=8, r2=110, s2=200):
    """
    Función lineal a trozos para estiramiento de contraste.
    Define dos puntos de quiebre (r1, s1) y (r2, s2):

        Tramo 1: [0,  r1] -> [0,  s1]   pendiente = s1/r1
        Tramo 2: [r1, r2] -> [s1, s2]   pendiente = (s2-s1)/(r2-r1)
        Tramo 3: [r2,255] -> [s2,255]   pendiente = (255-s2)/(255-r2)

    Parámetros por defecto ajustados para imágenes oscuras (Dark Face):
        Tramo 2 tiene pendiente ~2.56, estirando agresivamente el rango
        [30, 120] donde se concentran los píxeles con detalle útil.
    """
    A_float = A.astype(np.float64)
    B = np.zeros_like(A_float)

    mask1 = A_float <= r1
    B[mask1] = (s1 / r1) * A_float[mask1]

    mask2 = (A_float > r1) & (A_float <= r2)
    B[mask2] = s1 + ((s2 - s1) / (r2 - r1)) * (A_float[mask2] - r1)

    mask3 = A_float > r2
    B[mask3] = s2 + ((255 - s2) / (255 - r2)) * (A_float[mask3] - r2)

    return np.clip(B, 0, 255).astype(np.uint8)


# =============================================================================
# IGUALACIÓN DE HISTOGRAMA (FAMILIA 2)
# =============================================================================

def igualacion_histograma(A):
    """
    Igualación de histograma según la fórmula del Tema 6:
        B(x,y) = round[ (L-1) * CDA( A(x,y) ) ]
    donde:
        h(k)   = número de píxeles con intensidad k
        p(k)   = h(k) / (M*N)           histograma normalizado (fdp)
        CDA(k) = sum_{j=0}^{k} p(j)     función de distribución acumulada
        L      = 256  (8 bits)

    Implementación manual (no usa cv2.equalizeHist) para mantener
    trazabilidad entre la fórmula y el código.
    """
    L  = 256
    MN = A.size

    h   = np.bincount(A.ravel(), minlength=L)   # histograma
    p   = h / MN                                  # fdp
    CDA = np.cumsum(p)                            # acumulada
    T   = np.round((L - 1) * CDA).astype(np.uint8)  # tabla de transformación
    return T[A]                                   # aplicar píxel a píxel


# =============================================================================
# MÉTRICAS DE CONTRASTE Y CALIDAD
# =============================================================================

def metrica_media(A):
    """Media aritmética de intensidades. Indica brillo promedio."""
    return float(np.mean(A))


def metrica_std(A):
    """
    Desviación estándar de intensidades.
    Equivale al contraste RMS (Root Mean Square contrast).
    Mayor std = mayor contraste.
    """
    return float(np.std(A))


def metrica_rango_dinamico_efectivo(A):
    """
    Rango dinámico efectivo: P99 - P1.
    Usa percentiles en lugar de max-min para ser robusto frente a
    píxeles atípicos (ruido impulsivo, píxeles muertos del sensor).
    """
    p1, p99 = np.percentile(A, [1, 99])
    return float(p99 - p1)


def metrica_contraste_michelson(A):
    """
    Contraste de Michelson: (Imax - Imin) / (Imax + Imin).
    Se usan percentiles P1 y P99 para robustez.
    Devuelve un valor en [0, 1]. Mayor = más contraste.
    """
    p1, p99 = np.percentile(A.astype(np.float64), [1, 99])
    if (p99 + p1) == 0:
        return 0.0
    return float((p99 - p1) / (p99 + p1))


def metrica_entropia_shannon(A):
    """
    Entropía de Shannon del histograma normalizado:
        H = -sum_k p(k) * log2(p(k))
    Acotada en [0, 8] bits para imágenes de 8 bits.
    Mayor entropía = histograma más distribuido = más información.
    Los términos p(k) = 0 se excluyen (0·log(0) = 0 por convención).
    """
    h = np.bincount(A.ravel(), minlength=256)
    p = h / A.size
    p_nz = p[p > 0]
    return float(-np.sum(p_nz * np.log2(p_nz)))


def calcular_metricas(A):
    """Devuelve un diccionario con las 5 métricas para una imagen."""
    return {
        "media":                            metrica_media(A),
        "std (RMS)":                        metrica_std(A),
        "rango dinámico efectivo (P99-P1)": metrica_rango_dinamico_efectivo(A),
        "contraste de Michelson":           metrica_contraste_michelson(A),
        "entropía Shannon (bits)":          metrica_entropia_shannon(A),
    }


# =============================================================================
# PROCESAMIENTO EN COLOR
# =============================================================================

def aplicar_a_canales_rgb(img_rgb, transformacion):
    """
    Estrategia A — naive: aplica una transformación de intensidad de forma
    independiente a cada canal R, G y B.

    Limitación conocida: puede producir desplazamiento cromático (color shift)
    porque cada canal tiene una distribución distinta y se mueve de manera
    independiente, alterando los matices originales de la escena.

    Parámetros
    ----------
    img_rgb : np.ndarray (H, W, 3) uint8  —  imagen en RGB
    transformacion : callable  —  función (2D uint8) -> (2D uint8)

    Devuelve
    --------
    np.ndarray (H, W, 3) uint8
    """
    canales = [transformacion(img_rgb[:, :, c]) for c in range(3)]
    return np.stack(canales, axis=2)


def aplicar_a_luminancia_hsv(img_rgb, transformacion):
    """
    Estrategia B — preferida: convierte a HSV, aplica la transformación
    únicamente al canal V (Value / luminancia), y reconvierte a RGB.

    Preserva el matiz (H) y la saturación (S), modificando solo el brillo.
    Evita el desplazamiento cromático de la estrategia A.

    Parámetros
    ----------
    img_rgb : np.ndarray (H, W, 3) uint8  —  imagen en RGB
    transformacion : callable  —  función (2D uint8) -> (2D uint8)

    Devuelve
    --------
    np.ndarray (H, W, 3) uint8
    """
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    H, S, V = cv2.split(img_hsv)
    V_transf = transformacion(V)
    img_hsv_transf = cv2.merge([H, S, V_transf])
    return cv2.cvtColor(img_hsv_transf, cv2.COLOR_HSV2RGB)


# =============================================================================
# HELPERS DE VISUALIZACIÓN
# =============================================================================

def plot_histograma(ax, A, titulo="Histograma", color="steelblue"):
    """
    Dibuja el histograma de una imagen en escala de grises sobre un eje
    matplotlib. Marca media y mediana con líneas verticales de referencia.
    """
    ax.hist(A.ravel(), bins=256, range=(0, 256),
            color=color, edgecolor="none")
    media   = np.mean(A)
    mediana = np.median(A)
    ax.axvline(media,   color="red",    linestyle="--", linewidth=1,
               label=f"media={media:.0f}")
    ax.axvline(mediana, color="orange", linestyle="--", linewidth=1,
               label=f"mediana={mediana:.0f}")
    ax.set_xlim(0, 256)
    ax.set_xlabel("Intensidad")
    ax.set_ylabel("Frecuencia")
    ax.set_title(titulo, fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)


def plot_imagen(ax, A, titulo="", cmap="gray"):
    """
    Dibuja una imagen sobre un eje matplotlib.
    Para imágenes en color pasar cmap=None.
    vmin/vmax fijos en [0,255] para comparaciones consistentes entre paneles.
    """
    if cmap is None:
        ax.imshow(A)
    else:
        ax.imshow(A, cmap=cmap, vmin=0, vmax=255)
    ax.set_title(titulo, fontsize=10)
    ax.axis("off")


# =============================================================================
# TEST DE INTEGRIDAD
# =============================================================================

if __name__ == "__main__":
    print(f"PROJECT_ROOT : {PROJECT_ROOT}")
    print(f"DATA_RAW     : {DATA_RAW}")
    print(f"OUT_FIGS     : {OUT_FIGS}")
    print(f"OUT_TABLES   : {OUT_TABLES}\n")

    print("Verificando imágenes en data/raw/...")
    for nombre in IMAGENES:
        ruta   = DATA_RAW / nombre
        existe = "✓" if ruta.exists() else "✗"
        print(f"  {existe}  {nombre}")

    print("\nProbando lectura con imdecode...")
    try:
        img = cargar_imagen(IMAGENES[0], escala_grises=True)
        print(f"  ✓ {IMAGENES[0]} leída correctamente — shape: {img.shape}, "
              f"dtype: {img.dtype}, min: {img.min()}, max: {img.max()}")
    except Exception as e:
        print(f"  ✗ Error al leer imagen: {e}")

    print("\nProbando transformaciones sobre imagen sintética 4×4...")
    test = np.array([[0,  50, 100, 150],
                     [10, 60, 110, 200],
                     [20, 70, 120, 220],
                     [30, 80, 130, 250]], dtype=np.uint8)

    print(f"  Original      min={test.min():3d}  max={test.max():3d}")
    print(f"  Negativo      min={transf_negativo(test).min():3d}  "
          f"max={transf_negativo(test).max():3d}")
    print(f"  Logarítmica   min={transf_logaritmica(test).min():3d}  "
          f"max={transf_logaritmica(test).max():3d}")
    print(f"  Gamma 0.5     min={transf_gamma(test, 0.5).min():3d}  "
          f"max={transf_gamma(test, 0.5).max():3d}")
    print(f"  A trozos      min={transf_a_trozos(test).min():3d}  "
          f"max={transf_a_trozos(test).max():3d}")
    print(f"  Igualación    min={igualacion_histograma(test).min():3d}  "
          f"max={igualacion_histograma(test).max():3d}")

    print("\nMétricas sobre imagen sintética:")
    for k, v in calcular_metricas(test).items():
        print(f"  {k}: {v:.3f}")

    print("\n✓ utils.py listo.")