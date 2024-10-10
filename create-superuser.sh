#!/usr/bin/bash

if [ -f .env ]; then
   source .env
fi

if [[ "$DATABASE" = "postgres" ]]
then
    echo "Waiting for postgres..."

    while ! netcat -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate --noinput

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py ensure_adminuser --username="$DJANGO_SUPERUSER_USERNAME" \
    --email="$DJANGO_SUPERUSER_EMAIL" \
    --password="$DJANGO_SUPERUSER_PASSWORD"
fi

"$@"