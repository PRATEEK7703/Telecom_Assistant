import autogen
from config.config import LLM_MODEL, OPENAI_API_KEY

def get_network_group_chat(query, user_email=None):
    config_list = [
        {
            "model": LLM_MODEL,
            "api_key": OPENAI_API_KEY,
        }
    ]
    
    llm_config = {"config_list": config_list}

    # Termination Condition
    def is_termination_msg(content):
        have_content = content.get("content", None) is not None
        if have_content and "TERMINATE" in content["content"].upper():
            return True
        return False

    # Agents
    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        system_message="A human admin. Reply TERMINATE if the task has been solved to your satisfaction.",
        code_execution_config={"last_n_messages": 2, "work_dir": "groupchat", "use_docker": False},
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg
    )

    context_str = f" for customer {user_email}" if user_email else ""

    diagnostics_agent = autogen.AssistantAgent(
        name="Network_Diagnostics_Agent",
        system_message=f"You are a Network Diagnostics Agent. You check for known issues and patterns in network logs{context_str}. You can suggest common fixes for connectivity issues. Format your findings in Markdown.",
        llm_config=llm_config
    )

    router_agent = autogen.AssistantAgent(
        name="Router_Configuration_Agent",
        system_message="You are a Router Configuration Agent. You understand router settings, APN configurations, and technical parameters. You can guide users on how to configure their devices. Provide step-by-step guides in Markdown.",
        llm_config=llm_config
    )

    connectivity_agent = autogen.AssistantAgent(
        name="Connectivity_Specialist_Agent",
        system_message="You are a Connectivity Specialist. You synthesize information from diagnostics and router settings to provide a step-by-step troubleshooting guide. ALWAYS format your final response in Markdown with clear headers (e.g., ### Troubleshooting Steps), bullet points, and bold text. When you have provided the final solution, end your message with the word TERMINATE.",
        llm_config=llm_config
    )

    # Tools
    from langchain_community.utilities import SQLDatabase
    from config.config import DB_CONNECTION_STRING
    
    db = SQLDatabase.from_uri(DB_CONNECTION_STRING)

    def run_sql_query(query: str) -> str:
        return db.run(query)

    def list_tables() -> str:
        return str(db.get_usable_table_names())

    def get_table_schema(table_name: str) -> str:
        return db.get_table_info([table_name])

    # Register tools
    for agent in [diagnostics_agent, router_agent, connectivity_agent]:
        agent.register_for_llm(name="run_sql_query", description="Run a SQL query against the database.")(run_sql_query)
        agent.register_for_llm(name="list_tables", description="List all tables in the database.")(list_tables)
        agent.register_for_llm(name="get_table_schema", description="Get the schema of a specific table.")(get_table_schema)

    user_proxy.register_for_execution(name="run_sql_query")(run_sql_query)
    user_proxy.register_for_execution(name="list_tables")(list_tables)
    user_proxy.register_for_execution(name="get_table_schema")(get_table_schema)

    # Group Chat
    groupchat = autogen.GroupChat(
        agents=[user_proxy, diagnostics_agent, router_agent, connectivity_agent],
        messages=[],
        max_round=30
    )
    
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    return user_proxy, manager
