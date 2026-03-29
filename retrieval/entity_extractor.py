import json
import logging

from llm.bedrock_client import generate_answer

logger = logging.getLogger("entities")


def extract_entities(query):
    prompt = f"""
Extrae TODAS las entidades relevantes de la consulta.

Incluye:
- conceptos legales (contrato, regulación, factura, etc.)
- tipos de documentos (adenda, propuesta, cotización, etc.)
- nombres de empresas
- productos o tecnologías
- temas clave (anticorrupción, licencias, etc.)

Devuelve SOLO un arreglo JSON de strings.

Ejemplo:
["Contrato","BanBif","Delphi","Cotización","Anticorrupción"]

Consulta:
{query}
"""

    try:
        response = generate_answer([], prompt)

        text = response.strip()

        # intento directo
        try:
            return json.loads(text)

        except Exception:
            # fallback: extraer JSON dentro del texto
            try:
                start = text.index("[")
                end = text.rindex("]") + 1
                return json.loads(text[start:end])
            except Exception:
                logger.warning(f"Could not parse entities: {text}")
                return []

    except Exception as e:
        logger.error(f"Entity extraction failed: {e}")
        return []
