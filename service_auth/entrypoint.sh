#!/usr/bin/env bash
set -e

esperar_ala_db() {
  echo "Esperando a la base de datos ..."
  MAX_RETRIES=20
  COUNT=0
  until python - <<PY
import os, sys
import time
import psycopg2
from urllib.parse import urlparse

db_url = os.getenv("DATABASE_URL")
if not db_url:
    sys.exit(0)
p = urlparse(db_url)
conn_info = {
    "dbname": p.path.lstrip('/'),
    "user": p.username,
    "password": p.password,
    "host": p.hostname,
    "port": p.port or 5432
}
try:
    conn = psycopg2.connect(**conn_info)
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
PY
  do
    COUNT=$((COUNT+1))
    if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
      echo "La base de datos sigue sin estar disponible tras $MAX_RETRIES intentos; finalizando."
      exit 1
    fi
    sleep 2
  done
}

esperar_ala_db || true

echo "Aplicar migraciones a la base de datos ..."
python manage.py migrate --noinput

# opcional collectstatic en producción
# echo "Collect static"
# python manage.py collectstatic --noinput

echo "Inicializando el server ..."
exec "$@"
