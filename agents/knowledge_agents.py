from utils.document_loader import get_index
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from config.config import LLM_MODEL
from llama_index.llms.openai import OpenAI

def get_knowledge_agent(query):
    # Load Index
    print("DEBUG: Loading index in get_knowledge_agent")
    index = get_index()
    if not index:
        return "Error: Knowledge base not initialized."

    # Create Query Engine
    print("DEBUG: Creating vector query engine")
    vector_query_engine = index.as_query_engine()
    
    # Define Tools
    query_engine_tools = [
        QueryEngineTool(
            query_engine=vector_query_engine,
            metadata=ToolMetadata(
                name="vector_tool",
                description="Useful for retrieving specific technical information from documentation."
            )
        )
    ]

    # Initialize LLM
    llm = OpenAI(model=LLM_MODEL)

    # Create Router Query Engine
    print("DEBUG: Creating RouterQueryEngine")
    router_query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(llm=llm),
        query_engine_tools=query_engine_tools,
        verbose=True
    )

    return router_query_engine
