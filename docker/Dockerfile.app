# ===========================
# STAGE 1 — BUILDER
# ===========================
FROM python:3.14.0-slim AS builder

ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/shorty

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

RUN find /usr/local/lib/python3.14 -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
RUN find /usr/local/lib/python3.14 -type f -name "*.pyc" -delete
RUN poetry cache clear . --all --no-interaction


# ===========================
# STAGE 2 — RUNTIME
# ===========================
FROM python:3.14.0-slim AS runtime

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/local/shorty

COPY --from=builder /usr/local/lib/python3.14 /usr/local/lib/python3.14
COPY --from=builder /usr/local/bin /usr/local/bin

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY alembic.ini ./
COPY migrate.sh ./
COPY run.py ./
