import json
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

# def create_index(index_name):
es.indices.delete(index="test_index_1", ignore_unavailable=True)
es.indices.create(
    index="test_index_1",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
)


dummy_data = json.load(open("./dummy_data_2.json"))
for _ in range(10):
    dummy_data += dummy_data

operations = []
for document in dummy_data:
    operations.append({"index": {"_index": "test_index_1"}})
    operations.append(document)

print(len(dummy_data))

res = es.bulk(operations=operations)

es.indices.refresh(index="test_index_1")

# size and from
res = es.search(
    index="test_index_1",
    body={"query": {"match_all": {}}, "size": 10, "from": 10},
)
print(res["hits"]["hits"])

# timeout
res = es.search(
    index="test_index_1",
    body={"query": {"match": {"message": "search keyword"}}, "timeout": "10s"},
)
print(res["hits"]["hits"])

# combining all
res = es.search(
    index="test_index_1",
    body={
        "query": {"match": {"message": "search keyword"}},
        "aggs": {"max_price": {"max": {"field": "price"}}},
        "size": 10,
        "from": 10,
        "timeout": "10s",
    },
)
print(res)
