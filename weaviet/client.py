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

print(f"=====Connect to Weaviate=====")
class_obj = {
    "class": "JeopardyQuestion",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "vectorizeClassName": True
        },
        "generative-openai": {} 
    }
}

# client.schema.create_class(class_obj)
print("=====Created Class Obj=====")

resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
data = json.loads(resp.text)  # Load data

client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:  # Initialize a batch process
    for i, d in enumerate(data):  # Batch import data
        print(f"importing question: {i+1}")
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }
        batch.add_data_object(
            data_object=properties,
            class_name="Question"
        )
print("=====Added Embeddings=====")
json_data = client.schema.get()
print(json.dumps(json_data, indent=2))