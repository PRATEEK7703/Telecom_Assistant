from openai import OpenAI
from config.config import OPENAI_API_KEY, LLM_MODEL
import os

print(f"API Key present: {bool(OPENAI_API_KEY)}")

try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("Client initialized.")
    
    print("Sending request...")
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("Response received.")
    print(response.choices[0].message.content)
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
