# Django Heroku Docker

This is the ultimate full stack project using Heroku container build manifest to deploy. This is a generate template with Postgres, Celery, Redis, JWT.

## Deploy on Heroku

This template has a Dockerfile that is Django deployment ready using Heroku's container build manifest process. Each process in the Dockerfile is annotated to eplain each process. Migrations will be runned manually via Heroku docker container command line.

## Docker

remove existing images

```bash
docker stop django-heroku
docker rm django-heroku
```

build locally:

```bash
docker build -t web:latest .
docker run -d --name django-heroku -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```

view static files:

```bash
docker exec django-heroku ls /app/staticfiles
docker exec django-heroku ls /app/staticfiles/admin
```

to run commands within deployed heroku container:

```bash
heroku run python manage.py makemigrations -a {{HEROKU_APP_NAME}}
heroku run python manage.py migrate -a {{HEROKU_APP_NAME}}
```

## TIPS

- remember to check `ALLOWED_HOSTS` in settings to white list the correct domain
- killing a port: `kill -9 $(lsof -t -i tcp:8000)`
