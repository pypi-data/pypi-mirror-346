FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv && \
    uv pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "mcp_server_neo4j"] 