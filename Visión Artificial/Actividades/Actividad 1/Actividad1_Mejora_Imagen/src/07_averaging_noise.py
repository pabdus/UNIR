"""
07_averaging_noise.py — Reducción de ruido por promediado de capturas
(Familia 3, parte B).

Demuestra experimentalmente la propiedad:
    sigma_C^2 = sigma^2 / M

donde sigma^2 es la varianza del ruido en una sola captura y M es el
número de capturas promediadas.

Como el dataset Dark Face no provee múltiples capturas de la misma
escena, se simula el proceso:
    1. Se toma la imagen mejorada con gamma 0.5 (imagen base limpia)
    2. Se generan M versiones ruidosas añadiendo ruido gaussiano
       sintético con desviación estándar sigma_ruido
    3. Se promedia un subconjunto creciente de capturas
    4. Se mide la desviación estándar del ruido residual y se compara
       contra el valor teórico sigma / sqrt(M)

Este experimento cierra el laboratorio demostrando que incluso técnicas
simples (promediado aritmético) tienen fundamento estadístico riguroso
y son capaces de mejorar la calidad de imagen cuando se dispone de
múltiples capturas.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    IMAGEN_PROTAGONISTA,
    OUT_TABLES,
    cargar_imagen,
    plot_imagen,
    guardar_figura,
    transf_gamma,
)

# Parámetros del experimento
SIGMA_RUIDO  = 25.0        # desviación estándar del ruido gaussiano añadido
VALORES_M    = [1, 2, 4, 8, 16, 32, 64]  # número de capturas a promediar
SEMILLA      = 42          # semilla para reproducibilidad


def agregar_ruido_gaussiano(img_limpia, sigma, rng):
    """
    Añade ruido gaussiano a una imagen.

    Parámetros
    ----------
    img_limpia : np.ndarray (H, W) uint8
        Imagen sin ruido.
    sigma : float
        Desviación estándar del ruido gaussiano en niveles de intensidad.
    rng : np.random.Generator
        Generador de números aleatorios (para reproducibilidad).

    Devuelve
    --------
    np.ndarray (H, W) uint8
        Imagen con ruido añadido, clippeada a [0, 255].
    """
    ruido = rng.normal(loc=0.0, scale=sigma,
                       size=img_limpia.shape)
    img_ruidosa = img_limpia.astype(np.float32) + ruido
    return np.clip(img_ruidosa, 0, 255).astype(np.uint8)


def medir_sigma_ruido(img_base, img_promediada):
    """
    Estima la desviación estándar del ruido residual comparando la
    imagen promediada con la imagen base limpia.

    sigma_residual = std(img_promediada - img_base)

    Esta es la medición experimental de cuánto ruido queda tras
    promediar M capturas.
    """
    diff = img_promediada.astype(np.float32) - img_base.astype(np.float32)
    return float(np.std(diff))


def promediar_capturas(img_base, M, sigma, rng):
    """
    Genera M capturas ruidosas de img_base y las promedia.

    El promedio se hace en float32 para evitar errores de redondeo
    acumulados al sumar muchas imágenes uint8.

    Devuelve la imagen promediada como uint8.
    """
    acumulador = np.zeros(img_base.shape, dtype=np.float32)
    for _ in range(M):
        captura = agregar_ruido_gaussiano(img_base, sigma, rng)
        acumulador += captura.astype(np.float32)
    promedio = acumulador / M
    return np.clip(promedio, 0, 255).astype(np.uint8)


def main():
    print("=" * 70)
    print("Script 07 — Promediado para reducción de ruido (simulado)")
    print(f"Imagen base: gamma 0.5 sobre {IMAGEN_PROTAGONISTA}")
    print(f"Sigma ruido añadido: {SIGMA_RUIDO}")
    print(f"Valores de M: {VALORES_M}")
    print("=" * 70)

    # Imagen base limpia: 1033 mejorada con gamma 0.5
    img_orig = cargar_imagen(IMAGEN_PROTAGONISTA, escala_grises=True)
    img_base = transf_gamma(img_orig, 0.5)

    rng = np.random.default_rng(seed=SEMILLA)

    # -----------------------------------------------------------------
    # Experimento: promediar M capturas y medir sigma residual
    # -----------------------------------------------------------------
    filas = []

    print(f"\n{'M':>5}  {'σ teórico':>12}  {'σ medido':>12}  "
          f"{'error %':>10}")
    print("-" * 45)

    for M in VALORES_M:
        sigma_teorico = SIGMA_RUIDO / np.sqrt(M)
        img_prom      = promediar_capturas(img_base, M, SIGMA_RUIDO, rng)
        sigma_medido  = medir_sigma_ruido(img_base, img_prom)
        error_pct     = abs(sigma_medido - sigma_teorico) / sigma_teorico * 100

        filas.append({
            "M":             M,
            "sigma_teorico": round(sigma_teorico, 3),
            "sigma_medido":  round(sigma_medido, 3),
            "error_%":       round(error_pct, 2),
            "reduccion_x":   round(SIGMA_RUIDO / sigma_medido, 2),
        })

        print(f"  {M:>3}  {sigma_teorico:>12.3f}  "
              f"{sigma_medido:>12.3f}  {error_pct:>10.2f}%")

    df = pd.DataFrame(filas)

    # -----------------------------------------------------------------
    # Figura 1: galería de imágenes promediadas
    # -----------------------------------------------------------------
    M_mostrar = [1, 4, 16, 64]
    rng2      = np.random.default_rng(seed=SEMILLA)   # misma semilla

    fig1, axes1 = plt.subplots(2, len(M_mostrar),
                               figsize=(5 * len(M_mostrar), 10))
    fig1.suptitle(
        f"Reducción de ruido por promediado — base: gamma 0.5 sobre "
        f"{IMAGEN_PROTAGONISTA}\n"
        r"$\sigma_C = \sigma / \sqrt{M}$"
        f"  con σ={SIGMA_RUIDO}",
        fontsize=12, fontweight="bold", y=0.999,
    )

    for j, M in enumerate(M_mostrar):
        img_prom = promediar_capturas(img_base, M, SIGMA_RUIDO,
                                      np.random.default_rng(seed=SEMILLA+j))
        sigma_t  = SIGMA_RUIDO / np.sqrt(M)
        sigma_m  = medir_sigma_ruido(img_base, img_prom)

        # Fila superior: imagen promediada
        plot_imagen(axes1[0, j], img_prom,
                    titulo=f"M = {M} captura{'s' if M > 1 else ''}")
        axes1[0, j].set_xlabel(
            f"σ teórico={sigma_t:.2f}  σ medido={sigma_m:.2f}",
            fontsize=9,
        )

        # Fila inferior: imagen de diferencia (ruido residual)
        diff = np.abs(
            img_prom.astype(np.int16) - img_base.astype(np.int16)
        ).clip(0, 255).astype(np.uint8)
        # Amplificar para visibilidad
        max_d = diff.max()
        if max_d > 0:
            diff_amp = (diff.astype(np.float32) / max_d * 255).astype(np.uint8)
        else:
            diff_amp = diff

        plot_imagen(axes1[1, j], diff_amp,
                    titulo=f"Ruido residual (M={M})", cmap="hot")
        axes1[1, j].set_xlabel(
            f"std_residual={sigma_m:.2f}  "
            f"reducción: {SIGMA_RUIDO/max(sigma_m,0.01):.1f}×",
            fontsize=9,
        )

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    guardar_figura(fig1, "fig07_averaging.png", dpi=130)
    plt.close(fig1)

    # -----------------------------------------------------------------
    # Figura 2: verificación experimental de sigma/sqrt(M)
    # -----------------------------------------------------------------
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
    fig2.suptitle(
        r"Verificación experimental de $\sigma_C = \sigma / \sqrt{M}$",
        fontsize=12, fontweight="bold",
    )

    M_vals       = df["M"].values
    sigma_teo    = df["sigma_teorico"].values
    sigma_med    = df["sigma_medido"].values

    # Panel izquierdo: sigma teórico vs medido
    axes2[0].plot(M_vals, sigma_teo, "o--",
                  color="steelblue", linewidth=2,
                  markersize=7, label=r"$\sigma/\sqrt{M}$ (teórico)")
    axes2[0].plot(M_vals, sigma_med, "s-",
                  color="crimson",   linewidth=2,
                  markersize=7, label="σ medido (experimental)")
    axes2[0].axhline(SIGMA_RUIDO, color="gray", linestyle=":",
                     linewidth=1.5, label=f"σ original = {SIGMA_RUIDO}")
    axes2[0].set_xlabel("Número de capturas M")
    axes2[0].set_ylabel("Desviación estándar del ruido")
    axes2[0].set_title("σ teórico vs σ medido")
    axes2[0].legend(fontsize=9)
    axes2[0].grid(alpha=0.3)
    axes2[0].set_xscale("log")

    # Panel derecho: escala logarítmica para ambos ejes
    axes2[1].loglog(M_vals, sigma_teo, "o--",
                    color="steelblue", linewidth=2,
                    markersize=7, label=r"$\sigma/\sqrt{M}$ (teórico)")
    axes2[1].loglog(M_vals, sigma_med, "s-",
                    color="crimson",   linewidth=2,
                    markersize=7, label="σ medido (experimental)")

    # Línea de referencia con pendiente -0.5 (la ley de potencia)
    M_ref   = np.array([1, 64], dtype=float)
    sig_ref = SIGMA_RUIDO * M_ref**(-0.5)
    axes2[1].loglog(M_ref, sig_ref, "k--", linewidth=1,
                    alpha=0.5, label="Pendiente −0.5 (referencia)")

    axes2[1].set_xlabel("Número de capturas M (escala log)")
    axes2[1].set_ylabel("σ ruido (escala log)")
    axes2[1].set_title("Escala log-log — verifica la ley de potencia")
    axes2[1].legend(fontsize=9)
    axes2[1].grid(alpha=0.3, which="both")

    plt.tight_layout()
    guardar_figura(fig2, "fig07b_sigma_verificacion.png", dpi=130)
    plt.close(fig2)

    # -----------------------------------------------------------------
    # Tabla CSV
    # -----------------------------------------------------------------
    ruta_csv = OUT_TABLES / "tabla07_averaging.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"\n  ✓ Tabla guardada: {ruta_csv.name}")

    # -----------------------------------------------------------------
    # Interpretación
    # -----------------------------------------------------------------
    print("\nTabla de verificación:")
    print(df.to_string(index=False))

    print("\n" + "-" * 70)
    print("Interpretación:")
    print("-" * 70)

    # Verificar cuán bien se cumple la ley teórica
    error_max  = df["error_%"].max()
    error_mean = df["error_%"].mean()
    M_64       = df[df["M"] == 64].iloc[0]

    print(f"  Error máximo entre σ teórico y medido: {error_max:.2f}%")
    print(f"  Error medio: {error_mean:.2f}%")
    print(f"  Con M=64: σ medido={M_64['sigma_medido']:.3f} "
          f"vs σ teórico={M_64['sigma_teorico']:.3f} "
          f"→ reducción {M_64['reduccion_x']:.1f}×")
    print()
    print("  Limitación experimental:")
    print("  El dataset Dark Face provee una sola captura por escena.")
    print("  Este experimento simula múltiples capturas añadiendo ruido")
    print("  gaussiano sintético. En un escenario real, el promediado")
    print("  requeriría M exposiciones físicas de la misma escena.")
    print("  Datasets como SIDD (Smartphone Image Denoising Dataset)")
    print("  proveen capturas reales múltiples y permitirían validar")
    print("  esta propiedad sin simulación.")
    print()


if __name__ == "__main__":
    main()