from elasticsearch import Elasticsearch
from pprint import pprint
import json

es = Elasticsearch('http://localhost:9200')
# Check if Elasticsearch is running
if not es.ping():
    print("Elasticsearch not running")
    exit(1)

pprint(es.info().body)

es.indices.create(index="user_sessions")

try:
    with open('mock_data.json','r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Data file not found")
    exit(1)

operations = []
for document in data:
    operations.append({"index": {"_index": "user_sessions"}})
    operations.append(document)

es.bulk(body=operations)

es.indices.refresh(index="user_sessions")

doc_count = es.count(index='user_sessions')

print(f"Number of documents indexed: {doc_count['count']}")