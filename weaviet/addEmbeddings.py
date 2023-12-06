import weaviate
import numpy as np
import private
import loadEmbeddings
from tqdm import tqdm

# Add data to Weaviate

def add_embeddings(your_embeddings, client):
    for i in tqdm(range(len(your_embeddings))):
        embedding = your_embeddings[i]
        data_object = {
            "name":str(i),
            "embedding": embedding.tolist()  # Convert NumPy array to list
        }
        client.data_object.create(data_object, "EmbeddingsClass")
        # try:
        #     client.data_object.create(data_object, "EmbeddingsClass")
        # except JSONDecodeError as e:
        #     print(f"JSONDecodeError occurred: {e}")
        #     # Optionally, log the problematic data_object or take other actions
        #     continue  # Continue to the next item in the loop
