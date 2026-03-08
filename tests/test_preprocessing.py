# tests/test_preprocessing.py
"""Pruebas unitarias para el módulo de preprocesamiento."""
import pandas as pd
import pytest

from src.preprocessing.clean_data import (
    remove_nulls,
    remove_invalid_quantities,
    normalize_dates,
    normalize_text,
)


@pytest.fixture
def df_dirty():
    """DataFrame con datos sucios para pruebas."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "fecha": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        "producto": ["Laptop Pro", None, "  mouse inalámbrico  ", "Teclado", "Monitor"],
        "categoria": ["tecnología", "tecnología", "TECNOLOGÍA", "mobiliario", "tecnología"],
        "cantidad": [2, 1, -1, 0, 3],
        "precio_unitario": [1200.0, None, 25.50, 80.0, 400.0],
        "cliente_id": ["C001", "C002", "C003", "C004", "C005"],
        "region": ["norte", "sur", "centro", "este", "oeste"],
        "vendedor": ["v01", "v02", "v01", "v03", "v02"],
    })


def test_remove_nulls_drops_rows_with_null_product(df_dirty):
    """Debe eliminar filas donde 'producto' es nulo."""
    result = remove_nulls(df_dirty)
    assert result["producto"].isnull().sum() == 0


def test_remove_nulls_drops_rows_with_null_price(df_dirty):
    """Debe eliminar filas donde 'precio_unitario' es nulo."""
    result = remove_nulls(df_dirty)
    assert result["precio_unitario"].isnull().sum() == 0


def test_remove_invalid_quantities(df_dirty):
    """Debe eliminar filas con cantidad <= 0."""
    df_clean = remove_nulls(df_dirty)
    result = remove_invalid_quantities(df_clean)
    assert (result["cantidad"] > 0).all()


def test_normalize_dates(df_dirty):
    """La columna fecha debe convertirse a datetime."""
    result = normalize_dates(df_dirty)
    assert pd.api.types.is_datetime64_any_dtype(result["fecha"])


def test_normalize_text_strips_spaces(df_dirty):
    """El texto no debe tener espacios al inicio o al final."""
    result = normalize_text(df_dirty.dropna(subset=["producto"]))
    for val in result["producto"].dropna():
        assert val == val.strip()


def test_full_pipeline_reduces_rows(df_dirty):
    """El pipeline de limpieza debe reducir el número de filas (datos malos)."""
    original = len(df_dirty)
    df = remove_nulls(df_dirty)
    df = remove_invalid_quantities(df)
    assert len(df) < original
