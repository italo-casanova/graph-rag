import boto3
import json
from logger import get_logger

from config import AWS_REGION, EMBED_MODEL

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

logger = get_logger("embedder")

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def embed(text):

    logger.info("Calling Bedrock embedding model")

    body = json.dumps({"inputText": text})

    response = bedrock.invoke_model(modelId=EMBED_MODEL, body=body)

    data = json.loads(response["body"].read())

    vec = data["embedding"]

    logger.info(f"Embedding received (size={len(vec)})")

    return vec
