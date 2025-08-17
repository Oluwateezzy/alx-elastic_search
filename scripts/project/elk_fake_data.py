from elasticsearch import Elasticsearch

from faker import Faker
import random
from datetime import datetime, timedelta


es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "4CMkmoDx"))


# Elasticsearch index name
INDEX_NAME = "support-tickets"

# Ensure index exists with mapping
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(
        index=INDEX_NAME,
        body={
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "status": {"type": "keyword"},
                    "createdAt": {"type": "date"},
                    "updatedAt": {"type": "date"},
                    "customerId": {"type": "keyword"},
                    "assignedToId": {"type": "keyword"},
                    "activityLogs": {"type": "object"},
                    "verificationLogs": {"type": "object"},
                }
            }
        },
    )

fake = Faker()

# Generate fake tickets
for i in range(1, 21):  # 20 fake tickets
    created_at = fake.date_time_between(start_date="-30d", end_date="now")
    updated_at = created_at + timedelta(hours=random.randint(1, 72))

    ticket = {
        "id": i,
        "title": fake.sentence(nb_words=6),
        "description": fake.paragraph(nb_sentences=3),
        "status": random.choice(["OPEN", "CLOSED"]),
        "createdAt": created_at.isoformat(),
        "updatedAt": updated_at.isoformat(),
        "customerId": fake.uuid4(),
        "assignedToId": random.choice([fake.uuid4(), None]),
        "activityLogs": {
            "actions": [fake.sentence() for _ in range(random.randint(1, 5))]
        },
        "verificationLogs": {
            "checks": [fake.word() for _ in range(random.randint(1, 3))]
        },
    }

    es.index(index=INDEX_NAME, id=i, document=ticket)

print("✅ Inserted 20 fake support tickets into Elasticsearch")
