import boto3
import json

from config import AWS_REGION, BEDROCK_MODEL

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def generate_answer(context, question):

    context_text = "\n".join(context)

    prompt = f"""
Eres un asistente legal.

Usa el contexto proporcionado para responder a la pregunta de manera textual, tal y como esta en el documento,
No alteres la información y no inventes nada.
Si no sabes la respuesta, di que no lo sabes.

Contexto:
{context_text}

Pregunta:
{question}

Respuesta:
"""

    body = json.dumps(
        {
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            # "max_tokens": 500,
            # "temperature": 0.2,
        }
    )

    response = bedrock.invoke_model(modelId=BEDROCK_MODEL, body=body)

    data = json.loads(response["body"].read())

    return data["output"]["message"]["content"][0]["text"]
