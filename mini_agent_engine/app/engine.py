import asyncio
from typing import Callable, Dict, Any, Optional

class WorkflowEngine:
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.nodes: Dict[str, Callable] = {}
        self.edges: Dict[str, str] = {}  # simple map: from -> to
        self.conditional_edges: Dict[str, Callable] = {} # from -> routing_function
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable):
        """Register a node (function) to the graph."""
        self.nodes[name] = func

    def set_entry_point(self, node_name: str):
        self.entry_point = node_name

    def add_edge(self, start_node: str, end_node: str):
        """Add a static edge."""
        self.edges[start_node] = end_node

    def add_conditional_edge(self, start_node: str, router_func: Callable):
        """
        Add a dynamic edge. The router_func(state) returns the name 
        of the next node or "__END__".
        """
        self.conditional_edges[start_node] = router_func

    async def run(self, initial_state: Dict[str, Any], log_callback=None):
        """Executes the graph until __END__ or no edges remain."""
        state = initial_state.copy()
        current_node = self.entry_point
        execution_log = []

        if not current_node:
            raise ValueError("No entry point defined.")

        step_count = 0
        MAX_STEPS = 20  # Safety guardrail against infinite loops

        while current_node and current_node != "__END__" and step_count < MAX_STEPS:
            # 1. Execute Node
            node_func = self.nodes.get(current_node)
            if not node_func:
                break

            # Log execution
            log_entry = {"step": step_count, "node": current_node}
            execution_log.append(log_entry)
            if log_callback:
                await log_callback(current_node, state)
            
            # Run the node (support sync or async)
            if asyncio.iscoroutinefunction(node_func):
                state = await node_func(state)
            else:
                state = node_func(state)

            step_count += 1

            # 2. Determine Next Node
            # Check conditional edges first
            if current_node in self.conditional_edges:
                router = self.conditional_edges[current_node]
                next_node = router(state)
                current_node = next_node
            # Check static edges
            elif current_node in self.edges:
                current_node = self.edges[current_node]
            else:
                current_node = "__END__"

        return state, execution_log