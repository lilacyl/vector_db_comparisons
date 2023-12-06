import numpy as np
import os
import re

class Loader:
    def __init__(self) -> None:
        self.embeddings_path = "../data/sim_sentences"
    def sort_key(self, filename):
            numbers = re.findall(r'\d+', filename)
            return int(numbers[0]) if numbers else -1
        

    def load_embeddings(self):
        loaded_embeddings = []
        embedding_files = sorted(os.listdir(self.embeddings_path), key=self.sort_key)
        for file_name in embedding_files:
            if file_name.startswith('embeddings_') and file_name.endswith('.npy'):
                file_path = os.path.join(self.embeddings_path, file_name)
                embeddings = np.load(file_path)
                loaded_embeddings.append(embeddings)

        sentence_embeddings = np.vstack(loaded_embeddings)
        return sentence_embeddings

loader = Loader()
embedding = loader.load_embeddings()
print(embedding.shape)
