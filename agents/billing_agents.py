from crewai import Agent, Task, Crew, Process
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from config.config import DB_CONNECTION_STRING, LLM_MODEL
from langchain_openai import ChatOpenAI

# Initialize Database Tool
db = SQLDatabase.from_uri(DB_CONNECTION_STRING)
sql_tool = QuerySQLDataBaseTool(db=db)

# Initialize LLM
llm = ChatOpenAI(model=LLM_MODEL)

from crewai.tools import BaseTool

# Wrap the tool
class SQLQueryTool(BaseTool):
    name: str = "SQL Query Tool"
    description: str = "Useful for executing SQL queries against the database. Input should be a valid SQL query string."

    def _run(self, query: str) -> str:
        return sql_tool.run(query)

class ListTablesTool(BaseTool):
    name: str = "List Tables Tool"
    description: str = "Useful for listing all tables in the database."

    def _run(self, args: str = "") -> str:
        return str(db.get_usable_table_names())

class GetTableSchemaTool(BaseTool):
    name: str = "Get Table Schema Tool"
    description: str = "Useful for getting the schema of a specific table. Input should be the table name."

    def _run(self, table_name: str) -> str:
        return db.get_table_info([table_name])

crewai_sql_tool = SQLQueryTool()
list_tables_tool = ListTablesTool()
get_schema_tool = GetTableSchemaTool()

def get_billing_crew(query, user_email=None):
    # Agents
    billing_specialist = Agent(
        role='Billing Specialist',
        goal='Analyze customer bills and explain charges clearly',
        backstory='You are an expert in telecom billing systems. You can query the database to find customer bill details and explain any discrepancies or high charges. Always check the database schema first to understand the table structure.',
        tools=[list_tables_tool, get_schema_tool, crewai_sql_tool],
        llm=llm,
        verbose=True
    )

    service_advisor = Agent(
        role='Service Advisor',
        goal='Suggest plan changes or add-ons based on billing analysis',
        backstory='You help customers optimize their spending by suggesting better plans or add-ons based on their usage and billing history. Always check the database schema first.',
        tools=[list_tables_tool, get_schema_tool, crewai_sql_tool],
        llm=llm,
        verbose=True
    )

    # Tasks
    context_str = f" for customer with email '{user_email}'" if user_email else ""
    
    analysis_task = Task(
        description=f'Analyze the billing query: "{query}"{context_str}. Check the database for the customer\'s recent bills and usage. Identify any anomalies or reasons for high charges. Format your response in Markdown with clear headers and bullet points.',
        expected_output='A detailed analysis of the billing charges in Markdown format, using headers (e.g., ### Analysis) and bullet points.',
        agent=billing_specialist
    )

    recommendation_task = Task(
        description=f'Based on the billing analysis, suggest any plan changes or add-ons that could save the customer money or provide better value. Format your response in Markdown.',
        expected_output='Recommendations for plan changes or add-ons in Markdown format, using headers (e.g., ### Recommendations) and bullet points.',
        agent=service_advisor,
        context=[analysis_task]
    )

    # Crew
    billing_crew = Crew(
        agents=[billing_specialist, service_advisor],
        tasks=[analysis_task, recommendation_task],
        process=Process.sequential,
        verbose=True
    )

    return billing_crew
