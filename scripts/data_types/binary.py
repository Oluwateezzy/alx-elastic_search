import base64
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

es.indices.delete(index="binary_index", ignore_unavailable=True)

es.indices.create(
    index="binary_index",
    settings={"index": {"number_of_shards": 2, "number_of_replicas": 3}},
    mappings={"properties": {"image_data": {"type": "binary"}}},
)

image_path = "./img.jpeg"

with open(image_path, "rb") as file:
    image_byte = file.read()
    image_base64 = base64.b64encode(image_byte).decode("utf-8")
print(image_base64[:100])

response = es.index(index="binary_index", body={"image_data": image_base64})

print(response)
