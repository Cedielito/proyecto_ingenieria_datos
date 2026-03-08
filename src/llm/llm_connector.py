# src/llm/llm_connector.py
"""
Conexión a LLMs externos (Gemini, OpenAI, etc.)
Las API keys se leen desde .env — nunca hardcodeadas.
"""
import os
from src.utils.logger import logger


def get_gemini_summary(data_summary: str) -> str:
    """
    Envía un resumen de datos a Gemini y retorna el análisis.
    Requiere GEMINI_API_KEY en .env

    Args:
        data_summary: resumen en texto del dataset procesado.

    Returns:
        Análisis generado por el LLM.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        logger.warning("GEMINI_API_KEY no configurada en .env. Retornando análisis simulado.")
        return _mock_analysis(data_summary)

    try:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
        Eres un analista de datos experto. Analiza el siguiente resumen de ventas y dame:
        1. Tres insights clave del negocio.
        2. Una recomendación accionable.
        3. Un posible riesgo en los datos.

        Resumen:
        {data_summary}
        """

        response = model.generate_content(prompt)
        logger.success("Análisis LLM completado con Gemini.")
        return response.text

    except Exception as e:
        logger.error(f"Error conectando a Gemini: {e}")
        return _mock_analysis(data_summary)


def _mock_analysis(summary: str) -> str:
    """Análisis simulado cuando no hay API key."""
    return f"""
[ANÁLISIS SIMULADO - Configura GEMINI_API_KEY en .env para análisis real]

Resumen recibido:
{summary}

Insights detectados:
1. El pipeline ETL completó exitosamente todas las transformaciones.
2. Los datos están listos para modelado o visualización.
3. Se recomienda monitorear la calidad de datos en cada ejecución.

Recomendación: Automatizar la ejecución del pipeline con GitHub Actions.
"""
