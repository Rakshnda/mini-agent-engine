# mini-agent-engine

A minimal workflow / agent engine (simplified LangGraph) built with FastAPI. Define nodes, edges, and state; run workflows end-to-end via HTTP API.

## Overview

This is a clean, working implementation of a graph-based workflow engine. It lets you:
- Define **nodes** (Python functions that read/modify state).
- Connect them with **edges** (static routing or conditional branching).
- Run workflows **end-to-end** with a shared state dictionary.
- Support **looping** and **conditional branching** for complex logic.
- Execute asynchronously in the background via FastAPI.

## What This Engine Supports

- **Nodes**: Python functions decorated with `@register_node`. Each receives and returns state.
- **State**: A dictionary flowing through the workflow.
- **Edges**: Static (`{"node_a": "node_b"}`) or conditional (router function).
- **Branching**: If-else logic via router functions (e.g., "if quality_score >= 80, go to END").
- **Looping**: Nodes can loop back based on state conditions.
- **Tools**: Reusable functions in a registry (`@register_tool`).
- **Async Execution**: Workflows run in the background; poll `/graph/state/{run_id}` to check progress.
- **Execution Logging**: Full step-by-step logs of node execution.

## How to Run

### 1. Install Dependencies
```powershell
cd mini_agent_engine

**## start server**
python -m uvicorn app.main:app --reload

**## Test API**

# Create a graph
$payload = @{
    entry_point = "extract_functions"
    nodes = @("extract_functions", "check_complexity", "detect_issues", "suggest_improvements")
    edges = @{ 
        "extract_functions" = "check_complexity"
        "check_complexity" = "detect_issues"
        "detect_issues" = "suggest_improvements"
    }
} | ConvertTo-Json

$resp = Invoke-RestMethod -Uri "http://127.0.0.1:8000/graph/create" -Method Post -ContentType "application/json" -Body $payload
$graphId = $resp.graph_id

# Run the graph
$runPayload = @{
    graph_id = $graphId
    initial_state = @{ code = "def hello(): print('hi')" }
} | ConvertTo-Json

$runResp = Invoke-RestMethod -Uri "http://127.0.0.1:8000/graph/run" -Method Post -ContentType "application/json" -Body $runPayload
$runId = $runResp.run_id

# Check execution state (may take a moment)
Start-Sleep -Seconds 2
Invoke-RestMethod -Uri "http://127.0.0.1:8000/graph/state/$runId" -Method Get

Sample Workflow: Code Review (Option A)
Demonstrates a complete workflow with looping and conditional branching:

Extract Functions — Parse code, find functions.
Check Complexity — Calculate lines of code.
Detect Issues — Simulate issue detection.
Suggest Improvements — Calculate quality score.
Loop? — If quality_score >= 80, exit. Else loop back to step 1.
All logic is rule-based; no ML required.

Improvements
Database Persistence: Replace in-memory storage with SQLite/Postgres for durability across restarts.
WebSocket Streaming: Stream step-by-step logs in real-time instead of polling.
Unit & E2E Tests: Pytest suite covering engine logic and API endpoints.
Input Validation: Schema validation for graph creation payloads.
Error Handling: Better error messages and graceful failure recovery.
Authentication: API key or JWT auth if multi-user.
Visualization: Simple UI to draw the graph and see execution in real-time.
Dynamic Node Registration: Allow registering nodes via API, not just decorators.
Tech Stack
FastAPI — Web framework.
Pydantic — Data validation.
Uvicorn — ASGI server.
Python 3.11+
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
