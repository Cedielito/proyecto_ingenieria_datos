# tests/test_features.py
"""Pruebas unitarias para el módulo de features."""
import pandas as pd
import pytest

from src.features.build_features import (
    add_total_venta,
    add_temporal_features,
    add_segmento_precio,
)


@pytest.fixture
def df_clean():
    """DataFrame limpio para pruebas de features."""
    return pd.DataFrame({
        "fecha": pd.to_datetime(["2024-01-01", "2024-02-15", "2024-03-22"]),
        "producto": ["Laptop Pro", "Mouse", "Silla"],
        "categoria": ["Tecnología", "Tecnología", "Mobiliario"],
        "cantidad": [2, 5, 1],
        "precio_unitario": [1200.0, 25.50, 350.0],
        "region": ["Norte", "Sur", "Centro"],
    })


def test_add_total_venta(df_clean):
    """total_venta = cantidad * precio_unitario."""
    result = add_total_venta(df_clean)
    assert "total_venta" in result.columns
    assert result.loc[0, "total_venta"] == pytest.approx(2400.0)
    assert result.loc[1, "total_venta"] == pytest.approx(127.50)


def test_add_temporal_features(df_clean):
    """Deben existir columnas anio, mes y dia_semana."""
    result = add_temporal_features(df_clean)
    assert "anio" in result.columns
    assert "mes" in result.columns
    assert "dia_semana" in result.columns
    assert result.loc[0, "anio"] == 2024
    assert result.loc[0, "mes"] == 1


def test_add_segmento_precio_economico(df_clean):
    """Precio < 100 → Económico."""
    result = add_segmento_precio(df_clean)
    assert result.loc[1, "segmento_precio"] == "Económico"


def test_add_segmento_precio_premium(df_clean):
    """Precio >= 500 → Premium."""
    result = add_segmento_precio(df_clean)
    assert result.loc[0, "segmento_precio"] == "Premium"


def test_add_segmento_precio_medio(df_clean):
    """Precio 100-499 → Medio."""
    result = add_segmento_precio(df_clean)
    assert result.loc[2, "segmento_precio"] == "Medio"
