from agents.knowledge_agents import get_knowledge_agent
from config.config import OPENAI_API_KEY
import traceback

if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found.")
    else:
        print("Starting Knowledge Agent Test...")
        try:
            query = "How do I enable VoLTE?"
            print(f"Query: {query}")
            query_engine = get_knowledge_agent(query)
            if isinstance(query_engine, str):
                print(f"Error initializing agent: {query_engine}")
            else:
                print("DEBUG: Agent initialized successfully.")
                # Hack to access the vector query engine directly for debugging
                # The get_knowledge_agent returns a RouterQueryEngine
                # We want to test the underlying vector query engine
                
                # Re-create the vector query engine locally for testing
                from utils.document_loader import get_index
                print("DEBUG: Re-loading index...")
                index = get_index()
                print("DEBUG: Creating vector query engine directly...")
                vector_query_engine = index.as_query_engine()
                
                print("DEBUG: Executing query on vector engine directly...")
                response = vector_query_engine.query(query)
                print("DEBUG: Query execution completed.")
                print(f"Response: {response}")
        except Exception:
            traceback.print_exc()
        
        print("Test Completed.")
