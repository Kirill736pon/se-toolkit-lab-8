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

### User asks about errors
1. First call `logs_recent_errors()` to get actual error entries
2. **Always show the actual data** — include timestamps, service names, error messages
3. If errors found, also call `logs_error_count(start="1h")` to show counts per service
4. **Quote specific error messages** from the logs

### User asks about service health
1. Call `logs_search(query="_stream:{service.name=\"backend\"}", limit=10)` 
2. Show actual log entries with timestamps and events

### User asks "what went wrong?"
1. Call `logs_recent_errors()` — show the actual error messages
2. Call `traces_errors()` — show trace IDs and failing spans
3. For each error trace, call `traces_get(trace_id)` — show the full span hierarchy
4. **Report specific details**: trace IDs, operation names, services, error messages

## Response Style

- **Show real data** — include actual values from tool responses
- **Quote error messages** — copy exact error text from logs
- **Include trace IDs** — when showing traces, include the actual trace_id values
- **Show counts** — when available, include numeric counts from stats queries
- **Be specific** — name specific services, operations, timestamps
- **Don't just summarize** — include raw data excerpts alongside summary

## Example Flow with Real Data

User: "Any errors in the last hour?"

You (call logs_recent_errors, get actual data):
```
Yes, I found 3 errors in the last hour:

**Error count by service:**
- Learning Management Service: 2 errors
- Backend: 1 error

**Recent errors:**
1. [2026-04-01T12:11:02Z] Learning Management Service: "socket.gaierror: [Errno -2] Name or service not known"
2. [2026-04-01T12:10:45Z] Backend: "Connection refused to postgres:5432"
3. [2026-04-01T12:09:30Z] Learning Management Service: "HTTP 500 Internal Server Error"

**Error traces found:**
- Trace ID: abc123def456... (span: db_query, service: Learning Management Service)
- Trace ID: 789xyz012... (span: request_completed, service: Backend)
```

User: "What went wrong with the backend?"

You (call traces_get with actual trace_id):
```
I found the failure in trace `abc123def456...`:

**Span hierarchy:**
1. request_started (Learning Management Service) — 0ms
2. auth_success (Learning Management Service) — 5ms  
3. db_query (Learning Management Service) — ERROR
   - Error: "socket.gaierror: [Errno -2] Name or service not known"
   - Duration: 1000ms (timeout)
4. request_completed (Learning Management Service) — 500 status

**Root cause:** PostgreSQL database is unreachable. The db_query span failed because the service couldn't resolve the hostname 'postgres'.
```
