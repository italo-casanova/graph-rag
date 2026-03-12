import requests
import json
import logging

logger = logging.getLogger("entities")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def extract_entities(query):

    prompt = f"""
Extract the main legal concepts from the following query.

Return ONLY a JSON array.

Example:
["Contract","Proposal"]

Query:
{query}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        logger.error(response.text)
        return []

    data = response.json()

    text = data.get("response", "").strip()

    # try parsing JSON
    try:
        return json.loads(text)
    except Exception:

        # fallback: extract JSON from text
        try:
            start = text.index("[")
            end = text.rindex("]") + 1
            return json.loads(text[start:end])
        except Exception:
            return []