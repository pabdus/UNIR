"""
02_intensity_compare.py — Comparación de las cuatro transformaciones
de ajuste de intensidad (Familia 1 del Tema 6) sobre la imagen
protagonista del laboratorio (1033.png, la más oscura del conjunto).

Técnicas comparadas:
    1. Negativo:            B = 255 - A
    2. Transformación log:  B = c * log(1 + A)
    3. Gamma γ=0.3:         B = 255 * (A/255)^0.3
    4. Gamma γ=0.5:         B = 255 * (A/255)^0.5
    5. Función a trozos:    estiramiento de contraste lineal por segmentos

Para cada transformación se muestra:
    - Imagen resultante
    - Histograma con media y mediana
    - Métricas cuantitativas (tabla CSV)
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
    transf_negativo,
    transf_logaritmica,
    transf_gamma,
    transf_a_trozos,
)


# Definición de las transformaciones a comparar
# Cada entrada: (etiqueta en figura, función de transformación)
TRANSFORMACIONES = [
    ("Original",          lambda A: A),
    ("Negativo\nB=255-A", transf_negativo),
    ("Logarítmica\nB=c·log(1+A)",  transf_logaritmica),
    ("Gamma γ=0.3\nB=255·(A/255)^0.3", lambda A: transf_gamma(A, 0.3)),
    ("Gamma γ=0.5\nB=255·(A/255)^0.5", lambda A: transf_gamma(A, 0.5)),
    ("A trozos\nestiramiento de contraste",  transf_a_trozos),
]


def main():
    print("=" * 70)
    print("Script 02 — Comparación de transformaciones de intensidad")
    print(f"Imagen: {IMAGEN_PROTAGONISTA}")
    print("=" * 70)

    img = cargar_imagen(IMAGEN_PROTAGONISTA, escala_grises=True)
    n = len(TRANSFORMACIONES)

    # -----------------------------------------------------------------
    # Figura principal: imagen + histograma por cada transformación
    # -----------------------------------------------------------------
    fig = plt.figure(figsize=(18, 5 * n))
    fig.suptitle(
        f"Comparación de transformaciones de intensidad — {IMAGEN_PROTAGONISTA}\n"
        "(Familia 1: ajuste de intensidad punto a punto)",
        fontsize=13, fontweight="bold", y=0.999,
    )

    gs = gridspec.GridSpec(
        nrows=n, ncols=2,
        figure=fig,
        width_ratios=[1.8, 1],
        hspace=0.45,
        wspace=0.25,
    )

    filas = []

    for i, (etiqueta, funcion) in enumerate(TRANSFORMACIONES):
        img_transf = funcion(img)
        m = calcular_metricas(img_transf)

        # Imagen transformada
        ax_img  = fig.add_subplot(gs[i, 0])
        ax_hist = fig.add_subplot(gs[i, 1])

        titulo_img = etiqueta.replace("\n", "  |  ")
        plot_imagen(ax_img,  img_transf, titulo=titulo_img)
        plot_histograma(ax_hist, img_transf, titulo="Histograma")

        # Anotar métricas clave sobre el histograma
        texto = (
            f"std={m['std (RMS)']:.1f}  "
            f"H={m['entropía Shannon (bits)']:.2f} bits  "
            f"Mich={m['contraste de Michelson']:.3f}"
        )
        ax_hist.set_xlabel(f"Intensidad\n{texto}", fontsize=8)

        nombre_corto = etiqueta.split("\n")[0]
        filas.append({
            "transformación": nombre_corto,
            **{k: round(v, 3) for k, v in m.items()},
        })

        print(f"\n  {nombre_corto}")
        print(f"    media={m['media']:.1f}  "
              f"std={m['std (RMS)']:.1f}  "
              f"entropía={m['entropía Shannon (bits)']:.3f} bits  "
              f"Michelson={m['contraste de Michelson']:.3f}")

    guardar_figura(fig, "fig02_intensity_compare.png", dpi=150)
    plt.close(fig)

    # -----------------------------------------------------------------
    # Figura secundaria: curvas de transformación T(A) superpuestas
    # -----------------------------------------------------------------
    fig2, ax = plt.subplots(figsize=(8, 6))
    fig2.suptitle(
        "Curvas de transformación T(A) — Familia 1",
        fontsize=12, fontweight="bold",
    )

    A_vals = np.arange(256, dtype=np.float64)
    colores = ["black", "crimson", "steelblue", "darkorange",
               "forestgreen", "mediumpurple"]

    for (etiqueta, funcion), color in zip(TRANSFORMACIONES, colores):
        # Calcular T(k) para cada k en [0, 255]
        T_vals = np.array([funcion(np.array([[k]], dtype=np.uint8))[0, 0]
                           for k in range(256)], dtype=np.float64)
        nombre_curva = etiqueta.replace("\n", " | ")
        ax.plot(A_vals, T_vals, color=color, linewidth=2,
                label=nombre_curva)

    ax.plot([0, 255], [0, 255], "k--", linewidth=0.8,
            alpha=0.4, label="Identidad (referencia)")
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_xlabel("Intensidad de entrada A")
    ax.set_ylabel("Intensidad de salida B = T(A)")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
    ax.set_aspect("equal")

    guardar_figura(fig2, "fig02b_curvas_transformacion.png", dpi=150)
    plt.close(fig2)

    # -----------------------------------------------------------------
    # Tabla CSV con métricas comparativas
    # -----------------------------------------------------------------
    df = pd.DataFrame(filas)
    ruta_csv = OUT_TABLES / "tabla02_intensity_metricas.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"\n  ✓ Tabla guardada: {ruta_csv.name}")

    print("\nResumen comparativo:")
    print(df.to_string(index=False))

    # -----------------------------------------------------------------
    # Interpretación automática
    # -----------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Interpretación:")
    print("-" * 70)

    df_sin_neg = df[df["transformación"] != "Negativo"]
    mejor_std  = df_sin_neg.loc[df_sin_neg["std (RMS)"].idxmax(),
                                "transformación"]
    mejor_ent  = df_sin_neg.loc[
        df_sin_neg["entropía Shannon (bits)"].idxmax(), "transformación"
    ]

    orig = df[df["transformación"] == "Original"].iloc[0]
    neg  = df[df["transformación"] == "Negativo"].iloc[0]

    print(f"  Mayor contraste RMS (excl. negativo): {mejor_std}")
    print(f"  Mayor entropía     (excl. negativo): {mejor_ent}")
    print(f"  Negativo: misma std que original "
          f"({neg['std (RMS)']:.1f} ≈ {orig['std (RMS)']:.1f}), "
          f"confirma que no mejora el contraste.")
    print()


if __name__ == "__main__":
    main()