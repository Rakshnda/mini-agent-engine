import uuid
import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException
from app.models import GraphCreateRequest, GraphRunRequest, RunResponse, RunStatusResponse
from app.engine import WorkflowEngine
from app.storage import db
from app.registry import NODE_REGISTRY

app = FastAPI(title="Mini LangGraph Engine")

# Import workflows after app creation to avoid circular imports
import app.workflows.code_review as code_review_wf

@app.get("/")
def home():
    return {"message": "Agent Engine Running. Registry size: " + str(len(NODE_REGISTRY))}

@app.get("/debug/runs")
def debug_runs():
    """Debug endpoint to see all runs"""
    return {"runs": list(db.runs.keys()), "count": len(db.runs)}

@app.post("/graph/create")
def create_graph(payload: GraphCreateRequest):
    """
    Creates a new graph definition. 
    NOTE: For this mini-version, we construct the engine object and store it.
    """
    graph_id = str(uuid.uuid4())
    
    # Initialize Engine
    engine = WorkflowEngine(graph_id)
    engine.set_entry_point(payload.entry_point)
    
    # 1. Add Nodes (validate against registry)
    for node_name in payload.nodes:
        if node_name not in NODE_REGISTRY:
            raise HTTPException(status_code=400, detail=f"Node '{node_name}' not found in registry.")
        engine.add_node(node_name, NODE_REGISTRY[node_name])
    
    # 2. Add Static Edges
    for start, end in payload.edges.items():
        engine.add_edge(start, end)
        
    # 3. Special Handling for Sample Workflow (Branching/Looping)
    if "suggest_improvements" in payload.nodes:
        engine.add_conditional_edge("suggest_improvements", code_review_wf.quality_gate_router)
        
    db.save_graph(graph_id, engine)
    return {"graph_id": graph_id, "message": "Graph created successfully"}

async def _run_workflow_task(run_id: str, engine: WorkflowEngine, initial_state: dict):
    try:
        final_state, logs = await engine.run(initial_state)
        db.update_run(run_id, "completed", final_state, logs)
    except Exception as e:
        db.update_run(run_id, "failed", {"error": str(e)}, [])

@app.post("/graph/run", response_model=RunResponse)
def run_graph(payload: GraphRunRequest, background_tasks: BackgroundTasks):
    engine = db.get_graph(payload.graph_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    run_id = str(uuid.uuid4())
    db.create_run(run_id)
    
    # Run in background (async)
    background_tasks.add_task(_run_workflow_task, run_id, engine, payload.initial_state)
    
    return {"run_id": run_id, "status": "queued"}

@app.get("/graph/state/{run_id}")
def get_run_state(run_id: str):
    print(f"Looking for run_id: {run_id}")
    print(f"Available runs: {list(db.runs.keys())}")
    data = db.get_run(run_id)
    print(f"Found data: {data}")
    if not data:
        raise HTTPException(status_code=404, detail=f"Run ID '{run_id}' not found. Available: {list(db.runs.keys())}")
    
    return {
        "run_id": run_id, 
        "status": data["status"], 
        "state": data["state"],
        "logs": data["logs"]
    }