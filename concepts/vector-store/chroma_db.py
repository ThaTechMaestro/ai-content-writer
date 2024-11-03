from chromadb.utils import embedding_functions
from typing import List, Dict
import chromadb
import json, 

chroma_client = chromadb.Client()

ppe_collection = chroma_client.create_collection(name="ppe_collection", embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction())

ppe_collection.add(
    documents=[
        "Tokyo is the capital of Japan and a major global financial hub",
        "Kaduna is an industrial city in northern Nigeria",
        "Lagos is the largest city in Nigeria and a major port",
        "The Pacific Ocean borders Asia and the Americas",
        "Mount Fuji is Japan's highest mountain and a cultural symbol"
    ],
    ids=["id1", "id2", "id3", "id4"],
    metadata=[
    {"type": "city", "country": "Japan", "continent": "Asia"},
    {"type": "city", "country": "Nigeria", "continent": "Africa"},
    {"type": "city", "country": "Nigeria", "continent": "Africa"},
    {"type": "ocean", "category": "geography"},
    {"type": "landmark", "country": "Japan", "continent": "Asia"}
    ]
)

metadata = [
    {"type": "city", "country": "Japan", "continent": "Asia"},
    {"type": "city", "country": "Nigeria", "continent": "Africa"},
    {"type": "city", "country": "Nigeria", "continent": "Africa"},
    {"type": "ocean", "category": "geography"},
    {"type": "landmark", "country": "Japan", "continent": "Asia"}
]

ppe_results = ppe_collection.query(
    query_texts=["This is a query document about state and cities"],
    n_results=2
)

print(json.dumps(ppe_results, indent=4))


def add_documents(documents: List[str], metadata: List[Dict] = None, ids: List[str]=[]):
    """Add documents with error handling"""
    
    try:
        ppe_collection.add(
            documents=documents,
            ids=ids,
            metadata=metadata
        )
    except Exception as e:
        print(e)


def search_documents(query: str, n_results: int = 2, 
                    filter_dict: Dict = None):
    """Search with metadata filtering"""
    try:
        ppe_search_result = ppe_collection.query(
            query_texts=query,
            n_results=n_results,
            filter_dict=filter_dict
        )
        return ppe_search_result
    except Exception as e:
        print(e)
    pass


def analyze_results(results: Dict):
    """Pretty print results with distances and metadata"""
    pass


#----------------------------------
# TEST IMPLEMENTATIONS
test_queries = [
    "tell me about bodies of water",
    "African cities",
    "Asian locations"
]

for query in test_queries:
    print(f"\nQuery: {query}")
    results = ppe_collection.query(
        query_texts=[query],
        n_results=2
    )
    
    print(json.dumps(results, indent=4))