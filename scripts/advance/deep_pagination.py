from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import random
import time
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))

index_name = "my_index"
mappings = {
    "mappings": {
        "properties": {
            "timestamp": {"type": "date"},
            "value": {"type": "float"},
            "category": {"type": "keyword"},
            "description": {"type": "text"},
            "id": {"type": "keyword"},
        }
    },
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
}

es.indices.delete(index=index_name, ignore_unavailable=True)
es.indices.create(index=index_name, body=mappings)

base_documents = [
    {"category": "A", "value": 100, "description": "First sample document"},
    {"category": "B", "value": 200, "description": "Second sample document"},
    {"category": "C", "value": 300, "description": "Third sample document"},
    {"category": "D", "value": 400, "description": "Fourth sample document"},
    {"category": "E", "value": 500, "description": "Fifth sample document"},
]


def generate_bulk_data(base_documents, target_size=100_000):
    documents = []
    base_count = len(base_documents)
    duplications_needed = target_size // base_count

    base_timestamp = datetime.now()

    for i in range(duplications_needed):
        for document in base_documents:
            new_doc = document.copy()
            new_doc["id"] = f"doc_{len(documents)}"
            new_doc["timestamp"] = (
                base_timestamp - timedelta(minutes=len(documents))
            ).isoformat()
            new_doc["value"] = document["value"] + random.uniform(-10, 10)
            documents.append(new_doc)

    return documents


documents = generate_bulk_data(base_documents, target_size=100_000)
print(f"Generated {len(documents)} documents")

operations = []
for document in documents:
    operations.append({"index": {"_index": index_name}})
    operations.append(document)


response = es.bulk(operations=operations)
print(response.body["errors"])


es.indices.refresh(index=index_name)

count = es.count(index=index_name)["count"]
print(f"Indexed {count} documents")

# From / Size method
# To use the from/size method, include two parameters in your query: from, which specifies the number of documents to skip, and size, which tells Elasticsearch how many documents to return.
response = es.search(
    index=index_name,
    body={"from": 10, "size": 10, "sort": [{"timestamp": "desc"}, {"id": "desc"}]},
)

hits = response["hits"]["hits"]
for hit in hits:
    print(f"ID: {hit['_source']['id']}")
    print(f"Sort values: {hit['sort']}")
    print()

# To retrieve the next batch of documents using search_after, you’ll pass the sort values from the last document of the previous batch to the search_after parameter in the subsequent query.
last_sort_values = hits[-1]["sort"]
res = es.search(
    index=index_name,
    body={
        "size": 10,
        "sort": [{"timestamp": "desc"}, {"id": "desc"}],
        "search_after": last_sort_values,
    },
)

hits = response["hits"]["hits"]
for hit in hits:
    print(f"ID: {hit['_source']['id']}")
    print(f"Sort values: {hit['sort']}")
    print()

# Benchmark
# In this benchmark, we assess the performance of two pagination methods, from/size and search_after, by measuring and comparing their response times. We capture the response time of each method for multiple pages, plot the results, and calculate relevant statistics to provide insights.


def test_from_size_pagination(index_name, page_size=100, max_pages=50):
    timings = []

    for page in range(max_pages):
        start_time = time.time()

        _ = es.search(
            index=index_name,
            body={
                "from": page * page_size,
                "size": page_size,
                "sort": [{"timestamp": "desc"}, {"id": "desc"}],
            },
        )

        end_time = time.time()
        final_time = (end_time - start_time) * 1000
        timings.append((page + 1, final_time))

    return timings


# When attempting to retrieve more than 10,000 documents, Elasticsearch returns an error indicating that the from / size method cannot handle this request.
from_size_timings = test_from_size_pagination(
    index_name=index_name, page_size=200, max_pages=50
)

print(from_size_timings)


