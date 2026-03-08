# tests/test_pipeline.py
"""Prueba de integración: valida que el pipeline completo genera tabla_final.csv."""
import pytest
from pathlib import Path


def test_processed_file_exists():
    """
    Verifica que data/processed/tabla_final.csv existe después del pipeline.
    Ejecutar DESPUÉS de: python src/pipeline/main.py --mode full
    """
    from src.config import PROCESSED_FILE
    assert PROCESSED_FILE.exists(), (
        "tabla_final.csv no encontrada. Ejecuta primero:\n"
        "  python src/pipeline/main.py --mode full"
    )


def test_processed_file_has_rows():
    """El archivo procesado debe tener al menos 1 fila de datos."""
    from src.config import PROCESSED_FILE
    from src.dataset import load_processed_dataframe

    if not PROCESSED_FILE.exists():
        pytest.skip("Ejecuta el pipeline primero: python src/pipeline/main.py --mode full")

    df = load_processed_dataframe(PROCESSED_FILE)
    assert len(df) > 0, "El archivo procesado está vacío."


def test_processed_file_has_required_columns():
    """El archivo procesado debe tener las columnas esperadas."""
    from src.config import PROCESSED_FILE
    from src.dataset import load_processed_dataframe

    if not PROCESSED_FILE.exists():
        pytest.skip("Ejecuta el pipeline primero: python src/pipeline/main.py --mode full")

    df = load_processed_dataframe(PROCESSED_FILE)
    required = ["producto", "categoria", "cantidad", "precio_unitario",
                "total_venta", "segmento_precio", "anio", "mes"]
    for col in required:
        assert col in df.columns, f"Columna requerida faltante: {col}"


def test_no_negative_quantities_in_processed():
    """No deben existir cantidades negativas en el archivo final."""
    from src.config import PROCESSED_FILE
    from src.dataset import load_processed_dataframe

    if not PROCESSED_FILE.exists():
        pytest.skip("Ejecuta el pipeline primero")

    df = load_processed_dataframe(PROCESSED_FILE)
    assert (df["cantidad"] > 0).all(), "Hay cantidades negativas o cero en el archivo final."
