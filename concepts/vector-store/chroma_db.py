from chromadb.utils import embedding_functions
from typing import List, Dict
import chromadb
import json
from datetime import datetime


class VectorStore:
    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(
            name=f"collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}",  # Unique name each time
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction()
        )
    
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents with error handling"""
        
        try:
            ids = [f"doc_{i}" for i in range(len(documents))]
            
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadata if metadata else [{}] * len(documents)
            )
            return True, f"Successfully added {len(documents)} documents"
        except Exception as e:
            return False, f"Error adding documents: {str(e)}"
    
    
    def search_documents(self, query: str, n_results: int = 2, 
                        filter_dict: Dict = None):
        """Search with metadata filtering"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filter_dict  # ChromaDB uses 'where' for filtering
            )
            return True, results
        except Exception as e:
            return False, f"Error searching documents: {str(e)}"
    
    
    def analyze_results(self, collection_results: Dict) -> None:
        """
        Analyzes ChromaDB collection query results with comprehensive error handling.
        
        Args:
            collection_results (Dict): The results dictionary from a ChromaDB query
            
        Returns:
            None
            
        Raises:
            ValueError: If results format is invalid
        
        Parameters in collection_results:
        - 'documents': List[List[str]] - The actual text content of matched documents
        - 'ids': List[List[str]] - Unique identifiers for each document
        - 'distances': List[List[float]] - Similarity scores (closer to 0 = more similar)
        - 'metadatas': List[List[Dict]] - Associated metadata for each document
        - 'embeddings': Optional embeddings data (usually null unless specifically requested)
        """
        
        try:
            if not collection_results.get('documents'):
                print("No results found")
                return
            
            print("\nAnalysis of Query Results:")
            print("=" * 50)
            
            for i in range(len(collection_results['documents'][0])):
                print(f"\nResult #{i+1}")
                print("-" * 20)
                
                # Document content
                print(f"Content: {collection_results['documents'][0][i]}")
                
                # Distance score
                print(f"Similarity Score: {collection_results['distances'][0][i]:.4f}")
                
                # Metadata if available
                if collection_results.get('metadatas'):
                    print(f"Metadata: {collection_results['metadatas'][0][i]}")
                
                # Document ID
                print(f"ID: {collection_results['ids'][0][i]}")        
        except Exception as e:
            print(f"Error analyzing results: {str(e)}")


def test_vector_store():
    # Initialize
    store = VectorStore()
    
    # Test documents and metadata
    documents = [
        "Tokyo is the capital of Japan and a major global financial hub",
        "Kaduna is an industrial city in northern Nigeria",
        "Lagos is the largest city in Nigeria and a major port",
        "The Pacific Ocean borders Asia and the Americas",
        "Mount Fuji is Japan's highest mountain and a cultural symbol"
    ]
    
    metadata = [
        {"type": "city", "country": "Japan", "continent": "Asia"},
        {"type": "city", "country": "Nigeria", "continent": "Africa"},
        {"type": "city", "country": "Nigeria", "continent": "Africa"},
        {"type": "ocean", "category": "geography"},
        {"type": "landmark", "country": "Japan", "continent": "Asia"}
    ]
    
    # Test adding documents
    success, message = store.add_documents(documents, metadata)
    print(f"Adding documents: {message}")
    
    # Test different search scenarios
    test_cases = [
        {
            "query": "Asian cities",
            "filter": {"continent": "Asia"},
            "n_results": 2
        },
        {
            "query": "African locations",
            "filter": {"continent": "Africa"},
            "n_results": 2
        },
        {
            "query": "Geographic features",
            "filter": {"category": "geography"},
            "n_results": 1
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting: {case['query']} with filter {case['filter']}")
        success, results = store.search_documents(
            case['query'],
            case['n_results'],
            case['filter']
        )
        
        if success:
            store.analyze_results(results)
        else:
            print(f"Search failed: {results}")

if __name__ == "__main__":
    test_vector_store()

        
    
    
    
        