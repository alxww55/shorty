# ===========================
# STAGE 1 — BUILDER
# ===========================
FROM python:3.14.0-slim AS builder

ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/shorty

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

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

COPY . .

ENTRYPOINT ["./migrate.sh"]

CMD ["python3", "run.py"]
