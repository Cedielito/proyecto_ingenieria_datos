# src/ingestion/load_data.py
import pandas as pd
from src.utils.logger import logger
from src.config import RAW_FILE, INTERIM_FILE
from src.dataset import load_raw_dataframe, save_dataframe


def load_data() -> pd.DataFrame:
    logger.info("=" * 50)
    logger.info("PASO 1: INGESTA DE DATOS")
    logger.info("=" * 50)

    df = load_raw_dataframe(RAW_FILE)

    logger.info(f"  Columnas detectadas: {list(df.columns)}")
    logger.info(f"  Valores nulos por columna:\n{df.isnull().sum().to_string()}")
    logger.info(f"  Negativos en Quantity: {(df['Quantity'] < 0).sum()}")
    logger.info(f"  Negativos en Price: {(df['Price'] <= 0).sum()}")

    save_dataframe(df, INTERIM_FILE)

    logger.success("PASO 1 completado: datos cargados a data/interim/")
    return df


if __name__ == "__main__":
    load_data()
