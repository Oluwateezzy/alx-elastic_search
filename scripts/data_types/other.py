from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="other_index", ignore_unavailable=True)
es.indices.create(
    index="other_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={
        "properties": {
            "book_reference": {"type": "keyword"},
            "price": {"type": "float"},
            "published_date": {"type": "date", "format": "yyyy-MM-dd"},
            "is_available": {"type": "boolean"},
        }
    },
)

doc = {
    "book_reference": "ISBN:978-3-16-148410-0",
    "price": 29.99,
    "published_date": "2023-10-01",
    "is_available": True,
}

response = es.index(index="other_index", body=doc)

print(response)
