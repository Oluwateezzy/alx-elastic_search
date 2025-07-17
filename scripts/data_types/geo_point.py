from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="geo_point_index", ignore_unavailable=True)

es.indices.create(
    index="geo_point_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={
        "properties": {
            "location": {
                "type": "geo_point",
            }
        }
    },
)

doc = {
    "text": "This is a sample document with a geo_point field.",
    "location": {
        "type": "Point",
        "coordinates": [
            -73.856077,
            40.848447,
        ],  # Example coordinates (longitude, latitude)
    },
}

response = es.index(index="object_index", body=doc)

print(response)
