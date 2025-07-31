import json
from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="my_index", ignore_unavailable=True)
es.indices.create(
    index="my_index",
)

operations = []

documents = json.load(open("./clothes.json"))

for doc in documents:
    operations.append({"index": {"_index": "my_index"}})
    operations.append(doc)
res = es.bulk(operations=operations)

es.indices.refresh(index="my_index")

res = es.count(index="my_index")
print(res)

res = es.search(
    index="my_index",
    body={
        "query": {
            "bool": {
                "filter": [
                    {"term": {"brand": "adidas"}},
                    {"term": {"color": "yellow"}},
                ],
            },
        },
        "size": 100,
    },
)

res = es.search(
    index="my_index",
    body={
        "query": {"bool": {"filter": {"term": {"brand": "gucci"}}}},
        "aggs": {
            "colors": {"terms": {"field": "color.keyword"}},
            "color_red": {
                "filter": {"term": {"color.keyword": "red"}},
                "aggs": {"models": {"terms": {"field": "model.keyword"}}},
            },
        },
        "post_filter": {"term": {"color": "red"}},
        "size": 20,
    },
)

print(res)

colors_aggregation = res.body["aggregations"]["colors"]["buckets"]
print(colors_aggregation)

color_red_aggregation = res.body["aggregations"]["color_red"]["models"]["buckets"]
print(color_red_aggregation)
