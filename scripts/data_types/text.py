from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="text_index", ignore_unavailable=True)

es.indices.create(
    index="text_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={
        "properties": {
            "email_body": {
                "type": "text",
            }
        }
    },
)

doc = {"email_body": "This is a sample email body text for testing purposes."}

response = es.index(index="text_index", body=doc)

print(response)
