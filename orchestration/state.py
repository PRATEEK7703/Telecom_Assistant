from typing import TypedDict, Annotated, List, Union
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[dict], add_messages]
    query: str
    category: str
    response: str
    user_email: str
