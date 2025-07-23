import json
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

# def create_index(index_name):
es.indices.delete(index="test_index_1", ignore_unavailable=True)
es.indices.create(
    index="test_index_1",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
)

es.indices.delete(index="test_index_2", ignore_unavailable=True)
es.indices.create(
    index="test_index_2",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
)

dummy_data = json.load(open("./dummy_data.json"))


def insert_docs(doc, index="test_index_1"):
    response = es.index(index=index, body=doc)
    print(response)
    return response


def print_info(response):
    print(f"Index: {response['_index']}")
    print(f"ID: {response['_id']}")
    print(f"Version: {response['_version']}")
    print(f"Result: {response['result']}")


document_ids = []
for doc in dummy_data:
    response = insert_docs(doc, "test_index_1")
    response_2 = insert_docs(doc, "test_index_2")
    document_ids.append(response["_id"])
    document_ids.append(response_2["_id"])

# refresh the indices to ensure all documents are indexed
es.indices.refresh(index="test_index_1")
es.indices.refresh(index="test_index_2")

# term query
res = es.search(
    index="test_index_1", body={"query": {"term": {"created_on": "2024-09-22"}}}
)

print(res["hits"]["total"]["value"])

# match query
res = es.search(index="test_index_1", body={"query": {"match": {"text": "document"}}})

print(res["hits"]["total"]["value"])

# range query
res = es.search(
    index="test_index_1",
    body={"query": {"range": {"created_on": {"lte": "2024-09-22"}}}},
)

print(res["hits"]["total"]["value"])

# compound clauses
res = es.search(
    index="test_index_1",
    body={
        "query": {
            "bool": {
                "must": [
                    {"match": {"text": "third"}},
                    {
                        "range": {
                            "created_on": {"lte": "2024-09-24", "gte": "2024-09-24"}
                        }
                    },
                ]
            }
        }
    },
)
print(res["hits"]["total"]["value"])
