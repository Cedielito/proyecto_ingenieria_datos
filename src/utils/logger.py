# src/utils/logger.py
"""
Logger centralizado. Usa loguru si está disponible, si no usa logging estándar.
Esto permite que el proyecto funcione en cualquier entorno.
"""
try:
    from loguru import logger  # type: ignore
    USING_LOGURU = True
except ImportError:
    import logging
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )

    class _LoguruCompat:
        """Wrapper que imita la interfaz de loguru sobre el logging estándar."""
        def __init__(self):
            self._log = logging.getLogger("pipeline")

        def info(self, msg):    self._log.info(msg)
        def debug(self, msg):   self._log.debug(msg)
        def warning(self, msg): self._log.warning(msg)
        def error(self, msg):   self._log.error(msg)
        def success(self, msg): self._log.info(f"✅ {msg}")
        def remove(self):       pass
        def add(self, *a, **kw): pass

    logger = _LoguruCompat()
    USING_LOGURU = False

__all__ = ["logger"]
