import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Fallback for development if .env is not set, though not recommended for production
    # You might want to raise an error or handle this gracefully
    pass

# Model Configurations
LLM_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-small"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "telecom.db")
DOCS_DIR = os.path.join(DATA_DIR, "documents")

# Database Configuration
DB_CONNECTION_STRING = f"sqlite:///{DB_PATH}"

# Streamlit Configuration
STREAMLIT_PAGE_TITLE = "Telecom Service Assistant"
STREAMLIT_PAGE_ICON = "📞"
