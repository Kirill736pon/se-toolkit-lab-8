# Multi-stage build for nanobot gateway service
# Uses uv for dependency management (same pattern as backend/Dockerfile)

ARG REGISTRY_PREFIX_DOCKER_HUB

# ---
# Stage 1: Build the application
# ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy webchat channel packages
COPY --from=webchat pyproject.toml /app/webchat/pyproject.toml
COPY --from=webchat nanobot-channel-protocol /app/webchat/nanobot-channel-protocol
COPY --from=webchat nanobot-webchat /app/webchat/nanobot-webchat

# Copy MCP server from workspace
COPY --from=workspace mcp /app/mcp

# Create Docker-specific nanobot pyproject.toml with correct paths
RUN mkdir -p /app/nanobot && cat > /app/nanobot/pyproject.toml << 'EOF'
[project]
name = "nanobot"
version = "0.1.0"
description = "Nanobot gateway with webchat channel"
requires-python = "==3.14.2"
dependencies = [
    "nanobot-ai",
    "nanobot-webchat",
    "lms-mcp",
]

[tool.uv.sources]
nanobot-webchat = { path = "../webchat/nanobot-webchat", editable = true }
nanobot-channel-protocol = { path = "../webchat/nanobot-channel-protocol", editable = true }
nanobot-ai = { url = "https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip" }
lms-mcp = { path = "../mcp", editable = true }
EOF

# Sync nanobot dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    cd /app/nanobot && uv sync --no-install-workspace

# Copy the rest of nanobot source
COPY entrypoint.py config.json /app/nanobot/

# ---
# Stage 2: Runtime image
# ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Setup non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy application from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Add venv to PATH
ENV PATH="/app/nanobot/.venv/bin:$PATH"
ENV PYTHONPATH="/app/nanobot"

USER nonroot
WORKDIR /app

CMD ["python", "/app/nanobot/entrypoint.py"]
