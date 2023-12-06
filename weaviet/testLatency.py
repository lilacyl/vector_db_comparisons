import numpy as np
import weaviate
import private
import addEmbeddings
import loadEmbeddings
import querySingleEmbedding
from tqdm import tqdm
import time

CUR_TEST_CASE_SIZE = 3000

sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000]
loader = loadEmbeddings.Loader()
your_embeddings = loader.load_embeddings()


def generate_test_cases(embeddings, sizes):
    np.random.seed(42)
    test_cases = {}
    for size in sizes:
        # Randomly select 'size' number of embeddings from the sentence_embeddings
        indices = np.random.choice(len(embeddings), size, replace=False)
        test_cases[size] = embeddings[indices]
    return test_cases


def tests_runtime(embeddings, client, numTestCases=10000):
    runtimes = np.zeros(numTestCases)
    np.random.seed(42)
    indices = np.random.choice(len(embeddings), numTestCases, replace=True)
    tests = embeddings[indices]
    for i in tqdm(range(len(tests))):
        runtimes[i] = querySingleEmbedding.query_embedding_runtime(tests[i], client=client)
    return runtimes

# Connect to Weaviate
auth_config = weaviate.AuthApiKey(api_key=private.WEAVIET_API_KEY)

client = weaviate.Client(
  url=private.WEAVIET_API_LINK,
  auth_client_secret=auth_config,
  additional_headers = {
        "X-OpenAI-Api-Key": private.OPEN_API_KEY  # Replace with your inference API key
    }
)

test_cases = generate_test_cases(your_embeddings, sizes)
prev_test_case = np.concatenate((test_cases[1000], test_cases[2000]), axis=0)

CUR_TEST_CASE_SIZE = 5000
while (CUR_TEST_CASE_SIZE <= 14000): 
    print("==================================================")
    print(f'- currently running CUR_TEST_CASE_SIZE={CUR_TEST_CASE_SIZE}')
    print("- clearing old data")
    client.schema.delete_class("EmbeddingsClass")

    cur_embeddings = test_cases[CUR_TEST_CASE_SIZE]
    addEmbeddings.add_embeddings(cur_embeddings, client)
    print("- new embeddings uploaded, now testing rumtime")

    runtime_result = tests_runtime(cur_embeddings, client=client)
    np.savetxt(f'rumtime_size{CUR_TEST_CASE_SIZE}.txt', runtime_result)
    print("- results saved")

    # make it sleep so weaviet can reset its memory
    time.sleep(8 * 60)
    CUR_TEST_CASE_SIZE+= 1000