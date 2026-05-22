"""
05_head_to_head.py — Comparación cabeza a cabeza de todas las técnicas
de mejora sobre las 4 imágenes del laboratorio.

Para cada imagen se aplican las 5 técnicas de mejora y se calculan
las 5 métricas de calidad. El resultado es una tabla comparativa
completa que permite identificar qué técnica funciona mejor en qué
imagen y bajo qué criterio.

Técnicas comparadas:
    1. Original (referencia)
    2. Logarítmica
    3. Gamma γ=0.5
    4. Función a trozos (parámetros calibrados)
    5. Igualación de histograma

Métricas:
    1. Media de intensidad (brillo)
    2. Desviación estándar / contraste RMS
    3. Rango dinámico efectivo (P99-P1)
    4. Contraste de Michelson
    5. Entropía de Shannon (bits)
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    IMAGENES,
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

# Técnicas a comparar: (etiqueta corta, etiqueta figura, función)
TECNICAS = [
    ("Original",    "Original\n(referencia)",          lambda A: A),
    ("Log",         "Logarítmica\nc·log(1+A)",          transf_logaritmica),
    ("Gamma 0.5",   "Gamma γ=0.5\n255·(A/255)^0.5",    lambda A: transf_gamma(A, 0.5)),
    ("A trozos",    "A trozos\nestiramiento contraste", transf_a_trozos),
    ("Igualación",  "Igualación\nhistograma",           igualacion_histograma),
]

METRICAS_COLS = [
    "media",
    "std (RMS)",
    "rango dinámico efectivo (P99-P1)",
    "contraste de Michelson",
    "entropía Shannon (bits)",
]

METRICAS_LABELS = [
    "Media",
    "Std (RMS)",
    "Rango efectivo\n(P99-P1)",
    "Michelson",
    "Entropía\n(bits)",
]


def main():
    print("=" * 70)
    print("Script 05 — Comparación cabeza a cabeza")
    print("=" * 70)

    todas_filas = []

    # -----------------------------------------------------------------
    # Figura 1: grilla imagen — 4 imágenes × 5 técnicas
    # -----------------------------------------------------------------
    n_imgs   = len(IMAGENES)
    n_tecnic = len(TECNICAS)

    fig1 = plt.figure(figsize=(5 * n_tecnic, 4.5 * n_imgs))
    fig1.suptitle(
        "Comparación cabeza a cabeza — 4 imágenes × 5 técnicas",
        fontsize=14, fontweight="bold", y=0.999,
    )

    gs1 = gridspec.GridSpec(
        nrows=n_imgs, ncols=n_tecnic,
        figure=fig1,
        hspace=0.35, wspace=0.15,
    )

    for i, nombre in enumerate(IMAGENES):
        img = cargar_imagen(nombre, escala_grises=True)

        for j, (etiq_corta, etiq_fig, funcion) in enumerate(TECNICAS):
            img_t = funcion(img)
            m     = calcular_metricas(img_t)

            ax = fig1.add_subplot(gs1[i, j])

            # Etiqueta de fila solo en la primera columna
            titulo = etiq_fig if i == 0 else ""
            if j == 0:
                titulo = (f"{nombre}\n" if i > 0 else "") + etiq_fig

            plot_imagen(ax, img_t, titulo=titulo)

            # Anotar std y entropía bajo cada imagen
            ax.set_xlabel(
                f"std={m['std (RMS)']:.1f}  "
                f"H={m['entropía Shannon (bits)']:.2f}b",
                fontsize=7,
            )

            todas_filas.append({
                "imagen":    nombre,
                "técnica":   etiq_corta,
                **{k: round(v, 3) for k, v in m.items()},
            })

        print(f"  ✓ {nombre} procesada")

    guardar_figura(fig1, "fig05_head_to_head.png", dpi=130)
    plt.close(fig1)

    # -----------------------------------------------------------------
    # Figura 2: heatmap de métricas normalizadas
    # -----------------------------------------------------------------
    df = pd.DataFrame(todas_filas)

    fig2, axes2 = plt.subplots(
        2, 2, figsize=(16, 12),
        constrained_layout=True,
    )
    fig2.suptitle(
        "Heatmap de métricas normalizadas por imagen\n"
        "(valor 1.0 = mejor técnica para esa imagen y métrica)",
        fontsize=12, fontweight="bold",
    )

    tecnicas_labels = [t[0] for t in TECNICAS]
    axes_flat = axes2.flatten()

    for idx, nombre in enumerate(IMAGENES):
        ax = axes_flat[idx]
        df_img = df[df["imagen"] == nombre].copy()

        # Matriz de métricas: filas=técnicas, columnas=métricas
        matriz = df_img[METRICAS_COLS].values.astype(float)

        # Normalizar cada columna al rango [0,1] respecto al máximo
        # (mayor siempre = mejor para todas las métricas usadas)
        col_max = matriz.max(axis=0)
        col_max[col_max == 0] = 1  # evitar división por cero
        matriz_norm = matriz / col_max

        im = ax.imshow(matriz_norm, cmap="YlGn",
                       vmin=0, vmax=1, aspect="auto")

        # Etiquetas de ejes
        ax.set_xticks(range(len(METRICAS_COLS)))
        ax.set_xticklabels(METRICAS_LABELS, fontsize=8)
        ax.set_yticks(range(len(TECNICAS)))
        ax.set_yticklabels(tecnicas_labels, fontsize=9)
        ax.set_title(nombre, fontsize=11, fontweight="bold")

        # Anotar valores originales dentro de cada celda
        for r in range(len(TECNICAS)):
            for c in range(len(METRICAS_COLS)):
                val_orig = matriz[r, c]
                val_norm = matriz_norm[r, c]
                color_txt = "black" if val_norm > 0.5 else "white"
                ax.text(c, r, f"{val_orig:.1f}",
                        ha="center", va="center",
                        fontsize=7, color=color_txt,
                        fontweight="bold" if val_norm == 1.0 else "normal")

        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                     label="Score normalizado")

    guardar_figura(fig2, "fig05b_heatmap_metricas.png", dpi=130)
    plt.close(fig2)

    # -----------------------------------------------------------------
    # Figura 3: ranking de técnicas por métrica (barras agrupadas)
    # -----------------------------------------------------------------
    fig3, axes3 = plt.subplots(
        1, len(METRICAS_COLS),
        figsize=(20, 6),
        constrained_layout=True,
    )
    fig3.suptitle(
        "Promedio de métricas por técnica (sobre las 4 imágenes)",
        fontsize=12, fontweight="bold",
    )

    colores_tecnicas = [
        "slategray", "steelblue", "darkorange",
        "mediumpurple", "forestgreen"
    ]

    for k, (col, label) in enumerate(zip(METRICAS_COLS, METRICAS_LABELS)):
        ax = axes3[k]
        promedios = [
            df[df["técnica"] == t[0]][col].mean()
            for t in TECNICAS
        ]
        bars = ax.bar(
            range(len(TECNICAS)), promedios,
            color=colores_tecnicas, alpha=0.85,
        )
        ax.set_xticks(range(len(TECNICAS)))
        ax.set_xticklabels(
            [t[0] for t in TECNICAS],
            rotation=30, ha="right", fontsize=8,
        )
        ax.set_title(label.replace("\n", " "), fontsize=9)
        ax.grid(axis="y", alpha=0.3)

        # Anotar valor encima de cada barra
        for bar, val in zip(bars, promedios):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f"{val:.1f}",
                ha="center", va="bottom", fontsize=7,
            )

    guardar_figura(fig3, "fig05c_ranking_tecnicas.png", dpi=130)
    plt.close(fig3)

    # -----------------------------------------------------------------
    # Tabla CSV completa
    # -----------------------------------------------------------------
    ruta_csv = OUT_TABLES / "tabla05_head_to_head.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"\n  ✓ Tabla guardada: {ruta_csv.name}")

    # -----------------------------------------------------------------
    # Tabla resumen: promedio por técnica
    # -----------------------------------------------------------------
    df_resumen = df.groupby("técnica")[METRICAS_COLS].mean().round(3)
    df_resumen = df_resumen.reindex([t[0] for t in TECNICAS])

    print("\nPromedio de métricas por técnica (sobre las 4 imágenes):")
    print(df_resumen.to_string())

    # -----------------------------------------------------------------
    # Identificar mejor técnica por métrica
    # -----------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Mejor técnica por métrica (promedio sobre las 4 imágenes):")
    print("-" * 70)
    for col in METRICAS_COLS:
        mejor = df_resumen[col].idxmax()
        valor = df_resumen[col].max()
        print(f"  {col:<42} → {mejor}  ({valor:.3f})")

    # -----------------------------------------------------------------
    # Identificar mejor técnica por imagen
    # -----------------------------------------------------------------
    print("\nMejor técnica por imagen según contraste RMS:")
    for nombre in IMAGENES:
        df_img  = df[df["imagen"] == nombre]
        df_sin_orig = df_img[df_img["técnica"] != "Original"]
        mejor   = df_sin_orig.loc[
            df_sin_orig["std (RMS)"].idxmax(), "técnica"
        ]
        val_std = df_sin_orig["std (RMS)"].max()
        print(f"  {nombre}: {mejor}  (std={val_std:.1f})")
    print()


if __name__ == "__main__":
    main()