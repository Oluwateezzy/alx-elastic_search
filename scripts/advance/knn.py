import json
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import torch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))


es.indices.delete(index="test_index_1", ignore_unavailable=True)
es.indices.create(
    index="test_index_1",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    mappings={
        "properties": {
            "embedding": {"type": "dense_vector"},
        },
    },
)

model = SentenceTransformer("all-MiniLM-L6-v2")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = model.to(device=device)

dummy_data = json.load(open("../basics/astronomy.json"))


def get_embedding(text):
    return model.encode(text)


operations = []
for doc in dummy_data:
    operations.append({"index": {"_index": "test_index_1"}})
    operations.append({**doc, "embedding": get_embedding(doc["content"])})


res = es.bulk(operations=operations)

# refresh the indices to ensure all documents are indexed
es.indices.refresh(index="test_index_1")

# KNN
query = "What is a black hole?"
embedded_query = get_embedding(query)

res = es.search(
    index="test_index_1",
    knn={
        "field": "embedding",
        "query_vector": embedded_query,
        "num_candidates": 5,
        "k": 3,
    },
)

hits = res["hits"]["hits"]
for hit in hits:
    print(f"Title: {hit['_source']['title']}")
    print(f"Content: {hit['_source']['content']}")
    print(f"Score: {hit['_score']}")
    print("*" * 100)


query = "Hpw do we find exoplanets?"
embedded_query = get_embedding(query)

res = es.search(
    index="test_index_1",
    knn={
        "field": "embedding",
        "query_vector": embedded_query,
        "num_candidates": 5,
        "k": 3,
    },
)

hits = res["hits"]["hits"]
for hit in hits:
    print(f"Title: {hit['_source']['title']}")
    print(f"Content: {hit['_source']['content']}")
    print(f"Score: {hit['_score']}")
    print("*" * 100)
