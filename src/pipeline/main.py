#!/usr/bin/env python3
# src/pipeline/main.py
import argparse
from src.utils.logger import logger

MODOS_VALIDOS = ["full", "ingest", "clean", "features", "report"]


def parse_args():
    parser = argparse.ArgumentParser(
        prog="pipeline-etl",
        description="Pipeline ETL modular - Online Retail II (1M+ filas).",
    )
    parser.add_argument(
        "--mode", "-m",
        type=str,
        choices=MODOS_VALIDOS,
        default="full",
        help="Modo: full | ingest | clean | features | report",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()


def run(mode: str) -> None:
    from src.config import verify_structure

    logger.info("=" * 55)
    logger.info("  PIPELINE ETL - ONLINE RETAIL II (1M+ registros)")
    logger.info("=" * 55)
    logger.info(f"Modo de ejecucion: [{mode.upper()}]")

    verify_structure()
    df = None

    if mode in ("full", "ingest"):
        from src.ingestion.load_data import load_data
        df = load_data()

    if mode in ("full", "clean"):
        from src.preprocessing.clean_data import clean_data
        df = clean_data()

    if mode in ("full", "features"):
        if mode == "features":
            from src.preprocessing.clean_data import clean_data
            df = clean_data()
        from src.features.build_features import build_features
        df = build_features(df)

    if mode in ("full", "report"):
        if mode == "report":
            from src.config import PROCESSED_FILE
            from src.dataset import load_processed_dataframe
            df = load_processed_dataframe(PROCESSED_FILE)
        if df is not None:
            _generate_report(df)

    logger.info("=" * 55)
    logger.success("PIPELINE COMPLETADO EXITOSAMENTE")
    logger.info("=" * 55)


def _generate_report(df) -> None:
    logger.info("=" * 55)
    logger.info("PASO 4: GENERACION DE REPORTE")
    logger.info("=" * 55)

    total_ventas = df["TotalPrice"].sum()
    pais_top     = df.groupby("Country")["TotalPrice"].sum().idxmax()
    producto_top = df.groupby("Description")["TotalPrice"].sum().idxmax()

    logger.info(f"  Total ventas:      ${total_ventas:,.2f}")
    logger.info(f"  Pais top:          {pais_top}")
    logger.info(f"  Producto top:      {producto_top}")
    logger.info(f"  Registros finales: {len(df):,}")

    try:
        from src.plots import plot_ventas_por_categoria, plot_ventas_por_mes
        plot_ventas_por_categoria(df)
        plot_ventas_por_mes(df)
    except Exception as e:
        logger.warning(f"No se pudieron generar figuras: {e}")

    logger.success("PASO 4 completado.")


if __name__ == "__main__":
    args = parse_args()
    run(mode=args.mode)
