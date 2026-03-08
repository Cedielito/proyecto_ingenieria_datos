# src/features/build_features.py
import pandas as pd
from src.utils.logger import logger
from src.config import PROCESSED_FILE
from src.dataset import save_dataframe


def add_total_venta(df: pd.DataFrame) -> pd.DataFrame:
    df["TotalPrice"] = df["Quantity"] * df["Price"]
    logger.info("  add_total_venta: columna 'TotalPrice' creada.")
    return df


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    df["Year"]      = df["InvoiceDate"].dt.year
    df["Month"]     = df["InvoiceDate"].dt.month
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    logger.info("  add_temporal_features: columnas Year, Month, DayOfWeek creadas.")
    return df


def add_segmento_precio(df: pd.DataFrame) -> pd.DataFrame:
    def segmentar(precio):
        if precio < 2:
            return "Economico"
        elif precio < 10:
            return "Medio"
        else:
            return "Premium"
    df["PriceSegment"] = df["Price"].apply(segmentar)
    logger.info("  add_segmento_precio: columna 'PriceSegment' creada.")
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("=" * 50)
    logger.info("PASO 3: INGENIERÍA DE FEATURES")
    logger.info("=" * 50)

    df = add_total_venta(df)
    df = add_temporal_features(df)
    df = add_segmento_precio(df)

    save_dataframe(df, PROCESSED_FILE)

    logger.success(f"PASO 3 completado: tabla_final.csv con {len(df)} filas y {len(df.columns)} columnas.")
    logger.info(f"  Columnas finales: {list(df.columns)}")
    return df


if __name__ == "__main__":
    from src.preprocessing.clean_data import clean_data
    df_clean = clean_data()
    build_features(df_clean)
