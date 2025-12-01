from langchain_openai import OpenAIEmbeddings
from config.config import OPENAI_API_KEY, EMBEDDING_MODEL
import os

print(f"API Key present: {bool(OPENAI_API_KEY)}")

try:
    print("Initializing OpenAIEmbeddings...")
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )
    print("Embeddings initialized.")
    
    print("Embedding query...")
    query_embedding = embeddings.embed_query("test query")
    print("Query embedded.")
    print(f"Embedding length: {len(query_embedding)}")
    
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
