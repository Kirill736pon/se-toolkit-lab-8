"""MCP server exposing VictoriaLogs and VictoriaTraces observability tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import quote

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("observability")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_VICTORIALOGS_URL: str = ""
_VICTORIATRACES_URL: str = ""

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _NoArgs(BaseModel):
    """Empty input model for tools that don't need arguments."""


class _LogsSearchQuery(BaseModel):
    query: str = Field(
        default="*",
        description="LogsQL query. Use _stream:{service.name=\"backend\"} to filter by service. Use level:error for errors.",
    )
    limit: int = Field(default=10, ge=1, le=100, description="Max log entries to return.")
    start: str = Field(
        default="5m",
        description="Start time: RFC3339 timestamp or relative like '5m', '1h', '1d'.",
    )


class _LogsErrorCountQuery(BaseModel):
    start: str = Field(
        default="1h",
        description="Time window: '5m', '1h', '1d', etc.",
    )


class _TracesListQuery(BaseModel):
    service: str = Field(
        default="Learning Management Service",
        description="Service name to filter traces.",
    )
    limit: int = Field(default=5, ge=1, le=50, description="Max traces to return.")


class _TraceIdQuery(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch full details.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _text(data: Any) -> list[TextContent]:
    """Serialize data to JSON text."""
    if isinstance(data, (dict, list)):
        content = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        content = str(data)
    return [TextContent(type="text", text=content)]


async def _get_victorialogs(path: str, params: dict[str, Any] | None = None) -> Any:
    """Make GET request to VictoriaLogs API."""
    url = f"{_VICTORIALOGS_URL}{path}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        # VictoriaLogs returns NDJSON or JSON
        content = response.text.strip()
        if content.startswith("[") or content.startswith("{"):
            return json.loads(content)
        # Parse NDJSON
        lines = content.split("\n")
        results = []
        for line in lines:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    results.append({"_msg": line})
        return results


async def _get_victoriatraces(path: str, params: dict[str, Any] | None = None) -> Any:
    """Make GET request to VictoriaTraces API (Jaeger-compatible)."""
    url = f"{_VICTORIATRACES_URL}{path}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsSearchQuery) -> list[TextContent]:
    """Search logs using VictoriaLogs."""
    result = await _get_victorialogs(
        "/select/logsql/query",
        params={
            "query": args.query,
            "limit": args.limit,
            "start": args.start,
        },
    )
    return _text(result)


async def _logs_error_count(args: _LogsErrorCountQuery) -> list[TextContent]:
    """Count errors per service over a time window."""
    query = f'level:error | stats by(service.name) count() | sort by(_time:desc) | limit 10'
    result = await _get_victorialogs(
        "/select/logsql/stats_query",
        params={
            "query": query,
            "start": args.start,
        },
    )
    return _text(result)


async def _logs_recent_errors(_args: _NoArgs) -> list[TextContent]:
    """Get recent error logs from all services."""
    query = 'level:error | sort by(_time:desc) | limit 20'
    result = await _get_victorialogs(
        "/select/logsql/query",
        params={
            "query": query,
            "limit": 20,
            "start": "1h",
        },
    )
    return _text(result)


async def _traces_list(args: _TracesListQuery) -> list[TextContent]:
    """List recent traces for a service."""
    result = await _get_victoriatraces(
        "/jaeger/api/traces",
        params={
            "service": args.service,
            "limit": args.limit,
        },
    )
    # Extract summary info
    traces = result.get("data", [])
    summary = []
    for trace in traces[: args.limit]:
        summary.append(
            {
                "trace_id": trace.get("traceID"),
                "spans": len(trace.get("spans", [])),
                "start_time": trace.get("startTime"),
                "duration": trace.get("duration"),
            }
        )
    return _text(summary)


async def _traces_get(args: _TraceIdQuery) -> list[TextContent]:
    """Fetch full trace details by ID."""
    result = await _get_victoriatraces(f"/jaeger/api/traces/{args.trace_id}")
    # Extract span hierarchy
    traces = result.get("data", [])
    if not traces:
        return _text({"error": f"Trace {args.trace_id} not found"})
    
    trace = traces[0]
    spans = trace.get("spans", [])
    hierarchy = []
    for span in spans:
        hierarchy.append(
            {
                "span_id": span.get("spanID"),
                "operation": span.get("operationName"),
                "service": span.get("process", {}).get("serviceName"),
                "duration": span.get("duration"),
                "tags": span.get("tags", []),
                "logs": span.get("logs", []),
            }
        )
    return _text({"trace_id": trace.get("traceID"), "spans": hierarchy})


async def _traces_errors(_args: _NoArgs) -> list[TextContent]:
    """Find traces with errors."""
    # Search for traces containing error tags
    result = await _get_victoriatraces(
        "/jaeger/api/traces",
        params={"service": "Learning Management Service", "limit": 10},
    )
    traces = result.get("data", [])
    error_traces = []
    for trace in traces:
        for span in trace.get("spans", []):
            for tag in span.get("tags", []):
                if tag.get("key") == "error" or "error" in str(tag.get("value", "")).lower():
                    error_traces.append(
                        {
                            "trace_id": trace.get("traceID"),
                            "span": span.get("operationName"),
                            "service": span.get("process", {}).get("serviceName"),
                        }
                    )
                    break
    return _text(error_traces[:10])


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (model, handler, Tool(name=name, description=description, inputSchema=schema))


_register(
    "logs_search",
    "Search logs in VictoriaLogs using LogsQL. Use query='*' for all logs, 'level:error' for errors. Filter by service: _stream:{service.name=\"backend\"}.",
    _LogsSearchQuery,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count errors per service over a time window. Returns stats grouped by service name.",
    _LogsErrorCountQuery,
    _logs_error_count,
)
_register(
    "logs_recent_errors",
    "Get the 20 most recent error logs from all services in the last hour.",
    _NoArgs,
    _logs_recent_errors,
)
_register(
    "traces_list",
    "List recent traces for a service. Returns trace ID, span count, and duration.",
    _TracesListQuery,
    _traces_list,
)
_register(
    "traces_get",
    "Fetch full trace details by trace ID. Returns span hierarchy with operation names, services, and durations.",
    _TraceIdQuery,
    _traces_get,
)
_register(
    "traces_errors",
    "Find traces containing errors. Returns trace IDs and span info for traces with error tags.",
    _NoArgs,
    _traces_errors,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    global _VICTORIALOGS_URL, _VICTORIATRACES_URL
    _VICTORIALOGS_URL = os.environ.get("VICTORIALOGS_URL", "http://localhost:42010").rstrip("/")
    _VICTORIATRACES_URL = os.environ.get("VICTORIATRACES_URL", "http://localhost:42011").rstrip("/")
    
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
