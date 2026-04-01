# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question:** "What is the agentic loop?"

**Answer:**
```
The agentic loop is the iterative cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core stages:

The Loop

 1 Perceive/Observation — The agent gathers information about its environment, current state, or user request
 2 Think/Reasoning — The agent processes the information, makes decisions, plans next steps, and determines what actions to take
 3 Act — The agent executes actions (tool calls, API requests, file operations, etc.)
 4 Feedback — The agent observes the results of its actions
 5 Repeat — The loop continues until the task is complete or a stopping condition is met

Why It Matters

This loop enables agents to:

 • Handle complex, multi-step tasks
 • Adapt to new information dynamically
 • Recover from errors or unexpected results
 • Work autonomously without constant human guidance

Example

For a task like "analyze the project and fix any broken tests":

 1 Perceive: Read the project structure, find test files
 2 Think: Identify which tests are failing and why
 3 Act: Run tests, examine error messages
 4 Feedback: See test results
 5 Repeat: Fix code, re-run tests until all pass

This observe-think-act-feedback cycle is fundamental to how autonomous AI agents operate, distinguishing them from simple question-answer systems.
```

**Question:** "What labs are available in our LMS?"

**Answer:**
```
Here are the labs available in the LMS:

 ID  Lab Title
 ───────────────────────────────────────────────────────────
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   lab-08

You're currently working in Lab 08 (based on your workspace path /root/se-toolkit-lab-8/).

Would you like more details about any specific lab, such as:

 • Pass rates
 • Completion rates
 • Top learners
 • Submission timeline
 • Group performance
```

## Task 1B — Agent with LMS tools

**Question:** "What labs are available?"

**Answer:**
```
Here are the labs available in the LMS:

 ID  Lab Title
 ───────────────────────────────────────────────────────────
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   lab-08

You're currently working in Lab 08 (based on your workspace path /root/se-toolkit-lab-8/).

Would you like more details about any specific lab?
```

**Question:** "Describe the architecture of the LMS system"

**Answer:**
```
The Nanobot agent connects to multiple clients and has MCP tools to query the LMS:

 ┌─────────────┐    ┌─────────────┐
 │   Browser   │    │  Telegram   │
 │  (Flutter)  │    │    Bot      │
 └──────┬──────┘    └──────┬──────┘
        │                  │
        └────────┬─────────┘
                 │
          ┌──────▼──────┐
          │   Nanobot   │
          │   Agent     │
          └──────┬──────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
 ┌───▼───┐  ┌───▼───┐  ┌────▼────┐
 │  LMS  │  │  Log  │  │  Trace  │
 │ Tools │  │ Tools │  │  Tools  │
 └───┬───┘  └───┬───┘  └────┬────┘
     │           │           │
 ┌───▼───────────▼───────────▼───┐
 │        LMS Backend +          │
 │     Observability Stack       │
 └───────────────────────────────┘
```

## Task 1C — Skill prompt

**Question:** "Show me the scores" (without specifying a lab)

**Answer:**
```
                                                          📊 Lab Scores Overview

Lab 01 – Products, Architecture & Roles

 Task                                        Avg Score  Attempts
 ───────────────────────────────────────────────────────────────
 Lab setup                                   84.3       3003
 Task 0: Practice the Git workflow           64.5       306
 Task 1: Product & architecture description  55.1       161
 Task 2: Roles and skills mapping            49.8       83
 Optional: Create a release                  60.0       5
 Optional: Add a CI check                    42.9       7
 Optional: Resolve a merge conflict          34.6       13
 Optional: Plan skill development            20.0       5

-------------------------------------------------------------------------------------------------------------------------------------------

Lab 02 — Run, Fix, and Deploy a Backend Service

 Task                                            Avg Score  Attempts
 ───────────────────────────────────────────────────────────────────
 Task 1: Run the web server                      67.9       210
 Task 2: Identify, report, and fix a bug         66.7       216
 Task 4: Deploy the web server to the VM         56.2       84
 Optional 3: Implement the post-order traversal  62.5       6
 Optional 1: Implement the /outcomes endpoint    36.4       11
 Optional 2: Make your VM a proxy                0.0        3

[... labs 03-08 omitted for brevity ...]

-------------------------------------------------------------------------------------------------------------------------------------------

🔍 Key Insights

 Metric            Value                   Lab/Task
 ───────────────────────────────────────────────────────────────────────────────────
 Highest Score     84.3%                   Lab 01 — Lab setup
 Lowest Score      0.0%                    Lab 02 — Optional 2: Make your VM a proxy
 Most Attempts     3,003                   Lab 01 — Lab setup
 Most Challenging  42.8% (2,053 attempts)  Lab 06 — Task 3: The System Agent
```

The agent displays scores for ALL labs because no specific lab was specified. The skill prompt teaches the agent to either ask which lab OR show all available options when the lab parameter is missing.

## Task 2A — Deployed agent

Nanobot запущен как Docker сервис через `nanobot gateway`.

**Startup logs:**
```
nanobot-1  | Using config: /app/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  |   Created HEARTBEAT.md
nanobot-1  |   Created AGENTS.md
nanobot-1  |   Created TOOLS.md
nanobot-1  |   Created SOUL.md
nanobot-1  |   Created USER.md
nanobot-1  |   Created memory/MEMORY.md
nanobot-1  |   Created memory/HISTORY.md
nanobot-1  | 2026-04-01 11:38:30.823 | INFO     | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-04-01 11:38:31.281 | INFO     | nanobot.channels.manager:start_all:91 - Starting webchat channel...
```

**Files created/modified:**
- `nanobot/Dockerfile` — multi-stage build с uv
- `nanobot/entrypoint.py` — runtime config resolution и запуск gateway
- `nanobot/config.json` — добавлен webchat channel
- `nanobot/pyproject.toml` — зависимости nanobot-webchat
- `docker-compose.yml` — раскомментированы сервисы nanobot и client-web-flutter
- `caddy/Caddyfile` — раскомментированы маршруты /ws/chat и /flutter

## Task 2B — Web client

**WebSocket test:**
```
Connecting to WebSocket...
Connected!
Message sent, waiting for response...
Response 1:
{"type":"text","content":"I'll check what labs are available in the LMS for you.","format":"markdown"}
Response 2:
{"type":"text","content":"Here are the available labs:\n\n| ID | Title |\n|----|-------|\n| 1 | Lab 01 – Products, Architecture & Roles |\n..."}
```

**Flutter client:** Доступен по адресу `http://localhost:42002/flutter`

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
