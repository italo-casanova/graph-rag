import boto3
import json

from config import AWS_REGION, BEDROCK_MODEL

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def generate_answer(context, question):

    context_text = "\n".join(context)

    prompt = f"""
You are a legal assistant.

Use the context to answer the question.

Context:
{context_text}

Question:
{question}

Answer:
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

