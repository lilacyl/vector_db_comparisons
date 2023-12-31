import weaviate
import requests
import json
import private

auth_config = weaviate.AuthApiKey(api_key=private.WEAVIET_API_KEY)

client = weaviate.Client(
  url="https://vectordb-project-weaviet-3knitmrj.weaviate.network",
  auth_client_secret=auth_config,
  additional_headers = {
        "X-OpenAI-Api-Key": private.OPEN_API_KEY  # Replace with your inference API key
    }
)

response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_limit(2)
    .do()
)


print(json.dumps(response, indent=4))