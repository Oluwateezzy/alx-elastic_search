import json
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

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


for doc in dummy_data:
    response = insert_docs(doc)
    print_info(response)
