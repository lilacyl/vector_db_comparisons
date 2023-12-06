import time
import weaviate


def query_embedding_runtime(embedding, client) :
    start_time = time.time()
    try:
        _ = client.query.get("EmbeddingsClass", properties=["embedding"]).with_near_vector({
            "vector": embedding
        }).with_limit(5).do()
    except weaviate.exceptions.UnexpectedStatusCodeException as e:
         print(f"weaviet errr occurred: {e}")
    end_time = time.time()
    time.sleep(0.05)
    return end_time - start_time