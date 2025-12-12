#!/usr/bin/env bash
set -euo pipefail

# args: e.g. "gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"
# or "celery" "worker" "-A" "backend.celery.app" "-Q" "default" "--loglevel=info"

# Wait for DB to be ready (simple loop). For production, use a more robust wait-for.
if [ -n "${WAIT_FOR_DB:-1}" ]; then
  echo "Waiting for database..."
  until python - <<PY
import sys, psycopg2, os
try:
    dsn = {
        "dbname": os.environ.get("POSTGRES_DB"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": int(os.environ.get("POSTGRES_PORT", "5432")),
    }
    conn = psycopg2.connect(**dsn)
    conn.close()
    print("db ok")
except Exception as e:
    print("db not ready:", e)
    sys.exit(1)
PY
  do
    sleep 1
  done
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static only if USE_S3 is not enabled
if [ "${USE_S3:-false}" = "false" ] || [ "${USE_S3:-False}" = "FALSE" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

# Optionally create superuser / seed data (commented)
# python manage.py loaddata initial_data.json

# Execute the passed command
exec "$@"
