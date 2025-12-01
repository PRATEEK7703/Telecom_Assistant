from orchestration.graph import app
from config.config import OPENAI_API_KEY

def test_query(query, expected_category):
    print(f"\n--- Testing Query: {query} ---")
    try:
        result = app.invoke({"query": query})
        response = result["response"]
        print(f"Response: {response}")
        print("Status: Success")
    except Exception as e:
        print(f"Error: {e}")
        print("Status: Failed")

if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found.")
    else:
        print("Starting Verification...")
        # Test Billing
        try:
            test_query("Why is my bill higher this month?", "BILLING")
        except Exception as e:
            print(f"Billing Test Failed: {e}")
        
        # Test Network
        try:
            test_query("I can't make calls from my home area", "NETWORK")
        except Exception as e:
            print(f"Network Test Failed: {e}")
        
        # Test Service
        try:
            test_query("What's the best plan for a family of four?", "SERVICE")
        except Exception as e:
            print(f"Service Test Failed: {e}")
        
        # Test Knowledge
        try:
            test_query("How do I enable VoLTE?", "KNOWLEDGE")
        except Exception as e:
            print(f"Knowledge Test Failed: {e}")
        
        print("Verification Completed.")
