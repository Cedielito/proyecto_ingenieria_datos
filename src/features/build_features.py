# src/features/build_features.py
"""
PASO 3 - INGENIERÍA DE FEATURES
Responsabilidad: crear variables derivadas útiles para análisis o modelos.
"""
import pandas as pd
from src.utils.logger import logger

from src.config import PROCESSED_FILE
from src.dataset import save_dataframe


def add_total_venta(df: pd.DataFrame) -> pd.DataFrame:
    """Crea columna total_venta = cantidad * precio_unitario."""
    df["total_venta"] = df["cantidad"] * df["precio_unitario"]
    logger.info("  add_total_venta: columna 'total_venta' creada.")
    return df


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extrae año, mes y día de la semana de la fecha."""
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["dia_semana"] = df["fecha"].dt.day_name()
    logger.info("  add_temporal_features: columnas temporales creadas (anio, mes, dia_semana).")
    return df


def add_segmento_precio(df: pd.DataFrame) -> pd.DataFrame:
    """Clasifica productos por rango de precio."""
    def segmentar(precio):
        if precio < 100:
            return "Económico"
        elif precio < 500:
            return "Medio"
        else:
            return "Premium"

    df["segmento_precio"] = df["precio_unitario"].apply(segmentar)
    logger.info("  add_segmento_precio: columna 'segmento_precio' creada.")
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica toda la ingeniería de features y guarda el resultado final.

    Args:
        df: DataFrame limpio del paso anterior.

    Returns:
        pd.DataFrame: dataset final con todas las features.
    """
    logger.info("=" * 50)
    logger.info("PASO 3: INGENIERÍA DE FEATURES")
    logger.info("=" * 50)

    df = add_total_venta(df)
    df = add_temporal_features(df)
    df = add_segmento_precio(df)

    # Guardar resultado final
    save_dataframe(df, PROCESSED_FILE)

    logger.success(f"PASO 3 completado: tabla_final.csv con {len(df)} filas y {len(df.columns)} columnas.")
    logger.info(f"  Columnas finales: {list(df.columns)}")
    return df


if __name__ == "__main__":
    from src.preprocessing.clean_data import clean_data
    df_clean = clean_data()
    build_features(df_clean)
