from datetime import datetime, timedelta
import random
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

index_name = "my_index"
mappings = {
    "mappings": {
        "properties": {
            "timestamp": {"type": "date"},
            "value": {"type": "float"},
            "category": {"type": "keyword"},
            "description": {"type": "text"},
            "id": {"type": "keyword"},
        }
    },
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
}

es.indices.delete(index=index_name, ignore_unavailable=True)
es.indices.create(index=index_name, body=mappings)

base_documents = [
    {"category": "A", "value": 100, "description": "First sample document"},
    {"category": "B", "value": 200, "description": "Second sample document"},
    {"category": "C", "value": 300, "description": "Third sample document"},
    {"category": "D", "value": 400, "description": "Fourth sample document"},
    {"category": "E", "value": 500, "description": "Fifth sample document"},
]


def generate_bulk_data(base_documents, target_size=100_000):
    documents = []
    base_count = len(base_documents)
    duplications_needed = target_size // base_count

    base_timestamp = datetime.now()

    for i in range(duplications_needed):
        for document in base_documents:
            new_doc = document.copy()
            new_doc["id"] = f"doc_{len(documents)}"
            new_doc["timestamp"] = (
                base_timestamp - timedelta(minutes=len(documents))
            ).isoformat()
            new_doc["value"] = document["value"] + random.uniform(-10, 10)
            documents.append(new_doc)

    return documents


documents = generate_bulk_data(base_documents, target_size=100_000)
print(f"Generated {len(documents)} documents")

operations = []
for document in documents:
    operations.append({"index": {"_index": index_name}})
    operations.append(document)


response = es.bulk(operations=operations)
print(response.body["errors"])


es.indices.refresh(index=index_name)

count = es.count(index=index_name)["count"]
print(f"Indexed {count} documents")

# From / Size method
# To use the from/size method, include two parameters in your query: from, which specifies the number of documents to skip, and size, which tells Elasticsearch how many documents to return.
response = es.search(
    index=index_name,
    body={"from": 10, "size": 10, "sort": [{"timestamp": "desc"}, {"id": "desc"}]},
)

hits = response["hits"]["hits"]
for hit in hits:
    print(f"ID: {hit['_source']['id']}")
