import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# MCP Server for Student Success Agent
mcp = FastMCP("StudyPlanServer")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

@mcp.tool()
def save_study_plan(subject: str, duration_days: int, plan_content: str) -> str:
    """Save a student's study plan to disk."""
    plan = {
        "subject": subject,
        "duration_days": duration_days,
        "plan": plan_content,
        "created_at": datetime.now().isoformat()
    }
    filename = f"study_plan_{subject.lower().replace(' ', '_')}.json"
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(plan, f, indent=2)
    return f"Study plan for '{subject}' saved successfully as {filename}"

@mcp.tool()
def load_study_plan(subject: str) -> str:
    """Load a previously saved study plan."""
    filename = f"study_plan_{subject.lower().replace(' ', '_')}.json"
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return f"No study plan found for '{subject}'"
    with open(filepath, "r") as f:
        plan = json.load(f)
    return json.dumps(plan, indent=2)

@mcp.tool()
def list_study_plans() -> str:
    """List all saved study plans."""
    files = [f for f in os.listdir(DATA_DIR) if f.startswith("study_plan_")]
    if not files:
        return "No study plans saved yet."
    return "Saved plans:\n" + "\n".join(files)

if __name__ == "__main__":
    mcp.run(transport="stdio")