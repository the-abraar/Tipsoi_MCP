FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY tipsoi_mcp/ tipsoi_mcp/

RUN pip install --no-cache-dir mcp>=1.2.0 httpx>=0.27 hatchling \
    && pip install --no-cache-dir -e .

ENV TIPSOI_TRANSPORT=http

EXPOSE 8000

CMD ["python3", "-m", "tipsoi_mcp.server"]
