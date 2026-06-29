# Tipsoi-flavored Gemini proxy (drop-in google-genai compatible).
FROM python:3.12-slim
WORKDIR /app
COPY tipsoi_support_mcp/ ./tipsoi_support_mcp/
COPY gateway/ ./gateway/
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" httpx
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "uvicorn gateway.gemini_proxy:app --host 0.0.0.0 --port ${PORT}"]
