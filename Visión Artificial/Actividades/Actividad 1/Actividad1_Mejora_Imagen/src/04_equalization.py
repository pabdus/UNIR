"""
04_equalization.py — Igualación de histograma sobre las 4 imágenes
del laboratorio (Familia 2 del Tema 6).

Para cada imagen se aplica la igualación de histograma implementada
manualmente a partir de la fórmula:
    B(x,y) = round[ (L-1) * CDA( A(x,y) ) ]
donde CDA es la función de distribución acumulada del histograma
normalizado de la imagen original.

La figura muestra para cada imagen:
    - Imagen original (gris)
    - Histograma original
    - Imagen ecualizada
    - Histograma ecualizado

Esto permite comparar visualmente el efecto de la técnica en imágenes
con distintos perfiles de histograma, evidenciando tanto las mejoras
como las limitaciones (amplificación de ruido, saturación de luces).
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
    igualacion_histograma,
)


def main():
    print("=" * 70)
    print("Script 04 — Igualación de histograma sobre las 4 imágenes")
    print("=" * 70)

    n = len(IMAGENES)

    # -----------------------------------------------------------------
    # Figura principal: 4 filas × 4 columnas
    # orig_img | orig_hist | equal_img | equal_hist
    # -----------------------------------------------------------------
    fig = plt.figure(figsize=(20, 5 * n))
    fig.suptitle(
        "Igualación de histograma — Las 4 imágenes Dark Face\n"
        r"$B(x,y) = \mathrm{round}\,[(L-1)\cdot\mathrm{CDA}(A(x,y))]$",
        fontsize=13, fontweight="bold", y=0.999,
    )

    gs = gridspec.GridSpec(
        nrows=n, ncols=4,
        figure=fig,
        width_ratios=[1.5, 1, 1.5, 1],
        hspace=0.4,
        wspace=0.3,
    )

    filas = []

    for i, nombre in enumerate(IMAGENES):
        print(f"\nProcesando {nombre}...")

        img_orig  = cargar_imagen(nombre, escala_grises=True)
        img_equal = igualacion_histograma(img_orig)

        m_orig  = calcular_metricas(img_orig)
        m_equal = calcular_metricas(img_equal)

        # Ganancia en cada métrica
        delta_std  = m_equal["std (RMS)"]              - m_orig["std (RMS)"]
        delta_ent  = m_equal["entropía Shannon (bits)"] - m_orig["entropía Shannon (bits)"]
        delta_mich = m_equal["contraste de Michelson"]  - m_orig["contraste de Michelson"]

        # --- Columna 0: imagen original ---
        ax_oi = fig.add_subplot(gs[i, 0])
        plot_imagen(ax_oi, img_orig,
                    titulo=f"{nombre} — Original")

        # --- Columna 1: histograma original ---
        ax_oh = fig.add_subplot(gs[i, 1])
        plot_histograma(ax_oh, img_orig, titulo="Histograma original")
        texto_orig = (f"std={m_orig['std (RMS)']:.1f}  "
                      f"H={m_orig['entropía Shannon (bits)']:.2f} bits")
        ax_oh.set_xlabel(f"Intensidad\n{texto_orig}", fontsize=8)

        # --- Columna 2: imagen ecualizada ---
        ax_ei = fig.add_subplot(gs[i, 2])
        plot_imagen(ax_ei, img_equal,
                    titulo=f"{nombre} — Ecualizada")

        # --- Columna 3: histograma ecualizado ---
        ax_eh = fig.add_subplot(gs[i, 3])
        plot_histograma(ax_eh, img_equal,
                        titulo="Histograma ecualizado",
                        color="darkorange")
        texto_equal = (f"std={m_equal['std (RMS)']:.1f}  "
                       f"H={m_equal['entropía Shannon (bits)']:.2f} bits")
        ax_eh.set_xlabel(f"Intensidad\n{texto_equal}", fontsize=8)

        filas.append({
            "imagen": nombre,
            "media_orig":    round(m_orig["media"], 2),
            "media_equal":   round(m_equal["media"], 2),
            "std_orig":      round(m_orig["std (RMS)"], 2),
            "std_equal":     round(m_equal["std (RMS)"], 2),
            "delta_std":     round(delta_std, 2),
            "entropia_orig": round(m_orig["entropía Shannon (bits)"], 3),
            "entropia_equal":round(m_equal["entropía Shannon (bits)"], 3),
            "delta_entropia":round(delta_ent, 3),
            "michelson_orig": round(m_orig["contraste de Michelson"], 3),
            "michelson_equal":round(m_equal["contraste de Michelson"], 3),
            "delta_michelson":round(delta_mich, 3),
        })

        print(f"  Original:   std={m_orig['std (RMS)']:.1f}  "
              f"H={m_orig['entropía Shannon (bits)']:.3f} bits  "
              f"Mich={m_orig['contraste de Michelson']:.3f}")
        print(f"  Ecualizada: std={m_equal['std (RMS)']:.1f}  "
              f"H={m_equal['entropía Shannon (bits)']:.3f} bits  "
              f"Mich={m_equal['contraste de Michelson']:.3f}")
        print(f"  Δstd={delta_std:+.1f}  "
              f"ΔH={delta_ent:+.3f}  "
              f"ΔMich={delta_mich:+.3f}")

    guardar_figura(fig, "fig04_equalization.png", dpi=150)
    plt.close(fig)

    # -----------------------------------------------------------------
    # Figura secundaria: barras comparativas de métricas
    # -----------------------------------------------------------------
    df = pd.DataFrame(filas)

    fig2, axes2 = plt.subplots(1, 3, figsize=(16, 5))
    fig2.suptitle(
        "Ganancia de métricas por igualación de histograma",
        fontsize=12, fontweight="bold",
    )

    nombres_cortos = [n.replace(".png", "") for n in df["imagen"]]
    x = np.arange(len(nombres_cortos))
    ancho = 0.35

    # Panel 1: std antes vs después
    axes2[0].bar(x - ancho/2, df["std_orig"],  ancho,
                 label="Original",   color="steelblue",  alpha=0.85)
    axes2[0].bar(x + ancho/2, df["std_equal"], ancho,
                 label="Ecualizada", color="darkorange", alpha=0.85)
    axes2[0].set_xticks(x)
    axes2[0].set_xticklabels(nombres_cortos)
    axes2[0].set_ylabel("Desviación estándar (contraste RMS)")
    axes2[0].set_title("Contraste RMS")
    axes2[0].legend()
    axes2[0].grid(axis="y", alpha=0.3)

    # Panel 2: entropía antes vs después
    axes2[1].bar(x - ancho/2, df["entropia_orig"],  ancho,
                 label="Original",   color="steelblue",  alpha=0.85)
    axes2[1].bar(x + ancho/2, df["entropia_equal"], ancho,
                 label="Ecualizada", color="darkorange", alpha=0.85)
    axes2[1].set_xticks(x)
    axes2[1].set_xticklabels(nombres_cortos)
    axes2[1].set_ylabel("Entropía Shannon (bits)")
    axes2[1].set_title("Entropía de Shannon")
    axes2[1].legend()
    axes2[1].grid(axis="y", alpha=0.3)

    # Panel 3: delta (ganancia) de cada métrica por imagen
    delta_std_vals  = df["delta_std"].values
    delta_ent_vals  = df["delta_entropia"].values * 10   # escalar para visualizar junto a std
    colores_delta   = ["green" if v > 0 else "red" for v in delta_std_vals]

    axes2[2].bar(x - ancho/2, delta_std_vals, ancho,
                 color=colores_delta, alpha=0.85, label="Δstd")
    axes2[2].bar(x + ancho/2, df["delta_entropia"] * 10, ancho,
                 color="mediumpurple", alpha=0.7,
                 label="ΔEntropía ×10")
    axes2[2].axhline(0, color="black", linewidth=0.8)
    axes2[2].set_xticks(x)
    axes2[2].set_xticklabels(nombres_cortos)
    axes2[2].set_ylabel("Ganancia (Δ)")
    axes2[2].set_title("Ganancia por ecualización")
    axes2[2].legend(fontsize=8)
    axes2[2].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    guardar_figura(fig2, "fig04b_equalization_metricas.png", dpi=150)
    plt.close(fig2)

    # -----------------------------------------------------------------
    # Tabla CSV
    # -----------------------------------------------------------------
    ruta_csv = OUT_TABLES / "tabla04_equalization_metricas.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"\n  ✓ Tabla guardada: {ruta_csv.name}")

    # -----------------------------------------------------------------
    # Resumen e interpretación
    # -----------------------------------------------------------------
    print("\nResumen comparativo:")
    cols_show = ["imagen", "std_orig", "std_equal", "delta_std",
                 "entropia_orig", "entropia_equal", "delta_entropia"]
    print(df[cols_show].to_string(index=False))

    print("\n" + "-" * 70)
    print("Interpretación:")
    print("-" * 70)

    mejor_std = df.loc[df["delta_std"].idxmax(), "imagen"]
    peor_std  = df.loc[df["delta_std"].idxmin(), "imagen"]
    mejor_ent = df.loc[df["delta_entropia"].idxmax(), "imagen"]

    print(f"  Mayor ganancia en contraste RMS:  {mejor_std} "
          f"(+{df['delta_std'].max():.1f})")
    print(f"  Menor ganancia en contraste RMS:  {peor_std} "
          f"({df['delta_std'].min():+.1f})")
    print(f"  Mayor ganancia en entropía:       {mejor_ent} "
          f"(+{df['delta_entropia'].max():.3f} bits)")

    # Detectar imágenes donde la ecualización pudo saturar luces
    for _, fila in df.iterrows():
        if fila["michelson_equal"] < fila["michelson_orig"]:
            print(f"  ⚠ {fila['imagen']}: Michelson BAJA tras ecualización "
                  f"({fila['michelson_orig']:.3f} → {fila['michelson_equal']:.3f}) "
                  f"— posible saturación de luces")
    print()


if __name__ == "__main__":
    main()