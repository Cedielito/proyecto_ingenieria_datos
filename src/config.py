# src/config.py
"""
Configuración central del proyecto.
Gestiona rutas con pathlib y carga variables de entorno desde .env
"""
from pathlib import Path
from dotenv import load_dotenv
import os

# ── Rutas base ──────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"

MODELS_DIR = ROOT_DIR / "models"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# ── Cargar .env ──────────────────────────────────────────────────────────────
load_dotenv(ROOT_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ── Archivos del pipeline ────────────────────────────────────────────────────
RAW_FILE = RAW_DIR / "online_retail_II.csv"
INTERIM_FILE = INTERIM_DIR / "retail_interim.csv"
PROCESSED_FILE = PROCESSED_DIR / "tabla_final.csv"


def verify_structure() -> None:
    """Verifica que todas las carpetas necesarias existan."""
    dirs = [RAW_DIR, INTERIM_DIR, PROCESSED_DIR, EXTERNAL_DIR,
            MODELS_DIR, FIGURES_DIR]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
