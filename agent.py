# =============================================================================
# Student Success Agent - Main Entry Point
# Multi-agent system built with Google ADK for Kaggle AI Agents Capstone
# Track: Agents for Good
# =============================================================================

import sys
import os

# Add project root to path so local modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

# Google ADK - core agent framework
from google.adk.agents import Agent

# MCP toolset - connects agents to external tools via Model Context Protocol
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# Custom progress tracking skill - handles persistent study progress
from skills.progress_tracker import mark_day_complete, load_progress, set_total_days

# =============================================================================
# PLANNER AGENT
# Responsibility: Create personalized study plans and exam schedules
# MCP Integration: Saves/loads study plans to disk via custom MCP server
# =============================================================================
planner_agent = Agent(
    name="planner_agent",
    model="gemini-2.0-flash",  # Flash model for better quota and speed
    description="Creates study plans and exam schedules.",
    instruction="""You are a Study Planner Agent.
ALWAYS start your response with: [PLANNER AGENT]

Help students create study schedules, prepare for exams, organize subjects, and suggest revision plans.
When you create a study plan, use the save_study_plan tool to save it.
Give practical and realistic plans.""",
    tools=[
        # MCPToolset connects to external study plan server via stdio transport
        # This enables persistent storage of study plans across sessions
        MCPToolset(
            connection_params=StdioServerParameters(
                command="python",
                args=["mcp/study_plan_server.py"],  # Custom FastMCP server
            )
        )
    ],
)

# =============================================================================
# LEARNING AGENT
# Responsibility: Explain academic concepts and answer subject questions
# Design: Stateless agent - no tools needed, uses LLM knowledge directly
# =============================================================================
learning_agent = Agent(
    name="learning_agent",
    model="gemini-2.0-flash",
    description="Explains academic concepts and answers learning questions.",
    instruction="""You are a Learning Agent.
ALWAYS begin your response with: [LEARNING AGENT]

Help students understand concepts, explain topics clearly, answer academic questions, and give examples.
Be educational, clear, and beginner-friendly."""
)

# =============================================================================
# RESOURCE AGENT
# Responsibility: Recommend books, websites, and learning materials
# Design: Stateless agent - uses LLM knowledge to suggest resources
# =============================================================================
resource_agent = Agent(
    name="resource_agent",
    model="gemini-2.0-flash",
    description="Finds learning resources for students.",
    instruction="""You are a Resource Agent.
ALWAYS begin your response with: [RESOURCE AGENT]

Help students find books, practice questions, websites, and learning materials.
Recommend high-quality educational resources."""
)

# =============================================================================
# PROGRESS AGENT
# Responsibility: Track study completion and motivate students
# Tools: Custom function tools backed by progress.json for persistence
# =============================================================================
progress_agent = Agent(
    name="progress_agent",
    model="gemini-2.0-flash",
    description="Tracks student progress and motivates learning.",
    instruction="""You are a Progress Agent.
ALWAYS begin your response with: [PROGRESS AGENT]

Help students track study progress and stay motivated.

When a student says they completed a day:
1. Use mark_day_complete tool to update their progress
2. Show them their completion percentage
3. Encourage them to keep going

When a student asks for their progress:
1. Use load_progress tool to get current status
2. Show completed days and percentage""",
    tools=[
        mark_day_complete,  # Marks a study day complete, updates progress.json
        load_progress,      # Loads current progress from progress.json
        set_total_days,     # Sets the total number of study days for a plan
    ]
)

# =============================================================================
# ROOT AGENT (Coordinator)
# Responsibility: Receive all student requests and delegate to right agent
# Behavior: Never answers directly - always routes to a specialist
# Sub-agents: planner, learning, resource, progress
# =============================================================================
root_agent = Agent(
    name="student_success_agent",
    model="gemini-2.0-flash",
    description="A multi-agent system that helps students succeed academically.",
    instruction="""You are the Student Success Agent coordinator.

ALWAYS delegate to the right specialized agent — never answer directly yourself.

- Study plans, schedules, exam prep → planner_agent
- Concept explanations, learning questions → learning_agent
- Books, websites, resources → resource_agent
- Progress tracking, motivation → progress_agent""",
    # Sub-agents registered here enable ADK's automatic delegation
    sub_agents=[planner_agent, learning_agent, resource_agent, progress_agent],
)