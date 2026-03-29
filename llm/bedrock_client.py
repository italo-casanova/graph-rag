import boto3
import json

from config import AWS_REGION, BEDROCK_MODEL

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def generate_answer(context, question):
    context_text = "\n".join(context)

    prompt = f"""
Eres un asistente legal.

Usa el contexto proporcionado para responder la pregunta.

Reglas:
- Responde basándote únicamente en el contexto.
- Puedes resumir, reorganizar y explicar la información.
- NO inventes información que no esté en el contexto.
- Si el contexto no es suficiente, indica claramente qué falta.
- Incluye fragmentos textuales del contexto como evidencia cuando sea posible.

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
