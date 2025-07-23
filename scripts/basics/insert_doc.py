from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

document = {
    "title": "Sample Document",
    "text": "This is a sample document for testing purposes.",
    "created_at": "2023-10-01T12:00:00",
}

# Insert a document into the index
index = es.index(index="test-index", body=document)
print(index)
