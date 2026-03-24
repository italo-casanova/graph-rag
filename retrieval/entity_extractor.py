import json
import logging

from llm.bedrock_client import generate_answer

logger = logging.getLogger("entities")


def extract_entities(query):

    prompt = f"""
Extract the main legal concepts from the following query.

Return ONLY a JSON array.

Example:
["Contract","Proposal"]

Query:
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

