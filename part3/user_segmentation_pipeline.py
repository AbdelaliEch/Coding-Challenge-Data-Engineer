from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from collections import Counter


es = Elasticsearch('http://localhost:9200')
# Check if Elasticsearch is running
if not es.ping():
    print("Elasticsearch not running")
    exit(1)


# Function to extract search history per user from Elasticsearch
def extract_user_search_history(index='user_sessions'):
    
    response = es.search(
        index = index,
        body = {
            "aggs": {
                "users": {
                    "terms": {"field": "user_id.keyword", "size": 20000},
                    "aggs": {
                        "search_queries": {
                            "terms": {"field": "search_query.keyword", "size": 100}
                        }
                    }
                }
            } 
        }     
    )

    users_search_history = []
    for bucket in response['aggregations']['users']['buckets']:
        user_id = bucket['key']
        user_search_queries = [value['key'] for value in bucket['search_queries']['buckets']]
        user_search_history = {"user_id":user_id, "search_queries":user_search_queries}
        users_search_history.append(user_search_history)

    return users_search_history


# Function to convert search queries of each user into vectors using SentenceTransformer
def convert_search_queries_to_vectors(users_search_history, model_name = 'all-MiniLM-L6-v2'):

    model = SentenceTransformer(model_name)

    users_embeddings = []

    for user in users_search_history:
        queries = user['search_queries']
        queries_joined = ' '.join(queries)
        
        embeddings = model.encode(queries_joined)
        users_embeddings.append({'user_id': user['user_id'], 'search_queries': queries, 'embedding': embeddings.tolist()})

    return users_embeddings


# Function to group users into segments using Kmeans clustering
def cluster_into_segments(users_embeddings, n_clusters=5):
    embedding_list = [user['embedding'] for user in users_embeddings]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(embedding_list)

    for user, label in zip(users_embeddings, kmeans.labels_):
        user['segment'] = int(label)

    return users_embeddings


users_search_history = extract_user_search_history()

users_embeddings = convert_search_queries_to_vectors(users_search_history)

users_embeddings_segmented = cluster_into_segments(users_embeddings)


# Function to count search queries per segment
def count_queries_per_segment(users_embeddings_segmented):
    
    segment0_queries = []
    segment1_queries = []
    segment2_queries = []
    segment3_queries = []
    segment4_queries = []

    for user in users_embeddings_segmented:
        if user['segment'] == 0:
            segment0_queries.extend(user['search_queries'])
        elif user['segment'] == 1:
            segment1_queries.extend(user['search_queries'])
        elif user['segment'] == 2:
            segment2_queries.extend(user['search_queries'])
        elif user['segment'] == 3:
            segment3_queries.extend(user['search_queries'])
        elif user['segment'] == 4:
            segment4_queries.extend(user['search_queries'])

    print(f"Segment 0: {Counter(segment0_queries)}")
    print(f"Segment 1: {Counter(segment1_queries)}")
    print(f"Segment 2: {Counter(segment2_queries)}")
    print(f"Segment 3: {Counter(segment3_queries)}")
    print(f"Segment 4: {Counter(segment4_queries)}")

# Output of the count_queries_per_segment function:
    # Segment 0: Counter({'kitchen organizer': 49, 'robot vacuum': 41, 'indoor plants': 40, 'LED ceiling lights': 40, 'air fryer': 37})
    # Segment 1: Counter({'protein powder': 58, 'resistance bands': 57, 'fitness tracker': 55, 'dumbbells': 51, 'yoga mat': 48})
    # Segment 2: Counter({'summer dresses': 59, 'sneakers': 49, 'denim jacket': 47, 'designer handbags': 44, 'leather boots': 44})
    # Segment 3: Counter({'noise-cancelling headphones': 59, 'USB-C hub': 54, 'gaming laptop': 53, 'external SSD': 52, 'mechanical keyboard': 51})
    # Segment 4: Counter({'refurbished tablet': 53, 'discount smartwatch': 51, 'affordable earbuds': 51, 'cheap phone': 49, 'low price laptop': 42})

# Define segment labels based on the output of the count_queries_per_segment function
segment_labels = {
    0: "Home & Kitchen enthusiasts",
    1: "Fitness & Health seekers",
    2: "Fashion lovers",
    3: "Tech shoppers",
    4: "Budget-conscious buyers"
}

# Function to store users and their segment labels in Elasticsearch
def store_users_segments(users_embeddings_segmented, index='user_segments'):
    
    es.indices.create(index=index)

    operations = []
    for user in users_embeddings_segmented:
        operations.append({"index": {"_index":index}})
        operations.append({"user_id": user['user_id'], "segment_label": segment_labels[user['segment']]})

    es.bulk(body=operations)

store_users_segments(users_embeddings_segmented)