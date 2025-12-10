import random
from app.registry import register_node, TOOL_REGISTRY, register_tool

# -- Tool Definitions --

@register_tool("count_loc")
def count_loc(code: str) -> int:
    """Count lines of code."""
    return len(code.split("\n"))

# -- Router Logic --
def quality_gate_router(state: dict) -> str:
    """Decides whether to loop back or finish."""
    if state.get("quality_score", 0) >= 80:
        return "__END__"
    
    if state.get("iterations", 0) >= 3:
        state["final_note"] = "Max iterations reached. Stopping."
        return "__END__"
    
    return "extract_functions" # Loop back to start

# -- Nodes --

@register_node("extract_functions")
def node_extract(state: dict) -> dict:
    state["iterations"] = state.get("iterations", 0) + 1
    # Simulate work
    state["functions_found"] = ["func_a", "func_b"]
    return state

@register_node("check_complexity")
def node_complexity(state: dict) -> dict:
    code = state.get("code", "")
    # Use a tool from registry
    loc = TOOL_REGISTRY["count_loc"](code)
    state["complexity_score"] = loc * 0.5 # Dummy calc
    return state

@register_node("detect_issues")
def node_issues(state: dict) -> dict:
    # Randomly find issues
    issues_count = random.randint(0, 5)
    state["issues_found"] = issues_count
    return state

@register_node("suggest_improvements")
def node_improve(state: dict) -> dict:
    # Calculate a quality score
    issues = state.get("issues_found", 0)
    complexity = state.get("complexity_score", 0)
    
    # Simple scoring logic (0-100)
    # Each iteration, we pretend to 'fix' things by artificially boosting score
    base_score = 100 - (issues * 10) - complexity
    
    # Improve score per iteration to ensure loop eventually terminates
    boost = state["iterations"] * 10
    final_score = min(100, max(0, base_score + boost))
    
    state["quality_score"] = final_score
    state["suggestion"] = "Refactor logic" if final_score < 80 else "LGTM"
    
    return state