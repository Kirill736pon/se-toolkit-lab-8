#!/usr/bin/env python3
"""
Entrypoint for the nanobot Docker service.

Resolves environment variables into the config at runtime, then launches
the nanobot gateway.

Environment variables read:
- LLM_API_KEY: API key for the LLM provider
- LLM_API_BASE_URL: Base URL for the LLM provider
- LLM_API_MODEL: Model name to use
- NANOBOT_GATEWAY_CONTAINER_ADDRESS: Host address for the gateway
- NANOBOT_GATEWAY_CONTAINER_PORT: Port for the gateway
- NANOBOT_WEBCHAT_CONTAINER_ADDRESS: Host address for webchat
- NANOBOT_WEBCHAT_CONTAINER_PORT: Port for webchat
- NANOBOT_ACCESS_KEY: Access key for WebSocket connections
- NANOBOT_LMS_BACKEND_URL: Backend URL for MCP server
- NANOBOT_LMS_API_KEY: API key for LMS backend
"""

import json
import os
import sys


def main():
    # Paths
    config_path = "/app/nanobot/config.json"
    resolved_path = "/app/nanobot/config.resolved.json"
    workspace_path = "/app/nanobot/workspace"

    # Load the base config
    with open(config_path, "r") as f:
        config = json.load(f)

    # Resolve LLM provider env vars
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base = os.environ.get("LLM_API_BASE_URL")
    llm_api_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config["providers"]["custom"]["api_key"] = llm_api_key
    if llm_api_base:
        config["providers"]["custom"]["api_base"] = llm_api_base
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model

    # Resolve gateway config
    gateway_address = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")

    if "gateway" not in config:
        config["gateway"] = {}
    if gateway_address:
        config["gateway"]["host"] = gateway_address
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)

    # Resolve webchat channel config
    webchat_address = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    access_key = os.environ.get("NANOBOT_ACCESS_KEY")

    if "channels" not in config:
        config["channels"] = {}
    if "webchat" not in config["channels"]:
        config["channels"]["webchat"] = {}

    if webchat_address:
        config["channels"]["webchat"]["host"] = webchat_address
    if webchat_port:
        config["channels"]["webchat"]["port"] = int(webchat_port)
    if access_key:
        config["channels"]["webchat"]["access_key"] = access_key

    # Resolve MCP server env vars
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")

    if "tools" not in config:
        config["tools"] = {}
    if "mcp_servers" in config["tools"]:
        if "lms" in config["tools"]["mcp_servers"]:
            mcp_lms = config["tools"]["mcp_servers"]["lms"]
            # Update args with backend URL if provided
            if lms_backend_url and "args" in mcp_lms:
                # args is like ["python", "-m", "mcp_lms", "http://localhost:42002"]
                # Replace the last arg (URL) with the new one
                mcp_lms["args"][-1] = lms_backend_url
            # Update env with API key if provided
            if lms_api_key and "env" in mcp_lms:
                mcp_lms["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    # Import and run gateway directly from nanobot-ai
    # The venv is already in PATH from Dockerfile ENV
    from nanobot.cli.commands import gateway as gateway_fn
    
    # Call gateway function directly
    gateway_fn(
        port=None,
        workspace=workspace_path,
        verbose=False,
        config=resolved_path
    )


if __name__ == "__main__":
    main()
