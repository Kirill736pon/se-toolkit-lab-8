# Observability Skill

You have access to observability tools for querying VictoriaLogs and VictoriaTraces.

## Available Tools

### Log Tools (VictoriaLogs)

- `logs_search(query, limit, start)` — Search logs using LogsQL
  - `query`: Use `*` for all logs, `level:error` for errors
  - Filter by service: `_stream:{service.name="backend"}`
  - Example: `_stream:{service.name="backend"} AND level:error`
  
- `logs_error_count(start)` — Count errors per service over time window
  - `start`: Time window like `5m`, `1h`, `1d`
  
- `logs_recent_errors()` — Get 20 most recent errors from all services

### Trace Tools (VictoriaTraces)

- `traces_list(service, limit)` — List recent traces for a service
- `traces_get(trace_id)` — Fetch full trace details with span hierarchy
- `traces_errors()` — Find traces containing errors

## When to Use

### User asks about errors
1. First call `logs_recent_errors()` or `logs_search(query="level:error", start="1h")`
2. If you find errors, summarize them concisely
3. If errors mention a trace ID, call `traces_get(trace_id)` for details

### User asks about service health
1. Call `logs_search(query="_stream:{service.name=\"backend\"}", limit=5)` to see recent activity
2. Check for error patterns in the logs

### User asks "what went wrong?"
1. Call `logs_recent_errors()` to find recent failures
2. Call `traces_errors()` to find error traces
3. For any error trace, call `traces_get(trace_id)` to see the span hierarchy
4. Identify the failing service and operation from the trace

## Response Style

- **Be concise** — summarize findings, don't dump raw JSON
- **Highlight errors** — mention service names, error messages, timestamps
- **Trace hierarchy** — explain which service failed and at what step
- **Actionable** — suggest what might need fixing

## Example Flow

User: "Any errors in the last hour?"

You:
1. Call `logs_recent_errors()`
2. If results show errors: "Yes, I found X errors. The backend service had database connection failures..."
3. If no errors: "No errors found in the last hour. All services appear healthy."

User: "What went wrong with the backend?"

You:
1. Call `logs_search(query="_stream:{service.name=\"backend\"} AND level:error", start="1h")`
2. Call `traces_errors()`
3. For each error trace, call `traces_get(trace_id)`
4. Summarize: "The backend failed at the db_query step due to PostgreSQL connection timeout..."
