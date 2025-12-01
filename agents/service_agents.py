from langgraph.prebuilt import create_react_agent
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool, InfoSQLDatabaseTool, ListSQLDatabaseTool
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from config.config import DB_CONNECTION_STRING, LLM_MODEL

# Initialize Database Tool
db = SQLDatabase.from_uri(DB_CONNECTION_STRING)
sql_tool = QuerySQLDataBaseTool(db=db)
info_tool = InfoSQLDatabaseTool(db=db)
list_tables_tool = ListSQLDatabaseTool(db=db)

# Initialize LLM
llm = ChatOpenAI(model=LLM_MODEL)

def get_service_agent(query, user_email=None):
    # Create Agent
    tools = [sql_tool, info_tool, list_tables_tool]
    
    context_str = f" You are assisting a customer with email: {user_email}." if user_email else ""
    
    system_message = f"""You are a helpful Service Recommendation Agent.{context_str}
    Your goal is to suggest the best telecom plans for customers based on their needs.
    ALWAYS format your final response in Markdown.
    Use headers (e.g., ### Plan Options), bullet points, and bold text for emphasis.
    When presenting plan details, use a Markdown table if possible or structured lists.
    """
    
    agent = create_react_agent(llm, tools, prompt=system_message)
    
    return agent
