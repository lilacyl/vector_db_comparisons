import weaviate
import requests
import json
import private

auth_config = weaviate.AuthApiKey(api_key=private.WEAVIET_API_KEY)

client = weaviate.Client(
  url="https://vector-db-comparison-weaviet-3axgm0q8.weaviate.network",
  auth_client_secret=auth_config,
  additional_headers = {
        "X-OpenAI-Api-Key": private.OPEN_API_KEY  # Replace with your inference API key
    }
)


response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=4))