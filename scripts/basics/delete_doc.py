import json
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

# def create_index(index_name):
es.indices.delete(index="test-index", ignore_unavailable=True)
es.indices.create(
    index="test-index",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
)

dummy_data = json.load(open("./dummy_data.json"))


def insert_docs(doc):
    response = es.index(index="test_index", body=doc)
    print(response)
    return response


def print_info(response):
    print(f"Index: {response['_index']}")
    print(f"ID: {response['_id']}")
    print(f"Version: {response['_version']}")
    print(f"Result: {response['result']}")


document_ids = []
for doc in dummy_data:
    response = insert_docs(doc)
    document_ids.append(response["_id"])
    print_info(response)

res = es.delete(index="test_index", id=document_ids[0])
(
    print(f"Deleted document with ID: {document_ids[0]} - Result: {res['result']}")
    if res["result"]
    else print("Document not found for deletion.")
)
print(res)
