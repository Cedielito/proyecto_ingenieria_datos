.PHONY: help setup run test clean lint structure

# Mostrar ayuda
help:
	@echo ""
	@echo "============================================"
	@echo " Pipeline ETL - Comandos disponibles"
	@echo "============================================"
	@echo ""
	@echo "  make setup      → Crear venv e instalar dependencias"
	@echo "  make run        → Ejecutar pipeline completo"
	@echo "  make ingest     → Solo paso de ingesta"
	@echo "  make clean-data → Solo paso de limpieza"
	@echo "  make features   → Solo paso de features"
	@echo "  make test       → Ejecutar pruebas unitarias"
	@echo "  make lint       → Verificar estilo de código"
	@echo "  make structure  → Mostrar estructura del proyecto"
	@echo "  make clean      → Limpiar archivos generados"
	@echo ""

# Configurar entorno virtual
setup:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	@echo "✅ Entorno configurado. Activa con: source venv/bin/activate"

# Ejecutar pipeline completo
run:
	python src/pipeline/main.py --mode full

# Pasos individuales
ingest:
	python src/pipeline/main.py --mode ingest

clean-data:
	python src/pipeline/main.py --mode clean

features:
	python src/pipeline/main.py --mode features

# Tests
test:
	pytest tests/ -v

# Linting
lint:
	ruff check src/ tests/

# Mostrar estructura
structure:
	tree -a --dirsfirst -I '__pycache__|.ipynb_checkpoints|.git|venv|*.egg-info'

# Limpiar artefactos generados
clean:
	rm -f data/interim/*.csv
	rm -f data/processed/*.csv
	rm -f reports/figures/*.png
	@echo "🧹 Artefactos limpiados."
