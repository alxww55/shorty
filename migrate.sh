#!/usr/bin/env bash

set -euo pipefail

echo "Applying Alembic migrations..."

max_retries=3
count=1

until alembic upgrade head; do
    echo "Migrations not apllied! Attempt $count of $max_retries..."
    if [ "$count" -ge "$max_retries" ]; then
        echo "All retries failed. Exiting."
        exit 1
    fi
    count=$((count + 1))
    sleep 5
done

echo "Migrations apllied successfully."

exec "$@"