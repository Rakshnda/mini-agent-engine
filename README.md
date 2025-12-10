**mini-agent-engine**

A minimal workflow/agent engine (simplified LangGraph) built with FastAPI. Define nodes, edges, and state; run workflows end-to-end via HTTP API.

**Overview**

This implementation provides a small but functional graph-based workflow engine. It supports defining nodes (Python functions), linking them using edges, maintaining shared state, and executing workflows step-by-step. Looping, branching, and simple tool registration are included.

**What This Engine Supports**

Nodes: Python functions decorated with @register_node, each receiving and returning state.

State: A Python dictionary passed across workflow steps.

Edges: Routing between nodes ({"a": "b"}) or conditional routing through router functions.

Branching: Conditional logic such as checking a state value to decide next node.

Looping: Nodes may route execution back to earlier steps until a condition is met.

Tools: Reusable functions registered with @register_tool.

Async Execution: Workflows run in the background; clients can poll status.

Execution Logging: Logs stored per run with executed nodes and state snapshots.

**How to Run**

1. Install dependencies
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

2. Start the server
python -m uvicorn app.main:app --reload

3. Test the API (PowerShell Example)
Create a graph
$payload = @{
    entry_point = "extract_functions"
    nodes = @("extract_functions", "check_complexity", "detect_issues", "suggest_improvements")
    edges = @{
        "extract_functions" = "check_complexlicity"
        "check_complexity" = "detect_issues"
        "detect_issues" = "suggest_improvements"
    }
} | ConvertTo-Json

$resp = Invoke-RestMethod -Uri "http://127.0.0.1:8000/graph/create" -Method Post -ContentType "application/json" -Body $payload
$graphId = $resp.graph_id

Run the graph
$runPayload = @{
    graph_id = $graphId
    initial_state = @{ code = "def hello(): print('hi')" }
} | ConvertTo-Json

$runResp = Invoke-RestMethod -Uri "http://127.0.0.1:8000/graph/run" -Method Post -ContentType "application/json" -Body $runPayload
$runId = $runResp.run_id

Check execution state
Start-Sleep -Seconds 2
Invoke-RestMethod -Uri "http://127.0.0.1:8000/graph/state/$runId" -Method Get

**Sample Workflow: Code Review** 

Extract functions

Check complexity

Detect basic issues

Suggest improvements

Loop until quality_score >= threshold

This demonstrates node execution, state mutation, branching, and looping. All logic is rule-based.

**Improvements**

Database persistence instead of in-memory storage

WebSocket log streaming

Unit and integration tests

Input validation with stricter schemas

Error handling improvements

API authentication

Graph visualization

Dynamic node registration via API

**Tech Stack**

FastAPI

Pydantic

Uvicorn

Python 3.11+
