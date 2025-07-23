import json
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

# def create_index(index_name):
es.indices.delete(index="my_index", ignore_unavailable=True)
es.indices.create(
    index="my_index",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
)

dummy_data = json.load(open("./dummy_data.json"))


def insert_docs(doc):
    response = es.index(index="my_index", body=doc)
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

es.indices.refresh(index="my_index")

query = {
    "range": {
        "created_on": {"gte": "2024-09-24", "lte": "2024-09-24", "format": "yyyy-MM-dd"}
    }
}

res = es.count(index="my_index", query=query)
print(res)
