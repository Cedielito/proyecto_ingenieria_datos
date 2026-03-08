# src/plots.py
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.utils.logger import logger
from src.config import FIGURES_DIR


def plot_ventas_por_categoria(df: pd.DataFrame) -> None:
    output_path = FIGURES_DIR / "ventas_por_pais.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    top10 = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    top10.plot(kind="bar", ax=ax, color="#2196F3")
    ax.set_title("Top 10 Países por Ventas Totales", fontsize=14, fontweight="bold")
    ax.set_xlabel("País")
    ax.set_ylabel("Total Ventas ($)")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(output_path, dpi=100)
    plt.close()
    logger.success(f"  Figura guardada: {output_path}")


def plot_ventas_por_mes(df: pd.DataFrame) -> None:
    output_path = FIGURES_DIR / "ventas_por_mes.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ventas_mes = df.groupby("Month")["TotalPrice"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    ventas_mes.plot(kind="line", ax=ax, marker="o", color="#2196F3", linewidth=2)
    ax.set_title("Evolución de Ventas por Mes", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Total Ventas ($)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=100)
    plt.close()
    logger.success(f"  Figura guardada: {output_path}")
