from chromadb.utils import embedding_functions
import chromadb
import json 

chroma_client = chromadb.Client()

ppe_collection = chroma_client.create_collection(name="ppe_collection", embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction())

ppe_collection.add(
    documents=[
        "This is a document about tokyo",
        "This is a document about kaduna",
        "This is a document about Nigeria",
        "This is a document about pacific ocean"
    ],
    ids=["id1", "id2", "id3", "id4"]
)

# ppe_results = ppe_collection.query(
#     query_texts=["This is a query document about state and cities"],
#     n_results=2
# )

# print(json.dumps(ppe_results, indent=4))

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