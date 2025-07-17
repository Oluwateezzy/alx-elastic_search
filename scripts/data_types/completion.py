from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="completion_index", ignore_unavailable=True)

es.indices.create(
    index="completion_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={
        "properties": {
            "suggest": {
                "type": "completion",
            }
        }
    },
)

doc1 = {"suggest": {"input": ["apple", "banana", "cherry"]}}
doc2 = {"suggest": {"input": ["date", "elderberry", "fig"]}}


response = es.index(index="object_index", body=doc1)
response2 = es.index(index="object_index", body=doc2)

print(response)
print(response2)
