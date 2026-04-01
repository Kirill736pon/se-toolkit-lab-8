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
  - **Returns**: JSON with error counts grouped by service

- `logs_recent_errors()` — Get 20 most recent errors from all services
  - **Returns**: Array of error log entries with timestamps, service names, and error messages

### Trace Tools (VictoriaTraces)

- `traces_list(service, limit)` — List recent traces for a service
  - **Returns**: Array of trace summaries with trace_id, span count, duration

- `traces_get(trace_id)` — Fetch full trace details with span hierarchy
  - **Returns**: Full trace with all spans, operations, services, durations, tags, and logs

- `traces_errors()` — Find traces containing errors
  - **Returns**: Array of error traces with trace_id, span operation, service name

## When to Use

### User asks "What went wrong?" or "Check system health"
1. Call `logs_recent_errors()` first to get actual error entries
2. **Show the actual data** — include timestamps, service names, error messages
3. If errors found, call `traces_errors()` to find related traces
4. For each error trace, call `traces_get(trace_id)` to see the full span hierarchy
5. **Chain the investigation**: logs → traces → root cause
6. **Report specific details**: trace IDs, operation names, services, error messages
7. **Summarize concisely** — don't dump raw JSON, explain what failed and why

### User asks about errors
1. Call `logs_recent_errors()` to get actual error entries
2. **Always show the actual data** — include timestamps, service names, error messages
3. If errors found, also call `logs_error_count(start="1h")` to show counts per service
4. **Quote specific error messages** from the logs

### User asks about service health
1. Call `logs_search(query="_stream:{service.name=\"backend\"}", limit=10)` 
2. Show actual log entries with timestamps and events

## Response Style

- **Show real data** — include actual values from tool responses
- **Quote error messages** — copy exact error text from logs
- **Include trace IDs** — when showing traces, include the actual trace_id values
- **Show counts** — when available, include numeric counts from stats queries
- **Be specific** — name specific services, operations, timestamps
- **Chain investigations** — logs → traces → root cause analysis
- **Don't just summarize** — include raw data excerpts alongside summary
- **Be concise** — explain findings clearly without dumping full JSON

## Example Flow: "What went wrong?"

User: "What went wrong?"

You (investigate step by step):
1. Call `logs_recent_errors()` — find error at 2026-04-01T12:54:54Z
2. Extract trace_id: `1291c78fc8c9fae9319ec5ef6d0d9c8d`
3. Call `traces_get("1291c78fc8c9fae9319ec5ef6d0d9c8d")` — see span hierarchy
4. Report:

```
I found the failure:

**Log evidence:**
- [2026-04-01T12:54:54Z] ERROR in Learning Management Service: "socket.gaierror: [Errno -2] Name or service not known"
- Trace ID: 1291c78fc8c9fae9319ec5ef6d0d9c8d

**Trace evidence:**
- Span: db_query (Learning Management Service) — FAILED
- Duration: 1000ms (timeout)
- Error tag: true

**Root cause:**
PostgreSQL database is unreachable. The service cannot resolve hostname 'postgres'.
```
