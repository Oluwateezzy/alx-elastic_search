from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="object_index", ignore_unavailable=True)

es.indices.create(
    index="object_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={
        "properties": {
            "author": {
                "properties": {
                    "last_name": {"type": "text"},
                    "first_name": {"type": "text"},
                }
            }
        }
    },
)

doc = {"author": {"last_name": "Doe", "first_name": "John"}}

response = es.index(index="object_index", body=doc)

print(response)
