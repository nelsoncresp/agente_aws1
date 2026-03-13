"""Test directo de Bedrock para diagnosticar el problema"""
import json
import boto3

client = boto3.client("bedrock-runtime", region_name="us-west-2")

body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hola, dime que es AWS Lambda en una frase"}]
})

try:
    response = client.invoke_model(
        modelId="us.anthropic.claude-3-5-haiku-20241022-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json"
    )
    result = json.loads(response["body"].read())
    print("EXITO:", result["content"][0]["text"])
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
