import requests
import pandas as pd
import numpy as np
from io import StringIO
from sentence_transformers import SentenceTransformer



def prepare_dataset():
    sentences = []
    urls = [
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/sick2014/SICK_train.txt',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2012/MSRpar.train.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2012/MSRpar.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2012/OnWN.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2013/OnWN.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2014/OnWN.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2014/images.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2015/images.test.tsv'
    ]
    for url in urls:
        res = requests.get(url)
        data = pd.read_csv(StringIO(res.text), sep='\t', header=None, on_bad_lines="skip")
        sentences.extend(data[1].tolist())
        sentences.extend(data[2].tolist())
    sentences = [
        sentence.replace('\n', '') for sentence in list(set(sentences)) if type(sentence) is str
    ]
    with open('sentences.txt', 'w') as fp:
        fp.write('\n'.join(sentences))
    
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    sentence_embeddings = model.encode(sentences)
    split = 256
    file_count = 0
    for i in range(0, sentence_embeddings.shape[0], split):
        end = i + split
        if end > sentence_embeddings.shape[0] + 1:
            end = sentence_embeddings.shape[0] + 1
        file_count = '0' + str(file_count) if file_count < 0 else str(file_count)
        with open(f'./sim_sentences/embeddings_{file_count}.npy', 'wb') as fp:
            np.save(fp, sentence_embeddings[i:end, :])
        print(f"embeddings_{file_count}.npy | {i} -> {end}")
        file_count = int(file_count) + 1


prepare_dataset()