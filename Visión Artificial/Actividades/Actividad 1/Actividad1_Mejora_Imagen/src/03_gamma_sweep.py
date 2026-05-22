"""
03_gamma_sweep.py — Barrido paramétrico de la corrección gamma.

Demuestra el efecto del parámetro γ sobre la imagen protagonista
(1033.png) evaluando seis valores: 0.2, 0.3, 0.5, 0.7, 1.0, 1.5.

γ = 1.0 es la identidad (control).
γ < 1   aclara la imagen (expande tonos bajos).
γ > 1   oscurece la imagen (comprime tonos bajos).

Esta figura ilustra la naturaleza paramétrica de la corrección gamma
y justifica la elección de γ=0.5 como valor de trabajo en los
experimentos siguientes.
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
    transf_gamma,
)

# Valores de gamma a evaluar
GAMMAS = [0.2, 0.3, 0.5, 0.7, 1.0, 1.5]


def main():
    print("=" * 70)
    print("Script 03 — Barrido paramétrico de gamma")
    print(f"Imagen: {IMAGEN_PROTAGONISTA}")
    print(f"Valores de γ: {GAMMAS}")
    print("=" * 70)

    img = cargar_imagen(IMAGEN_PROTAGONISTA, escala_grises=True)
    n = len(GAMMAS)

    # -----------------------------------------------------------------
    # Figura 1: imagen + histograma por cada gamma
    # -----------------------------------------------------------------
    fig = plt.figure(figsize=(16, 4.2 * n))
    fig.suptitle(
        f"Barrido paramétrico — Corrección gamma sobre {IMAGEN_PROTAGONISTA}\n"
        r"$B = 255 \cdot (A/255)^{\gamma}$",
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

    for i, gamma in enumerate(GAMMAS):
        img_transf = transf_gamma(img, gamma)
        m = calcular_metricas(img_transf)

        ax_img  = fig.add_subplot(gs[i, 0])
        ax_hist = fig.add_subplot(gs[i, 1])

        # Etiqueta especial para la identidad
        if gamma == 1.0:
            etiqueta = f"γ = {gamma:.1f}  (identidad — sin cambio)"
        elif gamma < 1.0:
            etiqueta = f"γ = {gamma}  →  aclara"
        else:
            etiqueta = f"γ = {gamma}  →  oscurece"

        plot_imagen(ax_img,  img_transf, titulo=etiqueta)
        plot_histograma(ax_hist, img_transf, titulo="Histograma")

        texto = (
            f"media={m['media']:.1f}  "
            f"std={m['std (RMS)']:.1f}  "
            f"H={m['entropía Shannon (bits)']:.2f} bits"
        )
        ax_hist.set_xlabel(f"Intensidad\n{texto}", fontsize=8)

        filas.append({
            "gamma": gamma,
            "efecto": "aclara" if gamma < 1 else ("identidad" if gamma == 1 else "oscurece"),
            **{k: round(v, 3) for k, v in m.items()},
        })

        print(f"\n  γ={gamma}: media={m['media']:.1f}  "
              f"std={m['std (RMS)']:.1f}  "
              f"entropía={m['entropía Shannon (bits)']:.3f} bits")

    guardar_figura(fig, "fig03_gamma_sweep.png", dpi=150)
    plt.close(fig)

    # -----------------------------------------------------------------
    # Figura 2: curvas gamma superpuestas + métricas vs gamma
    # -----------------------------------------------------------------
    fig2, axes2 = plt.subplots(1, 3, figsize=(16, 5))
    fig2.suptitle(
        r"Análisis cuantitativo del barrido $\gamma$",
        fontsize=12, fontweight="bold",
    )

    # Panel izquierdo: curvas T(A) para cada gamma
    A_vals = np.linspace(0, 255, 500)
    colores = ["#e41a1c", "#ff7f00", "#4daf4a",
               "#377eb8", "#000000", "#984ea3"]

    for gamma, color in zip(GAMMAS, colores):
        T_vals = 255.0 * np.power(A_vals / 255.0, gamma)
        estilo = "--" if gamma == 1.0 else "-"
        axes2[0].plot(A_vals, T_vals, color=color,
                      linewidth=2, linestyle=estilo,
                      label=f"γ={gamma}")

    axes2[0].set_xlabel("Intensidad de entrada A")
    axes2[0].set_ylabel("Intensidad de salida B")
    axes2[0].set_title("Curvas de transformación T(A)")
    axes2[0].legend(fontsize=9)
    axes2[0].grid(alpha=0.3)
    axes2[0].set_aspect("equal")

    # Panel central: media vs gamma
    df = pd.DataFrame(filas)
    axes2[1].plot(df["gamma"], df["media"], "o-",
                  color="steelblue", linewidth=2, markersize=7)
    axes2[1].axhline(128, color="gray", linestyle="--",
                     linewidth=1, label="Media ideal=128")
    axes2[1].set_xlabel("γ")
    axes2[1].set_ylabel("Media de intensidad")
    axes2[1].set_title("Brillo medio vs γ")
    axes2[1].legend(fontsize=9)
    axes2[1].grid(alpha=0.3)

    # Panel derecho: std y entropía vs gamma (doble eje Y)
    ax_std = axes2[2]
    ax_ent = ax_std.twinx()

    l1, = ax_std.plot(df["gamma"], df["std (RMS)"], "s-",
                      color="crimson", linewidth=2,
                      markersize=7, label="std (RMS)")
    l2, = ax_ent.plot(df["gamma"], df["entropía Shannon (bits)"],
                      "^-", color="forestgreen", linewidth=2,
                      markersize=7, label="Entropía (bits)")

    ax_std.set_xlabel("γ")
    ax_std.set_ylabel("Desviación estándar (contraste RMS)", color="crimson")
    ax_ent.set_ylabel("Entropía Shannon (bits)", color="forestgreen")
    ax_std.set_title("Contraste y entropía vs γ")
    ax_std.tick_params(axis="y", labelcolor="crimson")
    ax_ent.tick_params(axis="y", labelcolor="forestgreen")
    ax_std.grid(alpha=0.3)
    lines = [l1, l2]
    ax_std.legend(lines, [l.get_label() for l in lines],
                  fontsize=9, loc="upper right")

    plt.tight_layout()
    guardar_figura(fig2, "fig03b_gamma_metricas.png", dpi=150)
    plt.close(fig2)

    # -----------------------------------------------------------------
    # Tabla CSV
    # -----------------------------------------------------------------
    ruta_csv = OUT_TABLES / "tabla03_gamma_sweep.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"\n  ✓ Tabla guardada: {ruta_csv.name}")

    print("\nResumen:")
    print(df[["gamma", "efecto", "media",
              "std (RMS)", "entropía Shannon (bits)"]].to_string(index=False))

    # -----------------------------------------------------------------
    # Interpretación
    # -----------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Interpretación:")
    print("-" * 70)

    gamma_max_std = df.loc[df["std (RMS)"].idxmax(), "gamma"]
    gamma_max_ent = df.loc[df["entropía Shannon (bits)"].idxmax(), "gamma"]
    gamma_mas_cercano_128 = df.loc[
        (df["media"] - 128).abs().idxmin(), "gamma"
    ]

    print(f"  γ con mayor contraste RMS:  {gamma_max_std}")
    print(f"  γ con mayor entropía:       {gamma_max_ent}")
    print(f"  γ con media más cercana a 128 (brillo equilibrado): "
          f"{gamma_mas_cercano_128}")
    print()


if __name__ == "__main__":
    main()