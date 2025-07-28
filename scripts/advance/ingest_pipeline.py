import json
from typing import Any
from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

res: ObjectApiResponse[Any] = es.ingest.put_pipeline(
    id="lowercase_pipeline",
    description="This pipeline transforms the text to lowercase",
    processors=[
        {
            "lowercase": {
                "field": "text",
            }
        }
    ],
)
print(res)

res = es.ingest.get_pipeline(id="lowercase_pipeline")
print(res)

res = es.ingest.put_pipeline(
    id="lowercase_pipeline",
    description="This pipeline transforms the text to lowercase",
    processors=[{"lowercase": {"field": "text"}}],
)

res = es.ingest.simulate(
    id="lowercase_pipeline",
    docs=[{"_index": "my_index", "_id": "1", "_source": {"text": "HELLO WORLD"}}],
)
print(res.body)

dummy_data = json.load(open("../basics/dummy_data.json"))
for i, document in enumerate(dummy_data):
    uppercased_text = document["text"].upper()
    document["text"] = uppercased_text
    dummy_data[i] = document

print(dummy_data)

es.indices.delete(index="my_index", ignore_unavailable=True)
es.indices.create(index="my_index")

operations = []
for document in dummy_data:
    operations.append({"index": {"_index": "my_index"}})
    operations.append(document)

res = es.bulk(operations=operations, pipeline="lowercase_pipeline")
print(res)

es.indices.refresh(index="my_index")

res = es.search(index="my_index")
hits = res.body["hits"]["hits"]

for hit in hits:
    print(hit["_source"])

res = es.ingest.delete_pipeline(id="lowercase_pipeline")
print(res)
