FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml .
COPY engine/ engine/
RUN pip install --user --no-cache-dir .

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8001/health', timeout=5)"
CMD ["uvicorn", "engine.main:app", "--host", "0.0.0.0", "--port", "8001"]
