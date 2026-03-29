import json
import logging
import unicodedata

from llm.bedrock_client import generate_answer

logger = logging.getLogger("entities")

VALID_CONCEPTS = ["Contract", "Proposal", "Regulation", "Invoice", "Document"]


def normalize(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.strip()


def extract_entities(query):
    """
    Devuelve:
    {
        "concepts": ["Contract", "Proposal"],
        "keywords": ["banbif", "anticorrupcion"]
    }
    """

    concepts_list = ", ".join(VALID_CONCEPTS)

    prompt = f"""
Eres un sistema de extracción de información legal.

Tu tarea es analizar la consulta y devolver DOS cosas:

1. "concepts": tipos de documentos del grafo
2. "keywords": términos importantes para búsqueda semántica

Conceptos válidos (usa SOLO estos):
{concepts_list}

Reglas:
- "concepts" SOLO puede contener valores de la lista
- "keywords" debe incluir empresas, temas, productos
- Normaliza todo a minúsculas
- No inventes conceptos fuera de la lista

Devuelve SOLO JSON con esta estructura:

{{
  "concepts": [...],
  "keywords": [...]
}}

Ejemplo:

Consulta:
"¿Qué dice la adenda anticorrupción firmada con BanBif?"

Respuesta:
{{
  "concepts": ["Contract"],
  "keywords": ["banbif", "anticorrupcion", "adenda"]
}}

Consulta:
{query}

Respuesta:
"""

    try:
        response = generate_answer([], prompt)
        text = response.strip()

        try:
            data = json.loads(text)
        except Exception:
            start = text.find("{")
            end = text.rfind("}") + 1
            data = json.loads(text[start:end])

        # --- validar concepts ---
        concepts = [c for c in data.get("concepts", []) if c in VALID_CONCEPTS]

        # fallback inteligente
        if not concepts:
            concepts = ["Contract", "Proposal"]

        # --- normalizar keywords ---
        keywords = [
            normalize(k)
            for k in data.get("keywords", [])
            if isinstance(k, str) and len(k) > 2
        ]

        logger.info(f"Concepts: {concepts}")
        logger.info(f"Keywords: {keywords}")

        return {"concepts": concepts, "keywords": keywords}

    except Exception as e:
        logger.error(f"Entity extraction failed: {e}")

        return {"concepts": ["Contract", "Proposal"], "keywords": []}
