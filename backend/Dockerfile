FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libmariadb-dev-compat libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements/prod.txt .
RUN pip install --user --no-cache-dir -r prod.txt

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
