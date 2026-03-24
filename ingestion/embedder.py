import boto3
import json
from logger import get_logger

from config import EMBED_MODEL

from config import AWS_REGION

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

logger = get_logger("embedder")


def embed(text):

    logger.info("Calling Bedrock embedding model")

    body = json.dumps({"inputText": text})

    response = bedrock.invoke_model(modelId=EMBED_MODEL, body=body)

    data = json.loads(response["body"].read())

    vec = data["embedding"]

    logger.info(f"Embedding received (size={len(vec)})")

    return vec


# OLLAMA_URL = "http://localhost:11434/api/embeddings"
# MODEL = "nomic-embed-text"

# def embed(text):
#
#     logger.info("Calling Ollama embedding model")
#
#     payload = {
#         "model": MODEL,
#         "prompt": text
#     }
#
#     response = requests.post(OLLAMA_URL, json=payload)
#
#     if response.status_code != 200:
#         raise Exception(f"Ollama error: {response.text}")
#
#     data = response.json()
#
#     if "embedding" not in data:
#         raise Exception(f"Invalid embedding response: {data}")
#
#     embedding = data["embedding"]
#
#     logger.info(f"Embedding received (size={len(embedding)})")
#
#     return embedding

