FROM python:3.14-slim

# 1. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

# 2. Copy project files
COPY . .

# 3. Install dependencies using uv
RUN uv sync

# 4. Use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# 5. Run both MCP server (background) and FastAPI (foreground)
CMD ["sh", "-c", "python -m mcp_server.server & uvicorn app.main:app --host 0.0.0.0 --port 8000"]
