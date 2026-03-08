# src/ingestion/load_data.py
"""
PASO 1 - INGESTA
Responsabilidad: cargar datos crudos desde disco o APIs externas.
"""
import pandas as pd
from src.utils.logger import logger

from src.config import RAW_FILE, INTERIM_FILE
from src.dataset import load_raw_dataframe, save_dataframe


def load_data() -> pd.DataFrame:
    """
    Carga el dataset crudo y lo persiste en data/interim/
    como primera copia de trabajo sin modificar los originales.

    Returns:
        pd.DataFrame: datos crudos sin transformar.
    """
    logger.info("=" * 50)
    logger.info("PASO 1: INGESTA DE DATOS")
    logger.info("=" * 50)

    # 1. Cargar CSV crudo
    df = load_raw_dataframe(RAW_FILE)

    # 2. Reporte básico de lo que llegó
    logger.info(f"  Columnas detectadas: {list(df.columns)}")
    logger.info(f"  Tipos de datos:\n{df.dtypes.to_string()}")
    logger.info(f"  Valores nulos por columna:\n{df.isnull().sum().to_string()}")

    # 3. Guardar copia interim (no modificar raw/)
    save_dataframe(df, INTERIM_FILE)

    logger.success("PASO 1 completado: datos cargados a data/interim/")
    return df


if __name__ == "__main__":
    load_data()
