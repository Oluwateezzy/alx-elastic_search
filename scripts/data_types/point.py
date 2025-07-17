from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="point_index", ignore_unavailable=True)

es.indices.create(
    index="point_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={"properties": {"location": {"type": "point"}}},
)

doc = {
    "location": {
        "type": "Point",
        "coordinates": [
            -73.856077,
            40.848447,
        ],
    },
}

response = es.index(index="object_index", body=doc)

print(response)
