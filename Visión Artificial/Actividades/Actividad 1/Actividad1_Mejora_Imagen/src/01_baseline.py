"""
01_baseline.py — Caracterización de las imágenes del laboratorio.

Genera una figura que muestra las 4 imágenes seleccionadas del dataset
Dark Face junto con sus histogramas de intensidades en escala de grises,
y exporta una tabla con sus estadísticas descriptivas.

Esta figura sirve como punto de partida en la sección Resultados de la
memoria: documenta la condición inicial de las imágenes (subexposición,
concentración del histograma en valores bajos) que motiva la aplicación
de las técnicas de mejora.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Permitir importar utils.py desde el mismo directorio
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    IMAGENES,
    OUT_TABLES,
    cargar_imagen,
    cargar_imagen_color,
    plot_imagen,
    plot_histograma,
    calcular_metricas,
    guardar_figura,
)


def main():
    print("=" * 70)
    print("Script 01 — Línea base: caracterización de las 4 imágenes")
    print("=" * 70)

    # ---------------------------------------------------------------------
    # 1) Construir figura: imagen color | imagen gris | histograma
    # ---------------------------------------------------------------------
    fig, axes = plt.subplots(
        nrows=len(IMAGENES),
        ncols=3,
        figsize=(15, 4 * len(IMAGENES)),
        gridspec_kw={"width_ratios": [1.2, 1.2, 1]},
    )
    fig.suptitle(
        "Línea base — Imágenes Dark Face seleccionadas y sus histogramas",
        fontsize=14,
        fontweight="bold",
        y=0.995,
    )

    filas_metricas = []

    for i, nombre in enumerate(IMAGENES):
        print(f"\nProcesando {nombre}...")

        img_color = cargar_imagen_color(nombre)
        img_gris = cargar_imagen(nombre, escala_grises=True)

        h, w = img_gris.shape
        m = calcular_metricas(img_gris)

        # Imagen en color
        plot_imagen(
            axes[i, 0],
            img_color,
            titulo=f"{nombre}  ({h}×{w})  —  RGB",
            cmap=None,
        )

        # Imagen en escala de grises
        plot_imagen(
            axes[i, 1],
            img_gris,
            titulo=f"{nombre}  —  escala de grises",
            cmap="gray",
        )

        # Histograma
        plot_histograma(
            axes[i, 2],
            img_gris,
            titulo="Histograma",
        )

        # Acumular métricas para la tabla
        filas_metricas.append({
            "imagen": nombre,
            "alto": h,
            "ancho": w,
            **{k: round(v, 3) for k, v in m.items()},
        })

        print(f"  media={m['media']:.2f}  "
              f"std={m['std (RMS)']:.2f}  "
              f"entropía={m['entropía Shannon (bits)']:.3f} bits")

    plt.tight_layout(rect=[0, 0, 1, 0.99])

    # ---------------------------------------------------------------------
    # 2) Guardar figura
    # ---------------------------------------------------------------------
    guardar_figura(fig, "fig01_baseline.png", dpi=150)
    plt.close(fig)

    # ---------------------------------------------------------------------
    # 3) Construir y guardar tabla de métricas
    # ---------------------------------------------------------------------
    df = pd.DataFrame(filas_metricas)
    ruta_csv = OUT_TABLES / "tabla01_baseline_metricas.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"\n  ✓ Tabla guardada: {ruta_csv.name}")

    # Mostrar tabla por consola para inspección rápida
    print("\nMétricas iniciales:")
    print(df.to_string(index=False))

    # ---------------------------------------------------------------------
    # 4) Resumen interpretativo
    # ---------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Lectura del resultado:")
    print("-" * 70)
    media_global = df["media"].mean()
    entropia_max_teorica = 8.0  # bits para 8 bits/píxel
    entropia_global = df["entropía Shannon (bits)"].mean()
    pct_entropia_usada = entropia_global / entropia_max_teorica * 100

    print(f"  Media de intensidad promedio: {media_global:.2f} / 255")
    print(f"  Entropía promedio: {entropia_global:.3f} bits "
          f"({pct_entropia_usada:.1f}% del máximo teórico de 8 bits)")
    print(f"  Conclusión: las imágenes están severamente subexpuestas y")
    print(f"  desaprovechan el rango dinámico disponible. Esto justifica")
    print(f"  la aplicación de las técnicas de mejora del Tema 6.")
    print()


if __name__ == "__main__":
    main()