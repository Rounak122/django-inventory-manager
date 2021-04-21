#!/bin/sh

set -e #Exit the script on encountring any error

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput # collect static files 

# runs our application using uWSGI
uwsgi --socket :8000 --master --enable-threads --module django_inventory_manager.wsgi
# uWSGI will run our application using socket (TCP) on port 8000 as master thread(foreground)
# threading is enabled , pass module app.wsgi( already built by django when project is created)

