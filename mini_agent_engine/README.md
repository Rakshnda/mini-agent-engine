# Mini Agent Workflow Engine

A simplified graph-based workflow engine (inspired by LangGraph) built with FastAPI. It supports nodes, shared state, conditional branching, loops, and async execution.

## Features
- **Nodes**: Python functions modifying state.
- **Edges**: Static and Conditional (branching/looping).
- **Tools**: Simple registry pattern.
- **API**: Create graphs, trigger background runs, check state.

## Folder Structure
- `app/engine.py`: Core graph execution logic.
- `app/workflows/`: Contains the sample "Code Review" agent logic.
- `app/registry.py`: Where nodes and tools are registered.

## How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt