#!/bin/bash
set -euo pipefail

echo "Starting Alembic migration..."

max_retries=3
count=1

until alembic upgrade head; do
    echo "Migration failed! Attempt $count of $max_retries..."
    if [ "$count" -ge "$max_retries" ]; then
        echo "All retries failed. Exiting."
        exit 1
    fi
    count=$((count + 1))
    sleep(2)
done

echo "✅ Migrations completed successfully."
