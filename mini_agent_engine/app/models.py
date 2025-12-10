from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Node(BaseModel):
    id: str
    type: str
    params: Dict[str, Any] = {}

class Graph(BaseModel):
    id: str
    nodes: List[Node] = []

class GraphCreateRequest(BaseModel):
    nodes: List[str]  # List of function names from registry
    edges: Dict[str, str]  # static edges: {"nodeA": "nodeB"}
    entry_point: str

class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class RunResponse(BaseModel):
    run_id: str
    status: str

class RunStatusResponse(BaseModel):
    run_id: str
    status: str  # 'running', 'completed', 'failed'
    state: Dict[str, Any]
    logs: List[Dict]