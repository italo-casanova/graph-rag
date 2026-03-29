import boto3
import json
from logger import get_logger
from config import EMBED_MODEL, AWS_REGION

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
logger = get_logger("embedder")


def embed(text):
    """
    Genera embedding usando Amazon Titan Text Embeddings V2.
    Titan v2 es multilingüe y soporta español de forma nativa,
    a diferencia de v1 que estaba optimizado para inglés.
    Dimensión de salida: 1024 (actualizar vector(768) → vector(1024) en SQL)
    """
    logger.info("Calling Bedrock embedding model (Titan v2 multilingual)")
    # Titan v2 acepta 'inputText' igual que v1
    body = json.dumps(
        {
            "inputText": text,
            "dimensions": 1024,  # 256 | 512 | 1024  (mayor = más preciso)
            "normalize": True,  # normalizar para cosine similarity
        }
    )
    response = bedrock.invoke_model(modelId=EMBED_MODEL, body=body)
    data = json.loads(response["body"].read())
    vec = data["embedding"]
    logger.info(f"Embedding received (size={len(vec)})")
    return vec
