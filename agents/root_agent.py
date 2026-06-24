from google.adk.agents import Agent

from agents.planner_agent import planner_agent
from agents.learning_agent import learning_agent
from agents.resource_agent import resource_agent
from agents.progress_agent import progress_agent

root_agent = Agent(
    name="student_success_agent",
    description="A multi-agent system that helps students succeed academically.",
    instruction="""
You are the Student Success Agent.

You MUST delegate tasks to the appropriate specialized agent.

Use Planner Agent for:
- study plans
- schedules
- exam preparation

Use Learning Agent for:
- explanations
- concepts
- teaching

Use Resource Agent for:
- books
- websites
- learning materials

Use Progress Agent for:
- progress tracking
- motivation
- study habits

Never answer directly if a specialized agent can handle the task.
Always transfer the task to the best matching agent.
""",
    sub_agents=[
        planner_agent,
        learning_agent,
        resource_agent,
        progress_agent,
    ],
)