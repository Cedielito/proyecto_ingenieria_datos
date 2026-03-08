# src/preprocessing/clean_data.py
import pandas as pd
from src.utils.logger import logger
from src.config import INTERIM_FILE, PROCESSED_DIR
from src.dataset import load_raw_dataframe, save_dataframe


def remove_nulls(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    critical_cols = ["Description", "Customer ID"]
    df = df.dropna(subset=critical_cols)
    logger.info(f"  remove_nulls: eliminadas {before - len(df)} filas con nulos críticos.")
    return df


def remove_invalid_quantities(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df[df["Quantity"] > 0]
    logger.info(f"  remove_invalid_quantities: eliminadas {before - len(df)} filas con Quantity <= 0.")
    return df


def remove_invalid_prices(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df[df["Price"] > 0]
    logger.info(f"  remove_invalid_prices: eliminadas {before - len(df)} filas con Price <= 0.")
    return df


def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    logger.info("  normalize_dates: columna 'InvoiceDate' convertida a datetime.")
    return df


def normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["Description", "Country"]:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()
    logger.info("  normalize_text: columnas Description y Country normalizadas.")
    return df


def clean_data() -> pd.DataFrame:
    logger.info("=" * 50)
    logger.info("PASO 2: LIMPIEZA Y NORMALIZACIÓN")
    logger.info("=" * 50)

    df = load_raw_dataframe(INTERIM_FILE)

    df = remove_nulls(df)
    df = remove_invalid_quantities(df)
    df = remove_invalid_prices(df)
    df = normalize_dates(df)
    df = normalize_text(df)

    clean_path = PROCESSED_DIR.parent / "interim" / "retail_clean.csv"
    save_dataframe(df, clean_path)

    logger.success(f"PASO 2 completado: {len(df)} filas limpias.")
    return df


if __name__ == "__main__":
    clean_data()
