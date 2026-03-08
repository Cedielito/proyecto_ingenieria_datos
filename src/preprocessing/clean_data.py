# src/preprocessing/clean_data.py
"""
PASO 2 - PREPROCESAMIENTO
Responsabilidad: limpiar y normalizar los datos crudos.
"""
import pandas as pd
from src.utils.logger import logger

from src.config import INTERIM_FILE, PROCESSED_DIR
from src.dataset import load_raw_dataframe, save_dataframe


def remove_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas con valores nulos en columnas críticas."""
    before = len(df)
    critical_cols = ["producto", "precio_unitario"]
    df = df.dropna(subset=critical_cols)
    removed = before - len(df)
    logger.info(f"  remove_nulls: eliminadas {removed} filas con nulos críticos.")
    return df


def remove_invalid_quantities(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas donde cantidad <= 0 (datos inválidos)."""
    before = len(df)
    df = df[df["cantidad"] > 0]
    removed = before - len(df)
    logger.info(f"  remove_invalid_quantities: eliminadas {removed} filas con cantidad ≤ 0.")
    return df


def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte la columna fecha a tipo datetime."""
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    logger.info("  normalize_dates: columna 'fecha' convertida a datetime.")
    return df


def normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza columnas de texto: strip y title case."""
    text_cols = ["producto", "categoria", "region", "vendedor"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()
    logger.info(f"  normalize_text: normalizadas columnas {text_cols}.")
    return df


def clean_data() -> pd.DataFrame:
    """
    Ejecuta todas las transformaciones de limpieza en secuencia.

    Returns:
        pd.DataFrame: datos limpios y normalizados.
    """
    logger.info("=" * 50)
    logger.info("PASO 2: LIMPIEZA Y NORMALIZACIÓN")
    logger.info("=" * 50)

    df = load_raw_dataframe(INTERIM_FILE)

    df = remove_nulls(df)
    df = remove_invalid_quantities(df)
    df = normalize_dates(df)
    df = normalize_text(df)

    # Guardar versión limpia en interim (aún no es el final)
    clean_path = PROCESSED_DIR.parent / "interim" / "ventas_clean.csv"
    save_dataframe(df, clean_path)

    logger.success(f"PASO 2 completado: {len(df)} filas limpias.")
    return df


if __name__ == "__main__":
    clean_data()
