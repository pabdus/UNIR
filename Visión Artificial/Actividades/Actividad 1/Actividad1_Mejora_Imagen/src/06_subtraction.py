"""
06_subtraction.py — Operador resta entre imágenes (Familia 3, parte A).

La resta de imágenes B = |A_mejorada - A_original| revela espacialmente
dónde actuó cada técnica de mejora: las zonas brillantes en la imagen
de diferencia indican mayor cambio introducido por la transformación.

Para la imagen protagonista (1033.png) se calculan las diferencias
absolutas entre la imagen original y cada una de las 4 técnicas de
mejora, produciendo mapas de cambio que permiten:
    - Identificar qué zonas de la imagen fueron más afectadas
    - Comparar la distribución espacial del efecto de cada técnica
    - Detectar artefactos localizados (zonas de saturación, halos)

Adicionalmente se calcula la diferencia entre la mejor técnica (gamma
0.5) y la igualación para mostrar en qué zonas difieren entre sí.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    IMAGEN_PROTAGONISTA,
    OUT_TABLES,
    cargar_imagen,
    plot_imagen,
    plot_histograma,
    calcular_metricas,
    guardar_figura,
    transf_logaritmica,
    transf_gamma,
    transf_a_trozos,
    igualacion_histograma,
)

# Técnicas a comparar contra el original
TECNICAS = [
    ("Log",        "Logarítmica",         transf_logaritmica),
    ("Gamma 0.5",  "Gamma γ=0.5",         lambda A: transf_gamma(A, 0.5)),
    ("A trozos",   "A trozos",            transf_a_trozos),
    ("Igualación", "Igualación histograma", igualacion_histograma),
]


def resta_absoluta(A, B):
    """
    Diferencia absoluta píxel a píxel entre dos imágenes.
    Se trabaja en int16 para evitar overflow de uint8 al restar.
    El resultado se clip a [0, 255] y se devuelve como uint8.

    C(x,y) = |A(x,y) - B(x,y)|
    """
    return np.abs(
        A.astype(np.int16) - B.astype(np.int16)
    ).clip(0, 255).astype(np.uint8)


def amplificar_diferencia(diff, factor=3):
    """
    Amplifica una imagen de diferencia para hacerla más visible.
    Muchas diferencias son pequeñas (1-5 niveles) y visualmente
    imperceptibles sin amplificación.

    Se escala al rango completo [0, 255] usando el valor máximo real,
    preservando las proporciones relativas entre zonas.
    """
    max_val = diff.max()
    if max_val == 0:
        return diff
    return np.clip(
        (diff.astype(np.float32) / max_val * 255), 0, 255
    ).astype(np.uint8)


def main():
    print("=" * 70)
    print("Script 06 — Resta de imágenes (mapas de diferencia)")
    print(f"Imagen: {IMAGEN_PROTAGONISTA}")
    print("=" * 70)

    img_orig = cargar_imagen(IMAGEN_PROTAGONISTA, escala_grises=True)
    n = len(TECNICAS)

    # -----------------------------------------------------------------
    # Figura 1: original | mejorada | diferencia absoluta | diff amplif.
    # 4 técnicas × 4 columnas
    # -----------------------------------------------------------------
    fig1 = plt.figure(figsize=(20, 5.5 * n))
    fig1.suptitle(
        f"Mapas de diferencia — {IMAGEN_PROTAGONISTA}\n"
        r"$C(x,y) = |A_{\mathrm{mejorada}}(x,y) - A_{\mathrm{original}}(x,y)|$",
        fontsize=13, fontweight="bold", y=0.999,
    )

    gs1 = gridspec.GridSpec(
        nrows=n, ncols=4,
        figure=fig1,
        width_ratios=[1.5, 1.5, 1.5, 1.5],
        hspace=0.4, wspace=0.2,
    )

    # Títulos de columna solo en la primera fila
    col_titles = [
        "Original",
        "Imagen mejorada",
        "Diferencia absoluta\n|mejorada − original|",
        "Diferencia amplificada\n(reescalada al rango [0,255])",
    ]

    filas = []

    for i, (etiq_corta, etiq_larga, funcion) in enumerate(TECNICAS):
        img_mejor = funcion(img_orig)
        diff      = resta_absoluta(img_orig, img_mejor)
        diff_amp  = amplificar_diferencia(diff)

        m_diff = calcular_metricas(diff)

        # Estadísticas de la diferencia
        pct_cambiado = np.mean(diff > 5) * 100   # % píxeles con cambio > 5
        cambio_medio = np.mean(diff[diff > 0])    # cambio medio en zonas activas

        ax0 = fig1.add_subplot(gs1[i, 0])
        ax1 = fig1.add_subplot(gs1[i, 1])
        ax2 = fig1.add_subplot(gs1[i, 2])
        ax3 = fig1.add_subplot(gs1[i, 3])

        # Títulos de columna en la primera fila
        titulo0 = col_titles[0] if i == 0 else ""
        titulo1 = (col_titles[1] if i == 0 else "") + f"\n{etiq_larga}"
        titulo2 = col_titles[2] if i == 0 else ""
        titulo3 = col_titles[3] if i == 0 else ""

        plot_imagen(ax0, img_orig,  titulo=titulo0)
        plot_imagen(ax1, img_mejor, titulo=titulo1)
        plot_imagen(ax2, diff,      titulo=titulo2)
        plot_imagen(ax3, diff_amp,  titulo=titulo3, cmap="hot")

        # Anotar estadísticas bajo cada mapa de diferencia
        ax2.set_xlabel(
            f"max_diff={diff.max()}  mean_diff={np.mean(diff):.1f}",
            fontsize=8,
        )
        ax3.set_xlabel(
            f"píxeles con Δ>5: {pct_cambiado:.1f}%  "
            f"cambio medio (activos): {cambio_medio:.1f}",
            fontsize=8,
        )

        filas.append({
            "técnica":           etiq_corta,
            "diff_max":          int(diff.max()),
            "diff_mean":         round(float(np.mean(diff)), 2),
            "diff_std":          round(float(np.std(diff)), 2),
            "pct_pixeles_>5":    round(pct_cambiado, 2),
            "cambio_medio_act":  round(float(cambio_medio), 2),
            "entropia_diff":     round(m_diff["entropía Shannon (bits)"], 3),
        })

        print(f"\n  {etiq_larga}")
        print(f"    diff_max={diff.max()}  "
              f"diff_mean={np.mean(diff):.1f}  "
              f"píxeles_Δ>5: {pct_cambiado:.1f}%  "
              f"cambio_medio_activos: {cambio_medio:.1f}")

    guardar_figura(fig1, "fig06_subtraction.png", dpi=130)
    plt.close(fig1)

    # -----------------------------------------------------------------
    # Figura 2: comparación gamma vs igualación — diferencia entre sí
    # -----------------------------------------------------------------
    img_gamma = transf_gamma(img_orig, 0.5)
    img_equal = igualacion_histograma(img_orig)
    diff_g_vs_e = resta_absoluta(img_gamma, img_equal)
    diff_g_vs_e_amp = amplificar_diferencia(diff_g_vs_e)

    fig2, axes2 = plt.subplots(1, 4, figsize=(20, 5))
    fig2.suptitle(
        "Diferencia entre técnicas — Gamma γ=0.5 vs Igualación de histograma\n"
        r"$C(x,y) = |\mathrm{Gamma}(x,y) - \mathrm{Igualación}(x,y)|$",
        fontsize=12, fontweight="bold",
    )

    plot_imagen(axes2[0], img_gamma,       titulo="Gamma γ=0.5")
    plot_imagen(axes2[1], img_equal,       titulo="Igualación histograma")
    plot_imagen(axes2[2], diff_g_vs_e,     titulo="Diferencia absoluta")
    plot_imagen(axes2[3], diff_g_vs_e_amp, titulo="Diferencia amplificada",
                cmap="hot")

    pct_distinto = np.mean(diff_g_vs_e > 10) * 100
    axes2[2].set_xlabel(
        f"max={diff_g_vs_e.max()}  mean={np.mean(diff_g_vs_e):.1f}",
        fontsize=9,
    )
    axes2[3].set_xlabel(
        f"Píxeles con diferencia >10: {pct_distinto:.1f}%",
        fontsize=9,
    )

    plt.tight_layout()
    guardar_figura(fig2, "fig06b_gamma_vs_equal.png", dpi=130)
    plt.close(fig2)

    # -----------------------------------------------------------------
    # Figura 3: histogramas de las diferencias superpuestos
    # -----------------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    fig3.suptitle(
        "Distribución de diferencias absolutas por técnica\n"
        "(solo se muestran valores > 0 para claridad)",
        fontsize=11, fontweight="bold",
    )

    colores = ["steelblue", "darkorange", "mediumpurple", "forestgreen"]
    for (etiq_corta, etiq_larga, funcion), color in zip(TECNICAS, colores):
        img_mejor = funcion(img_orig)
        diff = resta_absoluta(img_orig, img_mejor)
        vals_no_cero = diff[diff > 0].ravel()
        ax3.hist(vals_no_cero, bins=100, range=(0, 255),
                 color=color, alpha=0.55, label=etiq_larga, edgecolor="none")

    ax3.set_xlabel("Magnitud de la diferencia |mejorada − original|")
    ax3.set_ylabel("Frecuencia (píxeles con Δ > 0)")
    ax3.legend(fontsize=9)
    ax3.grid(alpha=0.3)
    ax3.set_xlim(0, 255)

    guardar_figura(fig3, "fig06c_hist_diferencias.png", dpi=130)
    plt.close(fig3)

    # -----------------------------------------------------------------
    # Tabla CSV
    # -----------------------------------------------------------------
    df = pd.DataFrame(filas)
    ruta_csv = OUT_TABLES / "tabla06_subtraction.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"\n  ✓ Tabla guardada: {ruta_csv.name}")

    print("\nResumen de diferencias absolutas:")
    print(df.to_string(index=False))

    # -----------------------------------------------------------------
    # Interpretación
    # -----------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Interpretación:")
    print("-" * 70)

    mayor_cambio   = df.loc[df["diff_mean"].idxmax(),  "técnica"]
    mayor_cobertur = df.loc[df["pct_pixeles_>5"].idxmax(), "técnica"]
    menor_cambio   = df.loc[df["diff_mean"].idxmin(),  "técnica"]

    print(f"  Técnica con mayor cambio promedio: {mayor_cambio} "
          f"(diff_mean={df['diff_mean'].max():.1f})")
    print(f"  Técnica con mayor cobertura (Δ>5): {mayor_cobertur} "
          f"({df['pct_pixeles_>5'].max():.1f}% de píxeles)")
    print(f"  Técnica con menor cambio promedio: {menor_cambio} "
          f"(diff_mean={df['diff_mean'].min():.1f})")
    print(f"\n  Diferencia entre Gamma 0.5 e Igualación:")
    print(f"    mean={np.mean(diff_g_vs_e):.1f}  "
          f"max={diff_g_vs_e.max()}  "
          f"píxeles con |Δ|>10: {pct_distinto:.1f}%")
    print()


if __name__ == "__main__":
    main()