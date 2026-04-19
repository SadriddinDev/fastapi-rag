# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# --- final image ---
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
