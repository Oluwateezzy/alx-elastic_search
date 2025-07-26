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

dummy_data = json.load(open("../basics/dummy_data.json"))


def get_embedding(text):
    return model.encode(text)


operations = []
for doc in dummy_data:
    operations.append({"index": {"_index": "test_index_1"}})
    operations.append({**doc, "embedding": get_embedding(doc["text"])})


res = es.bulk(operations=operations)

# refresh the indices to ensure all documents are indexed
es.indices.refresh(index="test_index_1")

res = es.search(index="test_index_1", body={"query": {"match_all": {}}})
