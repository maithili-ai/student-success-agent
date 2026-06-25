# Student Success Agent - Project Plan

## Track
Agents for Good

## Status
✅ 100% Complete

## Problem Statement
Students often struggle to manage multiple subjects, exams,
deadlines, study schedules, and learning resources.

Student Success Agent uses a multi-agent system to help
students plan, learn, discover resources, and track progress.

## Agents Built

### Root Agent
Routes requests to specialist agents using ADK delegation.

### Planner Agent
Creates study schedules and exam plans.
Connected to MCP server for persistent study plan storage.

### Learning Agent
Explains academic concepts clearly and gives examples.

### Resource Agent
Finds books, websites, and learning materials.

### Progress Agent
Tracks study progress with completion percentage.
Tools: mark_day_complete, load_progress, set_total_days.

## MCP Integration
- Custom MCP server (study_plan_server.py)
- Saves and loads study plans as JSON files
- Connected to planner_agent via MCPToolset

## Security
- Prompt injection detection and blocking
- Input length validation (max 1000 chars)
- Harmful content filtering
- Empty input handling

## Course Concepts Demonstrated
- ADK Multi-Agent System
- MCP Server
- Agent Skills (progress tracker)
- Security Features