# Search after test
def test_search_after_pagination(index_name, page_size=100, max_pages=50):
    timings = []
    search_after = None

    for page in range(max_pages):
        start_time = time.time()

        body = {"size": page_size, "sort": [{"timestamp": "desc"}, {"id": "desc"}]}

        if search_after:
            body["search_after"] = search_after

        response = es.search(index=index_name, body=body)

        hits = response["hits"]["hits"]
        if hits:
            search_after = hits[-1]["sort"]

        end_time = time.time()
        final_time = (end_time - start_time) * 1000
        timings.append((page + 1, final_time))

    return timings


search_after_timings = test_search_after_pagination(
    index_name, page_size=200, max_pages=50
)

print(search_after_timings)


def plot_comparison(from_size_timings, search_after_timings):
    plt.figure(figsize=(12, 6))

    pages_from_size, times_from_size = zip(*from_size_timings)
    pages_search_after, times_search_after = zip(*search_after_timings)

    plt.plot(pages_from_size, times_from_size, "b-", label="from/size")
    plt.plot(pages_search_after, times_search_after, "g-", label="search_after")

    plt.xlabel("Page number")
    plt.ylabel("Response time (milliseconds)")
    plt.title("Pagination performance comparison")
    plt.legend()
    plt.grid(True)
    plt.show()


plot_comparison(from_size_timings, search_after_timings)


# The search_after method performs more efficiently, especially for deep pagination, due to its stable response time. In contrast, from/size may be suitable for shallow pagination but becomes inefficient as the page depth grows.
def calculate_stats(from_size_timings, search_after_timings):
    _, times_from_size = zip(*from_size_timings)
    _, times_search_after = zip(*search_after_timings)

    stats = {
        "from_size": {
            "avg_time": sum(times_from_size) / len(times_from_size),
            "max_time": max(times_from_size),
            "min_time": min(times_from_size),
        },
        "search_after": {
            "avg_time": sum(times_search_after) / len(times_search_after),
            "max_time": max(times_search_after),
            "min_time": min(times_search_after),
        },
    }
    return stats


stats = calculate_stats(from_size_timings, search_after_timings)

print("\nPerformance statistics:")
print("\n- From/Size pagination:")
print(f"Average time: {stats['from_size']['avg_time']:.3f} milliseconds")
print(f"Maximum time: {stats['from_size']['max_time']:.3f} milliseconds")
print(f"Minimum time: {stats['from_size']['min_time']:.3f} milliseconds")

print("\n- Search after pagination:")
print(f"Average time: {stats['search_after']['avg_time']:.3f} milliseconds")
print(f"Maximum time: {stats['search_after']['max_time']:.3f} milliseconds")
print(f"Minimum time: {stats['search_after']['min_time']:.3f} milliseconds")

plt.figure(figsize=(12, 6))
_, times_from_size = zip(*from_size_timings)
_, times_search_after = zip(*search_after_timings)

plt.hist(times_from_size, alpha=0.5, label="from/size", bins=20)
plt.hist(times_search_after, alpha=0.5, label="search_after", bins=20)
plt.xlabel("Response time (milliseconds)")
plt.ylabel("Frequency")
plt.title("Distribution of response times")
plt.legend()
plt.grid(True)
plt.show()


# Based on this histogram visualization, the search_after approach (shown in orange) demonstrates consistently faster response times clustered around 2-5 milliseconds, while the from/size method (in blue) shows a wider distribution of response times spreading up to 16 milliseconds, suggesting that search_after provides more predictable and generally better performance for pagination.
def calculate_degradation(timings):
    first_page_time = timings[0][1]
    last_page_time = timings[-1][1]
    degradation_factor = last_page_time / first_page_time
    return degradation_factor


from_size_degradation = calculate_degradation(from_size_timings)
search_after_degradation = calculate_degradation(search_after_timings)

print("\nPerformance degradation (Last page time / First page time):")
print(f"- From/Size degradation factor   : {from_size_degradation:.2f}x")
print(f"- Search after degradation factor: {search_after_degradation:.2f}x")
