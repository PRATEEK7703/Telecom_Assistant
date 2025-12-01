import os
import sys

# Add current directory to sys.path
sys.path.append(os.getcwd())

from orchestration.graph import app

def test_personalization(email, query):
    print(f"\n--- Testing for User: {email} ---")
    print(f"Query: {query}")
    
    try:
        inputs = {
            "query": query,
            "user_email": email
        }
        result = app.invoke(inputs)
        response = result["response"]
        print(f"Response:\n{response}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

if __name__ == "__main__":
    # Test 1: Siva (Existing user)
    test_personalization("siva@example.com", "What is my current bill amount?")
    
    # Test 2: Vikram (Another existing user)
    test_personalization("vikram.reddy@example.com", "What is my current bill amount?")
