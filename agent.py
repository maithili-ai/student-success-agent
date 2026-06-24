import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from skills.progress_tracker import mark_day_complete, load_progress, set_total_days

planner_agent = Agent(
    name="planner_agent",
    model="gemini-2.0-flash",
    description="Creates study plans and exam schedules.",
    instruction="""You are a Study Planner Agent.
ALWAYS start your response with: [PLANNER AGENT]

Help students create study schedules, prepare for exams, organize subjects, and suggest revision plans.
When you create a study plan, use the save_study_plan tool to save it.
Give practical and realistic plans.""",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="python",
                args=["mcp/study_plan_server.py"],
            )
        )
    ],
)

learning_agent = Agent(
    name="learning_agent",
    model="gemini-2.0-flash",
    description="Explains academic concepts and answers learning questions.",
    instruction="""You are a Learning Agent.
ALWAYS begin your response with: [LEARNING AGENT]

Help students understand concepts, explain topics clearly, answer academic questions, and give examples.
Be educational, clear, and beginner-friendly."""
)

resource_agent = Agent(
    name="resource_agent",
    model="gemini-2.0-flash",
    description="Finds learning resources for students.",
    instruction="""You are a Resource Agent.
ALWAYS begin your response with: [RESOURCE AGENT]

Help students find books, practice questions, websites, and learning materials.
Recommend high-quality educational resources."""
)

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
        mark_day_complete,
        load_progress,
        set_total_days,
    ]
)

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
    sub_agents=[planner_agent, learning_agent, resource_agent, progress_agent],
)