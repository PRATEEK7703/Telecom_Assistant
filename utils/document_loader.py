import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from config.config import DOCS_DIR, DATA_DIR

# Persist directory for SimpleVectorStore
STORAGE_DIR = os.path.join(DATA_DIR, "storage")

def load_documents():
    """Loads documents from the documents directory and creates/updates the vector index."""
    if not os.path.exists(DOCS_DIR):
        print(f"Documents directory not found: {DOCS_DIR}")
        return None

    # Load documents
    reader = SimpleDirectoryReader(DOCS_DIR)
    documents = reader.load_data()
    
    # Create index
    index = VectorStoreIndex.from_documents(documents)
    
    # Persist index
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
    index.storage_context.persist(persist_dir=STORAGE_DIR)
    
    return index

def get_index():
    """Retrieves the existing vector index."""
    print("DEBUG: Entering get_index")
    if not os.path.exists(STORAGE_DIR):
        print("DEBUG: Storage dir does not exist, loading documents")
        return load_documents()

    try:
        print("DEBUG: Storage dir exists, loading from storage")
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        index = load_index_from_storage(storage_context)
        print("DEBUG: Index loaded successfully")
        return index
    except Exception as e:
        print(f"Error loading index: {e}")
        return load_documents()
