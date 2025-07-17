from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="nested_index", ignore_unavailable=True)

es.indices.create(
    index="nested_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={
        "properties": {
            "user": {
                "type": "nested",
            }
        }
    },
)

doc = [
    {"first_name": "John", "last_name": "Doe"},
    {"first_name": "Jane", "last_name": "Doe"},
    {"first_name": "Alice", "last_name": "Smith"},
    {"first_name": "Bob", "last_name": "Brown"},
]

response = es.index(index="object_index", body={"user": doc})

print(response)
