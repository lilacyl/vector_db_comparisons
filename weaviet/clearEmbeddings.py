import weaviate
import numpy as np
import private
import loadEmbeddings
from tqdm import tqdm

# Connect to Weaviate
auth_config = weaviate.AuthApiKey(api_key=private.WEAVIET_API_KEY)

client = weaviate.Client(
  url=private.WEAVIET_API_LINK,
  auth_client_secret=auth_config,
  additional_headers = {
        "X-OpenAI-Api-Key": private.OPEN_API_KEY  # Replace with your inference API key
    }
)

client.schema.delete_class("EmbeddingsClass")