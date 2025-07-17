from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="geo_shape_index", ignore_unavailable=True)

es.indices.create(
    index="gegeo_shape_indexo_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={
        "properties": {
            "location": {
                "type": "geo_shape",
            }
        }
    },
)

doc1 = {
    "location": {
        "type": "Polygon",
        "coordinates": [
            [
                [-73.856077, 40.848447],
                [-73.856077, 40.748447],
                [-73.756077, 40.748447],
                [-73.756077, 40.848447],
                [-73.856077, 40.848447],
            ],
            [
                [-73.756077, 40.848447],
                [-73.856077, 40.848447],
                [-73.856077, 40.848447],
                [-73.756077, 40.848447],
                [-73.756077, 40.848447],
            ],
        ],
    }
}

doc2 = {
    "location": {
        "type": "LineString",
        "coordinates": [
            [-73.856077, 40.848447],
            [-73.856077, 40.748447],
            [-73.756077, 40.748447],
            [-73.756077, 40.848447],
        ],
    }
}

response = es.index(index="object_index", body=doc1)
response2 = es.index(index="object_index", body=doc2)

print(response)
print(response2)
