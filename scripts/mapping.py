from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

map = es.indices.get_mapping(index="test-index")
print(map)
