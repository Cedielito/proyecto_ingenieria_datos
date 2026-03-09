# Pipeline ETL - Online Retail II

Pipeline ETL modular para análisis de ventas con +1 millón de registros.

---

## Arquitectura General del Pipeline
```mermaid
flowchart TD
    A[🗂️ data/raw/\nonline_retail_II.csv\n1.067.371 filas] --> B

    subgraph PASO1 [PASO 1 - INGESTA]
        B[load_data.py\nsrc/ingestion/]
    end

    B --> C[🗂️ data/interim/\nretail_interim.csv\n1.067.371 filas]
    C --> D

    subgraph PASO2 [PASO 2 - LIMPIEZA]
        D[clean_data.py\nsrc/preprocessing/]
        D --> D1[remove_nulls\n-243.007 filas]
        D --> D2[remove_invalid_quantities\n-18.744 filas]
        D --> D3[remove_invalid_prices\n-71 filas]
        D --> D4[normalize_dates]
        D --> D5[normalize_text]
    end

    D --> E[🗂️ data/interim/\nretail_clean.csv\n805.549 filas]
    E --> F

    subgraph PASO3 [PASO 3 - FEATURES]
        F[build_features.py\nsrc/features/]
        F --> F1[TotalPrice\nQuantity x Price]
        F --> F2[Year / Month\nDayOfWeek]
        F --> F3[PriceSegment\nEconomico/Medio/Premium]
    end

    F --> G[🗂️ data/processed/\ntabla_final.csv\n805.549 filas - 13 columnas]
    G --> H

    subgraph PASO4 [PASO 4 - REPORTE]
        H[main.py\nsrc/pipeline/]
        H --> H1[📊 ventas_por_pais.png]
        H --> H2[📈 ventas_por_mes.png]
        H --> H3[📋 Estadísticas consola]
    end
```

---

## Estructura del Proyecto
```mermaid
flowchart LR
    ROOT[proyecto_ingenieria_datos/]

    ROOT --> DATA[data/]
    DATA --> RAW[raw/ ← datos originales]
    DATA --> INTERIM[interim/ ← transformaciones]
    DATA --> PROCESSED[processed/ ← tabla_final.csv]

    ROOT --> SRC[src/ ← código fuente]
    SRC --> ING[ingestion/\nload_data.py]
    SRC --> PRE[preprocessing/\nclean_data.py]
    SRC --> FEA[features/\nbuild_features.py]
    SRC --> PIP[pipeline/\nmain.py ⭐]
    SRC --> UTL[utils/\nlogger.py]

    ROOT --> TST[tests/\npytest ✅]
    ROOT --> RPT[reports/\nfigures/]
```

---

## Flujo de Datos - ETL
```mermaid
flowchart LR
    E[EXTRACT\nload_data.py\nLee CSV crudo] -->|1.067.371 filas| T
    T[TRANSFORM\nclean_data.py\nbuild_features.py\nLimpia y enriquece] -->|805.549 filas| L
    L[LOAD\ndataset.py\nGuarda tabla_final.csv]
```

---

## Calidad de Datos
```mermaid
flowchart LR
    A[1.067.371 filas\ncrudas] -->|remove_nulls\n-243.007| B
    B[824.364 filas] -->|remove_invalid_quantities\n-18.744| C
    C[805.620 filas] -->|remove_invalid_prices\n-71| D
    D[✅ 805.549 filas\nlimpias]
```

---

## Módulos y Responsabilidades
```mermaid
flowchart TD
    MAIN[src/pipeline/main.py\nORQUESTADOR\nargparse --mode]

    MAIN -->|mode=ingest| ING[src/ingestion/\nload_data.py\nLee CSV → interim/]
    MAIN -->|mode=clean| PRE[src/preprocessing/\nclean_data.py\nElimina nulos y errores]
    MAIN -->|mode=features| FEA[src/features/\nbuild_features.py\nCrea TotalPrice, Year, PriceSegment]
    MAIN -->|mode=report| RPT[src/plots.py\nGenera figuras PNG]

    ING --> CFG[src/config.py\nRutas centralizadas]
    PRE --> CFG
    FEA --> CFG
    RPT --> CFG

    CFG --> DS[src/dataset.py\nread/write DataFrames]
    CFG --> LOG[src/utils/logger.py\nLogs en consola]
```

---

## Comandos de Ejecución
```bash
# Pipeline completo
python src/pipeline/main.py --mode full

# Pasos individuales
python src/pipeline/main.py --mode ingest
python src/pipeline/main.py --mode clean
python src/pipeline/main.py --mode features
python src/pipeline/main.py --mode report

# Tests
pytest tests/ -v

# Ver estructura
tree -a --dirsfirst -I '__pycache__|.ipynb_checkpoints|venv|*.egg-info'
```

---

## Resultados del Pipeline

| Métrica | Valor |
|---|---|
| Filas cargadas | 1.067.371 |
| Filas después de limpieza | 805.549 |
| Columnas finales | 13 |
| Total ventas | $17.743.429,18 |
| País top | United Kingdom |
| Producto top | Regency Cakestand 3 Tier |

---
