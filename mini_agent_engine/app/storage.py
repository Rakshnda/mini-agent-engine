# Simple in-memory storage
from typing import Dict, Any

class InMemoryStore:
    def __init__(self):
        self.graphs = {} # graph_id -> Graph Definition
        self.runs = {}   # run_id -> {status, state, logs}

    def save_graph(self, graph_id, graph_obj):
        self.graphs[graph_id] = graph_obj

    def get_graph(self, graph_id):
        return self.graphs.get(graph_id)

    def create_run(self, run_id):
        self.runs[run_id] = {"status": "running", "state": {}, "logs": []}

    def update_run(self, run_id, status, state, logs):
        self.runs[run_id] = {"status": status, "state": state, "logs": logs}
    
    def get_run(self, run_id):
        return self.runs.get(run_id)

db = InMemoryStore()