import json
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

# def create_index(index_name):
es.indices.delete(index="test_index", ignore_unavailable=True)
es.indices.create(
    index="test_index",
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

res = es.update(
    index="test_index",
    id=document_ids[0],
    script={
        "source": "ctx._source.title = params.title",
        "params": {"title": "Updated Title"},
    },
)

print(f"Updated document with ID: {document_ids[0]} - Result: {res['result']}")

res_0 = es.update(
    index="test_index",
    id=document_ids[0],
    script={
        "source": "ctx._source.new_field = params.new_field",
        "params": {"new_field": "dummy_value"},
    },
)

print(
    f"Added new field to document with ID: {document_ids[0]} - Result: {res_0['result']}"
)

get_res_0 = es.get(index="test_index", id=document_ids[0])
print(get_res_0)

res_1 = es.update(
    index="test_index",
    id=document_ids[0],
    script={
        "source": "ctx._source.remove('new_field')",
    },
)

print(
    f"Removed field from document with ID: {document_ids[0]} - Result: {res_1['result']}"
)

get_res_0 = es.get(index="test_index", id=document_ids[0])
print(get_res_0)
