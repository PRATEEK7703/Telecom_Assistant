import chromadb
import os
from config.config import DATA_DIR
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

CHROMA_DB_DIR = os.path.join(DATA_DIR, "chroma_db")

print(f"Testing ChromaDB at: {CHROMA_DB_DIR}")

try:
    if os.path.exists(CHROMA_DB_DIR):
        print("Directory exists.")
    else:
        print("Directory does not exist.")

    print("Initializing PersistentClient...")
    db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    print("PersistentClient initialized.")
    
    print("Getting collection...")
    collection = db.get_or_create_collection("telecom_docs")
    print("Collection retrieved.")
    
    print("Initializing ChromaVectorStore...")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    print("ChromaVectorStore initialized.")
    
    print("Initializing StorageContext...")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    print("StorageContext initialized.")
    
    print("Loading index from vector store...")
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )
    print("Index loaded successfully.")
    
    # Check API Key
    from config.config import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is not set!")
    else:
        print("OPENAI_API_KEY is set.")
        
    print("Creating query engine...")
    query_engine = index.as_query_engine()
    print("Query engine created.")
    
    print("Executing query...")
    response = query_engine.query("test query")
    print(f"Response: {response}")
    
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
