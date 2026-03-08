# src/dataset.py
"""
Funciones de lectura y escritura de DataFrames.
Punto único de acceso a datos para todo el proyecto.
"""
import pandas as pd
from pathlib import Path
from src.utils.logger import logger


def load_raw_dataframe(path: Path) -> pd.DataFrame:
    """Carga un CSV crudo desde disco."""
    logger.info(f"Cargando datos crudos desde: {path}")
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    df = pd.read_csv(path)
    logger.info(f"  → {len(df)} filas, {len(df.columns)} columnas cargadas.")
    return df


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    """Guarda un DataFrame como CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.success(f"  → Guardado en: {path} ({len(df)} filas)")


def load_processed_dataframe(path: Path) -> pd.DataFrame:
    """Carga el CSV procesado final."""
    logger.info(f"Cargando datos procesados desde: {path}")
    if not path.exists():
        raise FileNotFoundError(
            f"Archivo procesado no encontrado: {path}\n"
            "  Ejecuta primero: python src/pipeline/main.py --mode full"
        )
    df = pd.read_csv(path, parse_dates=["fecha"])
    logger.info(f"  → {len(df)} filas cargadas.")
    return df
