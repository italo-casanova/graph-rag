import json
import logging
import unicodedata

from llm.bedrock_client import generate_answer

logger = logging.getLogger("entities")


def normalize(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.strip()


def extract_entities(query):

    prompt = f"""
Extrae SOLO entidades útiles para búsqueda en documentos legales.

Incluye únicamente:
- tipos de documentos (contrato, adenda, propuesta, cotización, factura)
- instituciones o empresas (banbif, r2data)
- temas clave (anticorrupcion, licencias)

NO incluyas palabras irrelevantes.

Devuelve SOLO JSON.

Ejemplo:
["contrato","adenda","banbif","cotizacion"]

Consulta:
{query}
"""

    try:
        response = generate_answer([], prompt)
        text = response.strip()

        try:
            entities = json.loads(text)
        except:
            start = text.find("[")
            end = text.rfind("]") + 1
            entities = json.loads(text[start:end])

        entities = [normalize(e) for e in entities]

        return entities

    except Exception as e:
        logger.error(f"Entity extraction failed: {e}")
        return []
