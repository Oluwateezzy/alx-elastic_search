import json
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

# def create_index(index_name):
es.indices.delete(index="test_index_1", ignore_unavailable=True)
es.indices.create(
    index="test_index_1",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    mappings={
        "properties": {
            "sides_length": {"type": "dense_vector", "dims": 4},
            "shape": {"type": "keyword"},
        },
    },
)

res = es.index(
    index="test_index_1", id=1, document={"shape": "rect", "sides_length": [5, 5, 5, 5]}
)
print(res.body)
