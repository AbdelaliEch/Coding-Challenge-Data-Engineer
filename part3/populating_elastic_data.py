from elasticsearch import Elasticsearch
from pprint import pprint
import json

# Connect to the local Elasticsearch instance
es = Elasticsearch('http://localhost:9200')
# Check if Elasticsearch is running
if not es.ping():
    print("Elasticsearch not running")
    exit(1)

pprint(es.info().body)

es.indices.create(index="user_sessions")

# Load mock user session data from a JSON file
try:
    with open('mock_data.json','r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Data file not found")
    exit(1)

# Prepare bulk operations for inserting documents into Elasticsearch
operations = []
for document in data:
    operations.append({"index": {"_index": "user_sessions"}})
    operations.append(document)

# Bulk insert all documents into the "user_sessions" index
es.bulk(body=operations)

# Refresh the index to make sure all documents are searchable
es.indices.refresh(index="user_sessions")

# Count the number of documents in the index to verify insertion
doc_count = es.count(index='user_sessions')

print(f"Number of documents indexed: {doc_count['count']}")