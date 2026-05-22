"""
04b_color.py — Procesamiento en color: comparación de estrategias.

Aplica dos técnicas de mejora (gamma γ=0.5 e igualación de histograma)
sobre la imagen 1088.png en color, usando dos estrategias distintas:

    Estrategia A — naive: aplica la transformación canal por canal (R, G, B)
        de forma independiente. Puede producir desplazamiento cromático
        (color shift) porque cada canal tiene una distribución distinta.

    Estrategia B — HSV: convierte a espacio HSV, aplica la transformación
        solo al canal V (luminancia) y reconvierte a RGB. Preserva los
        matices (H) y la saturación (S) originales.

La figura comparativa permite evidenciar el desplazamiento cromático
producido por la estrategia A y justificar el uso de la estrategia B
como práctica estándar en procesamiento de imágenes en color.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    IMAGEN_COLOR,
    OUT_TABLES,
    cargar_imagen_color,
    cargar_imagen,
    plot_imagen,
    plot_histograma,
    calcular_metricas,
    guardar_figura,
    transf_gamma,
    igualacion_histograma,
    aplicar_a_canales_rgb,
    aplicar_a_luminancia_hsv,
)


def calcular_metricas_color(img_rgb):
    """
    Calcula métricas sobre la luminancia (canal V en HSV) de una imagen
    en color. Esto permite comparar técnicas usando la misma métrica
    independientemente de si la imagen fue procesada en RGB o HSV.
    """
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    V = img_hsv[:, :, 2]
    return calcular_metricas(V)


def medir_color_shift(img_orig_rgb, img_transf_rgb):
    """
    Mide el desplazamiento cromático entre dos imágenes en color.

    Calcula la diferencia media en el canal H (matiz) del espacio HSV.
    El matiz está en [0, 179] en OpenCV (8 bits). Una diferencia de
    matiz > 5 es perceptible al ojo humano.

    También calcula la diferencia media en saturación (canal S).

    Devuelve un diccionario con las métricas de desplazamiento cromático.
    """
    def to_hsv(img):
        return cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)

    hsv_orig  = to_hsv(img_orig_rgb)
    hsv_transf = to_hsv(img_transf_rgb)

    # Diferencia en matiz (H): considerar la circularidad del círculo de color
    diff_H = np.abs(hsv_transf[:, :, 0] - hsv_orig[:, :, 0])
    diff_H = np.minimum(diff_H, 180 - diff_H)   # distancia circular

    diff_S = np.abs(hsv_transf[:, :, 1] - hsv_orig[:, :, 1])
    diff_V = np.abs(hsv_transf[:, :, 2] - hsv_orig[:, :, 2])

    return {
        "delta_H_mean": round(float(np.mean(diff_H)), 3),
        "delta_H_max":  round(float(np.max(diff_H)),  3),
        "delta_S_mean": round(float(np.mean(diff_S)), 3),
        "delta_V_mean": round(float(np.mean(diff_V)), 3),
    }


def main():
    print("=" * 70)
    print("Script 04b — Procesamiento en color: RGB naive vs HSV")
    print(f"Imagen: {IMAGEN_COLOR}")
    print("=" * 70)

    img_color = cargar_imagen_color(IMAGEN_COLOR)
    img_gris  = cargar_imagen(IMAGEN_COLOR, escala_grises=True)

    # Transformaciones a aplicar
    gamma_fn   = lambda A: transf_gamma(A, 0.5)
    equal_fn   = igualacion_histograma

    tecnicas = [
        ("Gamma γ=0.5",          gamma_fn),
        ("Igualación histograma", equal_fn),
    ]

    filas = []

    # -----------------------------------------------------------------
    # Figura 1: comparación RGB naive vs HSV por técnica
    # Estructura: 2 técnicas × filas
    # Columnas: original | RGB naive | HSV | diff H (matiz)
    # -----------------------------------------------------------------
    n_tecnicas = len(tecnicas)

    fig1 = plt.figure(figsize=(22, 6 * n_tecnicas + 2))
    fig1.suptitle(
        f"Procesamiento en color — {IMAGEN_COLOR}\n"
        "Estrategia A (RGB canal por canal) vs Estrategia B (canal V en HSV)",
        fontsize=13, fontweight="bold", y=0.999,
    )

    gs1 = gridspec.GridSpec(
        nrows=n_tecnicas, ncols=5,
        figure=fig1,
        width_ratios=[1.4, 1.4, 1.4, 1.4, 1],
        hspace=0.4, wspace=0.2,
    )

    col_titles = [
        "Original (color)",
        "Estrategia A\n(RGB canal por canal)",
        "Estrategia B\n(canal V en HSV)",
        "Diferencia A vs B\n(amplificada)",
        "Histograma\nluminancia (V)",
    ]

    for i, (nombre_tecnica, funcion) in enumerate(tecnicas):
        print(f"\n  Técnica: {nombre_tecnica}")

        # Aplicar con las dos estrategias
        img_rgb_naive = aplicar_a_canales_rgb(img_color, funcion)
        img_hsv_based = aplicar_a_luminancia_hsv(img_color, funcion)

        # Diferencia absoluta entre estrategias (en luminancia)
        V_naive = cv2.cvtColor(img_rgb_naive, cv2.COLOR_RGB2HSV)[:, :, 2]
        V_hsv   = cv2.cvtColor(img_hsv_based, cv2.COLOR_RGB2HSV)[:, :, 2]
        diff_V  = np.abs(V_naive.astype(np.int16) - V_hsv.astype(np.int16))
        diff_V  = diff_V.clip(0, 255).astype(np.uint8)
        max_d   = diff_V.max()
        if max_d > 0:
            diff_V_amp = (diff_V.astype(np.float32) / max_d * 255).astype(np.uint8)
        else:
            diff_V_amp = diff_V

        # Métricas de color shift
        cs_naive = medir_color_shift(img_color, img_rgb_naive)
        cs_hsv   = medir_color_shift(img_color, img_hsv_based)

        # Métricas de luminancia
        m_orig  = calcular_metricas_color(img_color)
        m_naive = calcular_metricas_color(img_rgb_naive)
        m_hsv   = calcular_metricas_color(img_hsv_based)

        print(f"    Color shift (ΔH) — RGB naive: {cs_naive['delta_H_mean']:.3f}  "
              f"HSV: {cs_hsv['delta_H_mean']:.3f}")
        print(f"    Std luminancia — orig: {m_orig['std (RMS)']:.1f}  "
              f"naive: {m_naive['std (RMS)']:.1f}  "
              f"HSV: {m_hsv['std (RMS)']:.1f}")

        # Subplots
        ax0 = fig1.add_subplot(gs1[i, 0])
        ax1 = fig1.add_subplot(gs1[i, 1])
        ax2 = fig1.add_subplot(gs1[i, 2])
        ax3 = fig1.add_subplot(gs1[i, 3])
        ax4 = fig1.add_subplot(gs1[i, 4])

        # Títulos de columna solo en la primera fila
        t0 = col_titles[0] if i == 0 else ""
        t1 = (col_titles[1] if i == 0 else "") + f"\n{nombre_tecnica}"
        t2 = (col_titles[2] if i == 0 else "") + f"\n{nombre_tecnica}"
        t3 = col_titles[3] if i == 0 else "Diferencia A vs B\n(amplificada)"
        t4 = col_titles[4] if i == 0 else "Histograma\nluminancia (V)"

        plot_imagen(ax0, img_color,     titulo=t0, cmap=None)
        plot_imagen(ax1, img_rgb_naive, titulo=t1, cmap=None)
        plot_imagen(ax2, img_hsv_based, titulo=t2, cmap=None)
        plot_imagen(ax3, diff_V_amp,    titulo=t3, cmap="hot")

        # Histograma de luminancia: original, naive, HSV superpuestos
        V_orig = cv2.cvtColor(img_color, cv2.COLOR_RGB2HSV)[:, :, 2]
        ax4.hist(V_orig.ravel(),       bins=128, range=(0,256),
                 color="gray",       alpha=0.5, label="Original", density=True)
        ax4.hist(V_naive.ravel(),      bins=128, range=(0,256),
                 color="steelblue",  alpha=0.5, label="RGB naive", density=True)
        ax4.hist(V_hsv.ravel(),        bins=128, range=(0,256),
                 color="darkorange", alpha=0.5, label="HSV", density=True)
        ax4.set_title(t4, fontsize=9)
        ax4.set_xlabel("Intensidad V", fontsize=8)
        ax4.set_ylabel("Densidad", fontsize=8)
        ax4.legend(fontsize=7)
        ax4.grid(alpha=0.3)
        ax4.set_xlim(0, 256)

        # Anotar color shift bajo imágenes
        ax1.set_xlabel(
            f"ΔH={cs_naive['delta_H_mean']:.2f}  "
            f"ΔS={cs_naive['delta_S_mean']:.1f}",
            fontsize=8,
        )
        ax2.set_xlabel(
            f"ΔH={cs_hsv['delta_H_mean']:.2f}  "
            f"ΔS={cs_hsv['delta_S_mean']:.1f}",
            fontsize=8,
        )
        ax3.set_xlabel(
            f"diff_V max={max_d}  mean={np.mean(diff_V):.1f}",
            fontsize=8,
        )

        filas.append({
            "técnica":            nombre_tecnica,
            "estrategia":         "RGB naive",
            "delta_H_mean":       cs_naive["delta_H_mean"],
            "delta_S_mean":       cs_naive["delta_S_mean"],
            "std_luminancia":     round(m_naive["std (RMS)"], 2),
            "entropia_luminancia":round(m_naive["entropía Shannon (bits)"], 3),
        })
        filas.append({
            "técnica":            nombre_tecnica,
            "estrategia":         "HSV",
            "delta_H_mean":       cs_hsv["delta_H_mean"],
            "delta_S_mean":       cs_hsv["delta_S_mean"],
            "std_luminancia":     round(m_hsv["std (RMS)"], 2),
            "entropia_luminancia":round(m_hsv["entropía Shannon (bits)"], 3),
        })

    guardar_figura(fig1, "fig04b_color_comparison.png", dpi=130)
    plt.close(fig1)

    # -----------------------------------------------------------------
    # Figura 2: zoom en zona iluminada para ver color shift
    # -----------------------------------------------------------------
    gamma_rgb  = aplicar_a_canales_rgb(img_color,  lambda A: transf_gamma(A, 0.5))
    gamma_hsv  = aplicar_a_luminancia_hsv(img_color, lambda A: transf_gamma(A, 0.5))

    # Zona de interés: cuadrante superior derecho (zona con farol y vegetación)
    H, W = img_color.shape[:2]
    r1, r2 = H//4, 3*H//4
    c1, c2 = W//2, W

    crop_orig  = img_color[r1:r2, c1:c2]
    crop_naive = gamma_rgb[r1:r2,  c1:c2]
    crop_hsv   = gamma_hsv[r1:r2,  c1:c2]

    fig2, axes2 = plt.subplots(1, 3, figsize=(18, 6))
    fig2.suptitle(
        f"Zoom zona iluminada — {IMAGEN_COLOR} — Gamma γ=0.5\n"
        "Comparación de desplazamiento cromático entre estrategias",
        fontsize=12, fontweight="bold",
    )

    plot_imagen(axes2[0], crop_orig,  titulo="Original (zona iluminada)",  cmap=None)
    plot_imagen(axes2[1], crop_naive, titulo="Estrategia A — RGB naive\n"
                                             "(posible color shift)",      cmap=None)
    plot_imagen(axes2[2], crop_hsv,   titulo="Estrategia B — HSV\n"
                                             "(matices preservados)",      cmap=None)

    plt.tight_layout()
    guardar_figura(fig2, "fig04c_color_zoom.png", dpi=130)
    plt.close(fig2)

    # -----------------------------------------------------------------
    # Tabla CSV
    # -----------------------------------------------------------------
    df = pd.DataFrame(filas)
    ruta_csv = OUT_TABLES / "tabla04b_color_metricas.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"\n  ✓ Tabla guardada: {ruta_csv.name}")

    # -----------------------------------------------------------------
    # Interpretación
    # -----------------------------------------------------------------
    print("\nResumen de métricas de color:")
    print(df.to_string(index=False))

    print("\n" + "-" * 70)
    print("Interpretación:")
    print("-" * 70)

    for _, fila in df.iterrows():
        print(f"  {fila['técnica']} — {fila['estrategia']}:")
        print(f"    ΔH={fila['delta_H_mean']:.3f}  "
              f"ΔS={fila['delta_S_mean']:.1f}  "
              f"std_V={fila['std_luminancia']:.1f}  "
              f"H_V={fila['entropia_luminancia']:.3f} bits")

    df_rgb = df[df["estrategia"] == "RGB naive"]
    df_hsv = df[df["estrategia"] == "HSV"]

    print(f"\n  Color shift promedio RGB naive: "
          f"ΔH={df_rgb['delta_H_mean'].mean():.3f}")
    print(f"  Color shift promedio HSV:       "
          f"ΔH={df_hsv['delta_H_mean'].mean():.3f}")
    reduccion = df_rgb['delta_H_mean'].mean() / max(
        df_hsv['delta_H_mean'].mean(), 0.001)
    print(f"  Reducción de color shift: {reduccion:.1f}×")
    print()


if __name__ == "__main__":
    main()