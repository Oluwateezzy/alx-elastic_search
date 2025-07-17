from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

# def create_index(index_name):
es.indices.delete(index="test-index", ignore_unavailable=True)
es.indices.create(
    index="test-index",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
)
