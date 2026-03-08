# src/plots.py
"""
Funciones para crear y guardar figuras en reports/figures/
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from src.utils.logger import logger

from src.config import FIGURES_DIR


def plot_ventas_por_categoria(df: pd.DataFrame, output_path: Path = None) -> None:
    """Genera gráfica de ventas totales por categoría."""
    if output_path is None:
        output_path = FIGURES_DIR / "ventas_por_categoria.png"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    ventas = df.groupby("categoria")["total_venta"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ventas.plot(kind="bar", ax=ax, color=["#2196F3", "#4CAF50", "#FF9800"])
    ax.set_title("Ventas Totales por Categoría", fontsize=14, fontweight="bold")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Total Ventas ($)")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    plt.close()
    logger.success(f"  → Figura guardada: {output_path}")


def plot_ventas_por_mes(df: pd.DataFrame, output_path: Path = None) -> None:
    """Genera gráfica de ventas por mes."""
    if output_path is None:
        output_path = FIGURES_DIR / "ventas_por_mes.png"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df["mes"] = pd.to_datetime(df["fecha"]).dt.to_period("M").astype(str)
    ventas_mes = df.groupby("mes")["total_venta"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    ventas_mes.plot(kind="line", ax=ax, marker="o", color="#2196F3", linewidth=2)
    ax.set_title("Evolución de Ventas por Mes", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Total Ventas ($)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    plt.close()
    logger.success(f"  → Figura guardada: {output_path}")
