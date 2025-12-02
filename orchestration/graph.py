from langgraph.graph import StateGraph, END
from orchestration.state import AgentState
from agents.billing_agents import get_billing_crew
from agents.network_agents import get_network_group_chat
from agents.service_agents import get_service_agent
from agents.knowledge_agents import get_knowledge_agent
from langchain_openai import ChatOpenAI
from config.config import LLM_MODEL
import json

# Initialize LLM
llm = ChatOpenAI(model=LLM_MODEL)

def classify_query(state: AgentState):
    """Classifies the user query into one of the four categories."""
    query = state["query"]
    
    prompt = f"""
    Classify the following telecom query into one of these categories:
    1. BILLING (e.g., bill amount, charges, add-ons)
    2. NETWORK (e.g., signal issues, internet speed, troubleshooting)
    3. SERVICE (e.g., plan recommendations, new connections)
    4. KNOWLEDGE (e.g., technical docs, how-to guides, coverage)
    5. OTHERS (e.g., cooking recipes, general knowledge, politics, unrelated topics)
    
    Query: {query}
    
    Return only the category name (BILLING, NETWORK, SERVICE, KNOWLEDGE, or OTHERS).
    """
    
    response = llm.invoke(prompt)
    category = response.content.strip().upper()
    return {"category": category}

def billing_node(state: AgentState):
    """Handles billing queries using CrewAI."""
    query = state["query"]
    user_email = state.get("user_email")
    crew = get_billing_crew(query, user_email)
    result = crew.kickoff()
    return {"response": str(result)}

def network_node(state: AgentState):
    """Handles network queries using AutoGen."""
    query = state["query"]
    user_email = state.get("user_email")
    # AutoGen might need a different way to pass context, but for now passing to factory
    user_proxy, manager = get_network_group_chat(query, user_email)
    
    # Initiate chat
    user_proxy.initiate_chat(
        manager,
        message=f"User ({user_email}) asks: {query}"
    )
    
    # Extract the last message as the response
    # This is a simplification; in a real app, you'd parse the chat history
    last_message = user_proxy.last_message()["content"]
    return {"response": last_message}

def service_node(state: AgentState):
    """Handles service recommendations using LangChain."""
    query = state["query"]
    user_email = state.get("user_email")
    agent_executor = get_service_agent(query, user_email)
    result = agent_executor.invoke({"messages": [("user", f"User ({user_email}) asks: {query}")]})
    return {"response": result["messages"][-1].content}

def knowledge_node(state: AgentState):
    """Handles knowledge queries using LlamaIndex."""
    query = state["query"]
    query_engine = get_knowledge_agent(query)
    if isinstance(query_engine, str): # Error case
        return {"response": query_engine}
        
    response = query_engine.query(query)
    return {"response": str(response)}

def out_of_context_node(state: AgentState):
    """Handles out-of-context queries."""
    return {"response": "I can't say since it is out of context."}

def formulate_response(state: AgentState):
    """Formats the final response."""
    # In this simple version, we just pass through the response
    # You could add more formatting or logging here
    return {"response": state["response"]}

def route_query(state: AgentState):
    """Routes the query based on classification."""
    category = state["category"]
    if category == "BILLING":
        return "billing_node"
    elif category == "NETWORK":
        return "network_node"
    elif category == "SERVICE":
        return "service_node"
    elif category == "KNOWLEDGE":
        return "knowledge_node"
    elif category == "OTHERS":
        return "out_of_context_node"
    else:
        return "knowledge_node" # Default fallback

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("classify_query", classify_query)
workflow.add_node("billing_node", billing_node)
workflow.add_node("network_node", network_node)
workflow.add_node("service_node", service_node)
workflow.add_node("knowledge_node", knowledge_node)
workflow.add_node("out_of_context_node", out_of_context_node)
workflow.add_node("formulate_response", formulate_response)

workflow.set_entry_point("classify_query")

workflow.add_conditional_edges(
    "classify_query",
    route_query,
    {
        "billing_node": "billing_node",
        "network_node": "network_node",
        "service_node": "service_node",
        "service_node": "service_node",
        "knowledge_node": "knowledge_node",
        "out_of_context_node": "out_of_context_node"
    }
)

workflow.add_edge("billing_node", "formulate_response")
workflow.add_edge("network_node", "formulate_response")
workflow.add_edge("service_node", "formulate_response")
workflow.add_edge("knowledge_node", "formulate_response")
workflow.add_edge("out_of_context_node", "formulate_response")
workflow.add_edge("formulate_response", END)

app = workflow.compile()
