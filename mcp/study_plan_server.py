# =============================================================================
# Study Plan MCP Server
# Built with FastMCP - provides persistent study plan storage for Planner Agent
# Transport: stdio (called by ADK via StdioServerParameters)
# =============================================================================

import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with a named instance
# This name appears in ADK's agent graph as "MCPToolset"
mcp = FastMCP("StudyPlanServer")

# Store all study plans in the project's data/ directory
# Using relative path from this file's location for portability
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)  # Create data/ if it doesn't exist

# =============================================================================
# TOOL: save_study_plan
# Called by Planner Agent after creating a study schedule
# Persists plan as JSON so it can be retrieved in future sessions
# =============================================================================
@mcp.tool()
def save_study_plan(subject: str, duration_days: int, plan_content: str) -> str:
    """Save a student's study plan to disk."""
    # Structure the plan with metadata for future retrieval
    plan = {
        "subject": subject,
        "duration_days": duration_days,
        "plan": plan_content,
        "created_at": datetime.now().isoformat()  # Timestamp for tracking
    }
    # Filename derived from subject for easy lookup
    filename = f"study_plan_{subject.lower().replace(' ', '_')}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    # Write plan to disk as formatted JSON
    with open(filepath, "w") as f:
        json.dump(plan, f, indent=2)
    
    return f"Study plan for '{subject}' saved successfully as {filename}"

# =============================================================================
# TOOL: load_study_plan
# Called when student asks to review a previously created plan
# Enables cross-session memory for the agent
# =============================================================================
@mcp.tool()
def load_study_plan(subject: str) -> str:
    """Load a previously saved study plan."""
    filename = f"study_plan_{subject.lower().replace(' ', '_')}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    # Handle case where no plan exists for the subject
    if not os.path.exists(filepath):
        return f"No study plan found for '{subject}'"
    
    with open(filepath, "r") as f:
        plan = json.load(f)
    
    return json.dumps(plan, indent=2)

# =============================================================================
# TOOL: list_study_plans
# Lists all saved plans - useful for students to see what they've created
# =============================================================================
@mcp.tool()
def list_study_plans() -> str:
    """List all saved study plans."""
    # Filter only study plan files in data/ directory
    files = [f for f in os.listdir(DATA_DIR) if f.startswith("study_plan_")]
    
    if not files:
        return "No study plans saved yet."
    
    return "Saved plans:\n" + "\n".join(files)

# =============================================================================
# Entry point - runs MCP server with stdio transport
# ADK connects to this server via StdioServerParameters in agent.py
# =============================================================================
if __name__ == "__main__":
    mcp.run(transport="stdio")