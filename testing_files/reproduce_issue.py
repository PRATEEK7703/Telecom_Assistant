from crewai import Agent
from crewai.tools import BaseTool
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from config.config import DB_CONNECTION_STRING, LLM_MODEL
from langchain_openai import ChatOpenAI

# Initialize Database Tool
db = SQLDatabase.from_uri(DB_CONNECTION_STRING)
sql_tool = QuerySQLDataBaseTool(db=db)

# Wrap the tool
class SQLQueryTool(BaseTool):
    name: str = "SQL Query Tool"
    description: str = "Useful for querying the database."

    def _run(self, query: str) -> str:
        return sql_tool.run(query)

crewai_sql_tool = SQLQueryTool()

# Initialize LLM
llm = ChatOpenAI(model=LLM_MODEL)

try:
    print("Initializing Agent...")
    billing_specialist = Agent(
        role='Billing Specialist',
        goal='Analyze customer bills',
        backstory='Expert in billing.',
        tools=[crewai_sql_tool],
        llm=llm,
        verbose=True
    )
    print("Agent initialized successfully.")
except Exception as e:
    print(f"Error initializing agent: {e}")
