from typing import Callable, Dict

# Global registry to look up functions by string name
NODE_REGISTRY: Dict[str, Callable] = {}
TOOL_REGISTRY: Dict[str, Callable] = {}

def register_node(name: str):
    """Decorator to register a function as a usable workflow node."""
    def decorator(func):
        NODE_REGISTRY[name] = func
        return func
    return decorator

def register_tool(name: str):
    """Decorator to register a helper tool."""
    def decorator(func):
        TOOL_REGISTRY[name] = func
        return func
    return decorator

# --- Simple Tool Implementations ---

@register_tool("count_loc")
def count_lines_of_code(code: str) -> int:
    return len(code.split('\n'))

@register_tool("check_syntax")
def check_syntax_rules(code: str) -> int:
    # Dummy logic: assumes 'TODO' is a syntax warning
    return code.count("TODO")