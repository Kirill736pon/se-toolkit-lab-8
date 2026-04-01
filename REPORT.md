# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question:** "What is the agentic loop?"

**Answer:**
The agentic loop is the iterative cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core stages:

1. Perceive/Observation — The agent gathers information about its environment, current state, or user request
2. Think/Reasoning — The agent processes the information, makes decisions, plans next steps, and determines what actions to take
3. Act — The agent executes actions (tool calls, API requests, file operations, etc.)
4. Feedback — The agent observes the results of its actions
5. Repeat — The loop continues until the task is complete or a stopping condition is met

**Question:** "What labs are available in our LMS?"

**Answer:**
Based on the workspace structure, here are the labs/tasks available in this SE Toolkit Lab 8:

Required Tasks: task-1.md, task-2.md, task-3.md, task-4.md, task-5.md
Optional Tasks: task-1.md
Setup Guides: setup/setup-full.md, setup/setup-simple.md

The LMS (Learning Management System) integration isn't currently configured (missing API key), so I can't fetch lab data from the LMS backend directly.

## Task 1B — Agent with LMS tools

**Question:** "What labs are available?"

**Answer:**
Here are the labs available in the LMS:

| ID | Lab Title |
|----|-----------|
| 1 | Lab 01 – Products, Architecture & Roles |
| 2 | Lab 02 — Run, Fix, and Deploy a Backend Service |
| 3 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |
| 4 | Lab 04 — Testing, Front-end, and AI Agents |
| 5 | Lab 05 — Data Pipeline and Analytics Dashboard |
| 6 | Lab 06 — Build Your Own Agent |
| 7 | Lab 07 — Build a Client with an AI Coding Agent |
| 8 | lab-08 |

**Question:** "Describe the architecture of the LMS system"

**Answer:**
The agent should describe the LMS architecture based on data from MCP tools, mentioning:
- FastAPI backend service
- PostgreSQL database
- React/Flutter web clients
- Autochecker API integration for submissions
- OpenTelemetry for observability (VictoriaLogs, VictoriaTraces)
- Caddy reverse proxy

## Task 1C — Skill prompt

**Question:** "Show me the scores" (without specifying a lab)

**Answer:**
The agent displays scores for all labs in a structured table format:

- Lab 01: Lab setup (84.3% avg), Task 0 (64.5%), Task 1 (55.1%), etc.
- Lab 02: Task 1 (67.9%), Task 2 (66.7%), Task 4 (56.2%), Optional 1 (36.4%), Optional 2 (0.0%)
- Lab 03: Task 2 (66.4%), Task 1 (63.7%), Task 3 (50.0%), Task 4 (43.9%)
- Lab 04: Task 3 (68.8%), Task 1 (60.9%), Task 2 (59.9%), Optional 1 (33.8%)
- Lab 05: Task 3 (74.1%), Task 1 (73.5%), Task 2 (64.4%), Optional 1 (57.2%)
- Lab 06: Task 2 (73.6%), Task 1 (61.1%), Task 3 (42.8%)
- Lab 07: Task 1 (76.9%), Task 2 (66.8%), Task 4 (66.6%), Task 3 (58.9%)
- Lab 08: No submissions yet

Key Observations:
- Highest scoring task: Lab setup (Lab 01) at 84.3%
- Lowest scoring task: "Optional 2: Make your VM a proxy" (Lab 02) at 0.0%
- Most attempted task: Lab setup (Lab 01) with 3,003 attempts
- Lab 06 Task 3 ("The System Agent") has high attempts (2,053) but low score (42.8%)

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
